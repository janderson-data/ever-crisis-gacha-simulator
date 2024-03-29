import numpy as np
from decimal import Decimal, getcontext
from ever_crisis_gacha_simulator.constants import OVERALL_RARITY_RATES_DICT


getcontext().prec = 16  # Set Decimal to continue to a max of 16 decimal places


class TenDraw:
    """
    Class representing a set of 10 draws within a crystal pull session.
    """

    def __init__(
        self,
        rules_for_next_ten_draw,
        target_weapon_rates_dict,
        target_weapon_type,
        num_featured_weapons,
    ):
        self.special_rules = rules_for_next_ten_draw
        self.target_weapon_rates_dict = target_weapon_rates_dict
        self.target_weapon_type = target_weapon_type
        self.num_featured_weapons = num_featured_weapons
        self.pull_results = {
            "targeted_weapon_parts": 0,
            "pull_result_strings": [],
        }

    def draws_for_special_rules(self):
        """
        Perform correspending operation for each rule within the special rules list.
        """

        pull_result_strings = []

        for rule in self.special_rules:
            if rule == "guaranteed_featured_five_star_draw":
                pull_result_strings.append(
                    self.guaranteed_featured_five_star_draw(desired=True)
                )
            elif rule == "guaranteed_five_star_draw":
                pull_result_strings.append(self.guaranteed_five_star_draw())
            elif rule == "guaranteed_four_star_draw":
                pull_result_strings.append(self.guaranteed_four_star_draw())
            elif rule == "guaranteed_not_desired_five_star_draw":
                pull_result_strings.append(
                    self.guaranteed_featured_five_star_draw(desired=False)
                )

        return pull_result_strings

    def guaranteed_featured_five_star_draw(self, desired):
        """
        Pass a float with value restricted to targeted 5* range through `determine_pull_result()`, but only if the targeted weapon
        is a featured weapon.
        """

        if (
            desired and self.target_weapon_type == "featured"
        ):  # `desired` means the featured weapon in question is the one you actually want.

            random_float = np.random.default_rng().uniform(
                0, self.target_weapon_rates_dict["five_star"]
            )

            return self.determine_pull_result(random_float)
        else:
            # For now, this will make sure a 5* weapon gets logged.
            # Will change this once I allow the code to log featured and wishlisted simultaneously.

            random_float = np.random.default_rng().uniform(
                self.target_weapon_rates_dict["five_star"],
                OVERALL_RARITY_RATES_DICT["five_star"],
            )

            return self.determine_pull_result(random_float)

    def guaranteed_five_star_draw(self, seed=None):
        """
        Pass a float with value restricted to 5* outcomes through `determine_pull_result()`.
        """

        random_float = np.random.default_rng(seed).uniform(
            0, OVERALL_RARITY_RATES_DICT["five_star"]
        )

        return self.determine_pull_result(random_float)

    def guaranteed_four_star_draw(self, seed=None):
        """
        Pass a float into `determine_pull_result()` and process with all 3* probability rolled into 4* probability.
        """

        random_float = np.random.default_rng(seed).uniform(0, 1)

        return self.determine_pull_result(random_float, guaranteed_four_star=True)

    def determine_pull_result(self, random_float, guaranteed_four_star=False):
        """
        Processes the random_float created for a pull and returns the outcome as a string.
        Results are based on the range into which random_float falls.
        """

        random_decimal = Decimal(str(random_float))

        if self.num_featured_weapons == 1 or self.target_weapon_type == "wishlisted":
            if 0 <= random_decimal < self.target_weapon_rates_dict["five_star"]:
                return "targeted_five_star"
            elif (
                self.target_weapon_rates_dict["five_star"]
                <= random_decimal
                < OVERALL_RARITY_RATES_DICT["five_star"]
            ):
                return "nontargeted_five_star"
            elif guaranteed_four_star and OVERALL_RARITY_RATES_DICT[
                "five_star"
            ] <= random_decimal < (
                OVERALL_RARITY_RATES_DICT["five_star"]
                + self.target_weapon_rates_dict["guaranteed_four_star"]
            ):
                return "targeted_four_star"
            elif (
                guaranteed_four_star
                and (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + self.target_weapon_rates_dict["guaranteed_four_star"]
                )
                <= random_decimal
                < 1
            ):
                return "nontargeted_four_star"
            elif (
                OVERALL_RARITY_RATES_DICT["five_star"]
                <= random_decimal
                < (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + self.target_weapon_rates_dict["four_star"]
                )
            ):
                return "targeted_four_star"
            elif (
                (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + self.target_weapon_rates_dict["four_star"]
                )
                <= random_decimal
                < (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + OVERALL_RARITY_RATES_DICT["four_star"]
                )
            ):
                return "nontargeted_four_star"
            elif (
                (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + OVERALL_RARITY_RATES_DICT["four_star"]
                )
                <= random_decimal
                < (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + OVERALL_RARITY_RATES_DICT["four_star"]
                    + self.target_weapon_rates_dict["three_star"]
                )
            ):
                return "targeted_three_star"
            else:
                return "nontargeted_three_star"

        elif self.num_featured_weapons == 2 and self.target_weapon_type == "featured":
            if 0 <= random_decimal < self.target_weapon_rates_dict["five_star"]:
                return "targeted_five_star"
            elif (
                self.target_weapon_rates_dict["five_star"]
                <= random_decimal
                < 2 * self.target_weapon_rates_dict["five_star"]
            ):
                return "nontargeted_featured_five_star"
            elif (
                2 * self.target_weapon_rates_dict["five_star"]
                <= random_decimal
                < OVERALL_RARITY_RATES_DICT["five_star"]
            ):
                return "nontargeted_five_star"
            elif guaranteed_four_star and OVERALL_RARITY_RATES_DICT[
                "five_star"
            ] <= random_decimal < (
                OVERALL_RARITY_RATES_DICT["five_star"]
                + self.target_weapon_rates_dict["guaranteed_four_star"]
            ):
                return "targeted_four_star"
            elif guaranteed_four_star and (
                OVERALL_RARITY_RATES_DICT["five_star"]
                + self.target_weapon_rates_dict["guaranteed_four_star"]
            ) <= random_decimal < (
                OVERALL_RARITY_RATES_DICT["five_star"]
                + 2 * self.target_weapon_rates_dict["guaranteed_four_star"]
            ):
                return "nontargeted_featured_four_star"
            elif (
                guaranteed_four_star
                and (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + 2 * self.target_weapon_rates_dict["guaranteed_four_star"]
                )
                <= random_decimal
                < 1
            ):
                return "nontargeted_four_star"
            elif (
                OVERALL_RARITY_RATES_DICT["five_star"]
                <= random_decimal
                < (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + self.target_weapon_rates_dict["four_star"]
                )
            ):
                return "targeted_four_star"
            elif (
                (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + self.target_weapon_rates_dict["four_star"]
                )
                <= random_decimal
                < (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + 2 * self.target_weapon_rates_dict["four_star"]
                )
            ):
                return "nontargeted_featured_four_star"
            elif (
                (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + 2 * self.target_weapon_rates_dict["four_star"]
                )
                <= random_decimal
                < (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + OVERALL_RARITY_RATES_DICT["four_star"]
                )
            ):
                return "nontargeted_four_star"
            elif (
                (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + OVERALL_RARITY_RATES_DICT["four_star"]
                )
                <= random_decimal
                < (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + OVERALL_RARITY_RATES_DICT["four_star"]
                    + self.target_weapon_rates_dict["three_star"]
                )
            ):
                return "targeted_three_star"
            elif (
                (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + OVERALL_RARITY_RATES_DICT["four_star"]
                    + self.target_weapon_rates_dict["three_star"]
                )
                <= random_decimal
                < (
                    OVERALL_RARITY_RATES_DICT["five_star"]
                    + OVERALL_RARITY_RATES_DICT["four_star"]
                    + 2 * self.target_weapon_rates_dict["three_star"]
                )
            ):
                return "nontargeted_featured_three_star"
            else:
                return "nontargeted_three_star"

    @staticmethod
    def convert_pull_result_to_weapon_parts(pull_result_string):
        """
        Converts a pull result into a number of weapons parts for the targeted weapon.
        """

        if pull_result_string == "targeted_five_star":
            return 200
        elif pull_result_string == "targeted_four_star":
            return 10
        elif pull_result_string == "targeted_three_star":
            return 1
        else:
            return 0

    def standard_single_draws(self, number_of_draws, seed=None):
        """
        Passes a `number_of_draws` random floats through `determine_pull_result()` and returns a list of the result strings.
        """

        random_floats = np.random.default_rng(seed).uniform(
            low=0, high=1, size=number_of_draws
        )

        return [
            self.determine_pull_result(random_float) for random_float in random_floats
        ]

    def perform_ten_draw(self):
        """
        Perform ten draws -- draws with special rules first, and then standard draws until ten have been completed.
        Store the pull results, including result strings and total weapon parts, in the `pull_results` attribute.
        """

        self.pull_results["pull_result_strings"].extend(self.draws_for_special_rules())

        number_of_remaining_draws = 10 - len(self.special_rules)

        self.pull_results["pull_result_strings"].extend(
            self.standard_single_draws(number_of_draws=number_of_remaining_draws)
        )

        for pull_result in self.pull_results["pull_result_strings"]:
            self.pull_results[
                "targeted_weapon_parts"
            ] += self.convert_pull_result_to_weapon_parts(pull_result)
