import numpy as np
import pandas as pd
from decimal import Decimal


class StampCard:
    """
    Class representing a single stamp card during a pull session.
    """
    def __init__(self, stamp_card_position_dicts):

        self.rule_enum = [
             'guaranteed_feature_five_star_draw',
             'guaranteed_five_star_draw',
             'guaranteed_four_star_draw',
             'guaranteed_not_desired_draw',
        ]

        self.position_and_rule_df = pd.DataFrame(stamp_card_position_dicts)

        self.validate_stamp_card_rules()

        self.current_stamp_value = 0

    def validate_stamp_card_rules(self):
        """
        Make sure only supported stamp card rules were provided.
        """

        unsupported_stamp_card_rules = []

        for rule in self.position_and_rule_df['rule'].drop_duplicates().to_list():
            if rule not in rule_enum:
                unsupported_stamp_card_rules.append(rule)

        if len(unsupported_stamp_card_rules) != 0:
            raise ValueError("One or more unsupported rules in stamp cards", unsupported_stamp_card_rules)