import numpy as np
from .stamp_card import StampCard
from .ten_draw import TenDraw
from ever_crisis_gacha_simulator.constants import *
from decimal import Decimal, getcontext


getcontext().prec = 16  # Set Decimal to continue to a max of 16 decimal places


class CrystalPullSession:
    """
    Class representing a pull session.
    """

    def __init__(
        self,
        session_criterion,
        criterion_value,
        banner_info,
        target_weapon_type,
        starting_weapon_parts=0,
    ):

        if target_weapon_type not in ["featured", "wishlisted"]:
            raise ValueError(
                "`target_weapon_type` must be a str of either 'featured' or 'wishlisted'. Provided: ",
                target_weapon_type,
            )

        self.target_weapon_type = target_weapon_type  # In a future refactor, this will be removed, as it will collect data on both types.

        if session_criterion not in ["overboost", "crystals_spent", "stamps_earned"]:
            raise ValueError(
                "`session_criterion` must be a str of either 'overboost', 'crystals_spent', or 'stamps_earned'. Provided: ",
                session_criterion
            )

        self.session_criterion = session_criterion
        self.criterion_value = criterion_value

        self.num_featured_weapons = len(banner_info["metadata"]["weapons"])

        self.target_weapon_rates_dict = generate_target_probabilities(
            num_featured_weapons=self.num_featured_weapons,
            target_weapon_type=self.target_weapon_type,
            non_featured_five_star_percent_rate=banner_info["metadata"]["non_featured_five_star_percent_rate"],
        )

        self.current_stamp_card_index = 0
        self.stamp_cards_list = banner_info["stamp_cards_list"]
        self.current_stamp_card = StampCard(
            self.stamp_cards_list[list(self.stamp_cards_list.keys())[self.current_stamp_card_index]]
        )

        self.completed_stamp_cards = []
        self.rules_for_next_ten_draw = []

        self.data = {
            "targeted_weapon_parts": starting_weapon_parts,
            "total_stamps_earned": 0,
            "num_crystals_spent": 0,
            "targeted_five_stars_drawn": 0,
            "targeted_four_stars_drawn": 0,
            "targeted_three_stars_drawn": 0,
            "nontargeted_featured_five_stars_drawn": 0,
            "nontargeted_featured_four_stars_drawn": 0,
            "nontargeted_featured_three_stars_drawn": 0,
            "nontargeted_five_stars_drawn": 0,
            "nontargeted_four_stars_drawn": 0,
            "nontargeted_three_stars_drawn": 0,
            "metadata": {
                "session_criterion": self.session_criterion,
                "criterion_value": self.criterion_value,
                "banner_info": banner_info,
                "target_weapon_rate_info": self.target_weapon_rates_dict,
                "starting_weapon_parts": starting_weapon_parts,
            },
        }

    def criterion_overboost(self, overboost_target):
        """
        Simulate pulling until reaching a desired overboost level for the targeted weapon.
        What we eventually care about in this situation is the number of crystals required to reach the
        targeted overboost level.
        """

        required_weapon_parts = (overboost_target + 1) * WEAPON_PARTS_PER_OVERBOOST

        while self.data["targeted_weapon_parts"] < required_weapon_parts:
            self.pre_draw_stamp_card_operations()
            self.perform_ten_draw()

    def criterion_crystals_spent(self, num_crystals_to_spend):
        """
        Simulate pulling until a certain number of crystals have been spent.
        What we eventually care about in this situation is the number of weapon parts we end up with after
        spending the indicated amount of crystals.
        """

        while (num_crystals_to_spend - self.data["num_crystals_spent"]) >= TEN_DRAW_CRYSTAL_COST:
            self.pre_draw_stamp_card_operations()
            self.perform_ten_draw()

    def criterion_stamps_earned(self, num_stamps_to_earn):
        """
        Simulate pulling until a certain number of stamps have been earned.
        What we eventually care about in this situation is the number of crystals spent AND weapon parts
        earned after we've earned the indicated number of stamps.
        """

        while self.data["total_stamps_earned"] < num_stamps_to_earn:
            self.pre_draw_stamp_card_operations()
            self.perform_ten_draw()

    def determine_stamp_value_for_ten_draw(self, predetermined_int=None):
        """
        Generates a number of stamps for the beginning of a 10-draw
        """

        if predetermined_int:
            stamp_randint = predetermined_int
        else:
            stamp_randint = np.random.default_rng().integers(
                low=1, high=10000, endpoint=True
            )

        if 1 <= stamp_randint <= 4500:
            stamp_value = 1
        elif 4501 <= stamp_randint <= 8000:
            stamp_value = 2
        elif 8001 <= stamp_randint <= 9592:
            stamp_value = 3
        elif 9593 <= stamp_randint <= 9794:
            stamp_value = 4
        elif 9795 <= stamp_randint <= 9944:
            stamp_value = 5
        elif 9945 <= stamp_randint <= 9999:
            stamp_value = 6
        else:
            stamp_value = 12

        return stamp_value

    def move_to_next_stamp_card(self):
        """
        Transition the pull session to the next stamp card.
        """

        self.completed_stamp_cards.append(self.current_stamp_card)

        self.current_stamp_card_index += 1

        # Continuously re-use the final (EX) card once all other cards are completed
        if self.current_stamp_card_index >= len(self.stamp_cards_list):
            self.current_stamp_card = StampCard(self.stamp_cards_list[list(self.stamp_cards_list.keys())[-1]])
        else:
            self.current_stamp_card = StampCard(
                self.stamp_cards_list[list(self.stamp_cards_list.keys())[self.current_stamp_card_index]]
            )

    def pre_draw_stamp_card_operations(self, predetermined_stamp_value=None):
        """
        Determine a stamp value, determine whether a stamp card has been completed based on the result, and
        determine if any stamp card rules need to go into the subsequent ten draw.
        """

        ten_draw_stamp_value = predetermined_stamp_value if predetermined_stamp_value else self.determine_stamp_value_for_ten_draw()

        self.data["total_stamps_earned"] += ten_draw_stamp_value

        new_stamp_value = (
            self.current_stamp_card.current_stamp_value + ten_draw_stamp_value
        )

        self.log_rules_for_next_draw(new_stamp_value)

        if new_stamp_value >= MAX_STAMP_CARD_VALUE:
            self.move_to_next_stamp_card()
            new_stamp_value_for_new_card = new_stamp_value - MAX_STAMP_CARD_VALUE
            self.log_rules_for_next_draw(new_stamp_value_for_new_card)
            self.current_stamp_card.current_stamp_value = new_stamp_value_for_new_card
        else:
            self.current_stamp_card.current_stamp_value = new_stamp_value

    def log_rules_for_next_draw(self, new_stamp_value):
        """
        Determines any special rules for a ten draw, based on the current and new stamp card values.
        """

        for _, row in self.current_stamp_card.position_and_rule_df.iterrows():
            if (
                self.current_stamp_card.current_stamp_value
                < row["position"]
                <= new_stamp_value
            ):
                self.rules_for_next_ten_draw.append(row["rule"])

    def perform_ten_draw(self):
        """
        Instantiates a TenDraw class object, uses its operations to perform a ten_draw, and stores the results.
        """
        ten_draw = TenDraw(
            self.rules_for_next_ten_draw,
            self.target_weapon_rates_dict,
            self.target_weapon_type,
            self.num_featured_weapons,
        )

        ten_draw.perform_ten_draw()

        self.data["targeted_weapon_parts"] += ten_draw.pull_results[
            "targeted_weapon_parts"
        ]

        self.data["num_crystals_spent"] += TEN_DRAW_CRYSTAL_COST

        for pull_result_string in ten_draw.pull_results["pull_result_strings"]:
            for pull_session_outcome in self.data:
                if pull_session_outcome.startswith(pull_result_string):
                    self.data[pull_session_outcome] += 1

        self.rules_for_next_ten_draw = []

    def execute_pull_session(self):
        """
        Executes a pull session, calling the appropriate function for the provided `session_criterion`.
        """
        if self.session_criterion == "overboost":
            if self.criterion_value > 10 or self.criterion_value < 0:
                raise ValueError("Simulations of criterion 'overboost' only support overboost levels between 0 (OB0) and 10 (OB10).\nEntered: ", self.criterion_value)
            self.criterion_overboost(overboost_target=self.criterion_value)
        elif self.session_criterion == "crystals_spent":
            if self.criterion_value < TEN_DRAW_CRYSTAL_COST:
                raise ValueError("Simulations of criterion 'crystals_spent' require at least 3,000 crystals as input. Provided: ", self.criterion_value)
            self.criterion_crystals_spent(num_crystals_to_spend=self.criterion_value)
        elif self.session_criterion == "stamps_earned":
            if self.criterion_value < 0:
                raise ValueError("Simulations of criterion 'stamps_earned' require a positive value. Provided: ", self.criterion_value)
            self.criterion_stamps_earned(num_stamps_to_earn=self.criterion_value)


# Having this as a separate function instead of a method allows for better integration with pytest
def generate_target_probabilities(
    num_featured_weapons, target_weapon_type, non_featured_five_star_percent_rate
):
    """
    Generate a dictionary containing all of the weapon draw rates based on the number of featured weapons and the
    non-featured five star weapon rate.
    """

    num_weapons_in_banner = (
        round(Decimal("1.5") / Decimal(str(non_featured_five_star_percent_rate)))
        + Decimal(str(5))
        + Decimal(str(num_featured_weapons))
    )

    if target_weapon_type == "wishlisted":

        target_five_star_rate = (
            Decimal("0.01") if num_featured_weapons == 1 else Decimal("0.008")
        )
        target_four_star_rate = (
            OVERALL_RARITY_RATES_DICT["four_star"]
            - ONE_FEATURED_TARGET_FEATURED_RATES_DICT["four_star"]
        ) / Decimal(str(num_weapons_in_banner - num_featured_weapons))
        target_three_star_rate = (
            OVERALL_RARITY_RATES_DICT["three_star"]
            - ONE_FEATURED_TARGET_FEATURED_RATES_DICT["three_star"]
        ) / Decimal(str(num_weapons_in_banner - num_featured_weapons))
        target_guaranteed_four_star_rate = (
            target_four_star_rate
            * (
                OVERALL_RARITY_RATES_DICT["four_star"]
                + OVERALL_RARITY_RATES_DICT["three_star"]
            )
            / OVERALL_RARITY_RATES_DICT["four_star"]
        )

        target_weapon_rates_dict = {
            "five_star": target_five_star_rate,
            "four_star": target_four_star_rate,
            "guaranteed_four_star": target_guaranteed_four_star_rate,
            "three_star": target_three_star_rate,
        }

        return target_weapon_rates_dict

    elif target_weapon_type == "featured" and num_featured_weapons == 1:

        return ONE_FEATURED_TARGET_FEATURED_RATES_DICT

    elif target_weapon_type == "featured" and num_featured_weapons == 2:

        return TWO_FEATURED_TARGET_FEATURED_RATES_DICT
