import numpy as np
import pandas as pd
from stamp_card import StampCard
from ten_draw import TenDraw
from constants import *
from decimal import Decimal


class CrystalPullSession:
    """
    Class representing a pull session.
    """
    def __init__(self, stamp_cards_list, num_featured_weapons, non_featured_five_star_percent_rate, starting_weapon_parts=0, target_weapon_type):

        self.target_weapon_type = target_weapon_type  # In a future refactor, this will be removed, as it will collect data on both types.

        self.target_weapon_rates_dict = self.generate_target_probabilities(num_featured_weapons, self.target_weapon_type, non_featured_five_star_percent_rate)

        self.current_stamp_card_index = 0
        self.stamp_cards_list = stamp_cards_list
        self.current_stamp_card = StampCard(self.stamp_cards_list[self.current_stamp_card_index])

        self.completed_stamp_cards = []
        self.rules_for_next_ten_draw = []

        self.data = {
            'targeted_weapon_parts': starting_weapon_parts,
            'targeted_five_stars_drawn': 0,
            'targeted_four_stars_drawn': 0,
            'targeted_three_stars_drawn': 0,
            'nontargeted_five_stars_drawn': 0,
            'nontargeted_four_stars_drawn': 0,
            'nontargeted_three_stars_drawn': 0,
        }

    def criterion_target_overboost(self, overboost_target):
        """
        Simulate pulling until reaching a desired overboost level for the targeted weapon.
        """

        required_weapon_parts = (overboost_target + 1) * 200

        while self.data['targeted_weapon_parts'] < required_weapon_parts:
            self.pre_draw_stamp_card_operations()
            self.perform_ten_draw()

    def determine_stamp_value_for_ten_draw(self, seed=None):
        """
        Generates a number of stamps for the beginning of a 10-draw
        """

        stamp_randint = np.random.default_rng(seed).integers(low=1, high=10000, endpoint=True)

        if 1 <= stamp_randint <= 4500:
            stamp_value = self.current_stamp_card.current_stamp_value + 1
        elif 4501 <= stamp_randint <= 8000:
            stamp_value = self.current_stamp_card.current_stamp_value + 2
        elif 8001 <= stamp_randint <= 9592:
            stamp_value = self.current_stamp_card.current_stamp_value + 3
        elif 9593 <= stamp_randint <= 9794:
            stamp_value = self.current_stamp_card.current_stamp_value + 4
        elif 9795 <= stamp_randint <= 9944:
            stamp_value = self.current_stamp_card.current_stamp_value + 5
        elif 9945 <= stamp_randint <= 9999:
            stamp_value = self.current_stamp_card.current_stamp_value + 6
        else:
            stamp_value = self.current_stamp_card.current_stamp_value + 12

        return stamp_value

    def move_to_next_stamp_card(self):
        """
        Transition the pull session to the next stamp card.
        """

        self.completed_stamp_cards.append(self.current_stamp_card)

        self.current_stamp_card_index += 1

        # Continuously re-use the final (EX) card once all other cards are completed
        if self.current_stamp_card_index >= len(self.stamp_cards_list):
            self.current_stamp_card = StampCard(self.stamp_cards_list[-1])
        else:
            self.current_stamp_card = StampCard(self.stamp_cards_list[self.current_stamp_card_index])

    def pre_draw_stamp_card_operations(self):
        """
        Determine a stamp value, determine whether a stamp card has been completed based on the result, and
        determine if any stamp card rules need to go into the subsequent ten draw.
        """

        ten_draw_stamp_value = self.determine_stamp_value_for_ten_draw()

        new_stamp_value = self.current_stamp_card.current_stamp_value + ten_draw_stamp_value

        self.log_rules_for_next_draw(new_stamp_value)

        if new_stamp_value >= 12:
            self.move_to_next_stamp_card()
            new_stamp_value_for_new_card = new_stamp_value - 12
            self.log_rules_for_next_draw(new_stamp_value_for_new_card)
            self.current_stamp_card.current_stamp_value = new_stamp_value_for_new_card
        else:
            self.current_stamp_card.current_stamp_value = new_stamp_value

    def log_rules_for_next_draw(self, new_stamp_value):
        """
        Determines any special rules for a ten draw, based on the current and new stamp card values.
        """

        for _, row in self.current_stamp_card.position_and_rule_df.iterrows():
            if self.current_stamp_card.current_stamp_value < row['position'] <= new_stamp_value:
                self.rules_for_next_ten_draw.append(row['rule'])

    def perform_ten_draw(self):
        """
        Instantiates a TenDraw class object, uses its operations to perform a ten_draw, and stores the results.
        """
        ten_draw = TenDraw(self.rules_for_next_ten_draw, self.target_weapon_rates_dict)

        ten_draw.perform_ten_draw()

        self.data['targeted_weapon_parts'] += ten_draw.pull_results['targeted_weapon_parts']

        for pull_result_string in ten_draw.pull_results['pull_result_strings']:
            for pull_session_outcome in self.data:
                if pull_session_outcome.startswith(pull_result_string):
                    self.data[pull_session_outcome] += 1

    def generate_target_probabilities(num_featured_weapons, target_weapon_type, non_featured_five_star_percent_rate):

        """
        Generate a dictionary containing all of the weapon draw rates based on the number of featured weapons and the
        non-featured five star weapon rate.
        """

        num_weapons_in_banner = round(1.5 / non_featured_five_star_percent_rate) + 5 + num_featured_weapons

        if target_weapon_type == 'wishlisted':

            target_five_star_rate = 0.01 if num_featured_weapons == 1 else 0.008
            target_four_star_rate = Decimal(OVERALL_RARITY_RATES_DICT['four_star'] - ONE_FEATURED_TARGET_FEATURED_RATES_DICT['four_star']) / Decimal(num_weapons_in_banner - num_featured_weapons)
            target_three_star_rate = Decimal(OVERALL_RARITY_RATES_DICT['three_star'] - ONE_FEATURED_TARGET_FEATURED_RATES_DICT['three_star']) / Decimal(num_weapons_in_banner - num_featured_weapons)
            target_guaranteed_four_star_rate = target_four_star_rate * (OVERALL_RARITY_RATES_DICT['four_star'] + OVERALL_RARITY_RATES_DICT['three_star']) / OVERALL_RARITY_RATES_DICT['four_star']

            target_weapon_rates_dict = {
                'five_star': target_five_star_rate,
                'four_star': target_four_star_rate,
                'guaranteed_four_star': target_guaranteed_four_star_rate,
                'three_star': target_three_star_rate,
            }

            return target_weapon_rates_dict

        elif target_weapon_type == 'featured' and num_featured_weapons == 1:

            return ONE_FEATURED_TARGET_FEATURED_RATES_DICT

        elif target_weapon_type == 'featured' and num_featured_weapons == 2:

            return TWO_FEATURED_TARGET_FEATURED_RATES_DICT