OVERALL_RARITY_RATES_DICT = {  # Move to a constants module
    'five_star': 0.075,
    'four_star': 0.225,
    'three_star': 0.70
    }

ONE_FEATURED_TARGET_FEATURED_RATES_DICT = {  # Move to a constants module
    'five_star': 0.01,
    'four_star': 0.10,  # Not sure if this is true for two featured weapons
    'guaranteed_four_star': 0.10 * (OVERALL_RARITY_RATES_DICT['four_star'] + OVERALL_RARITY_RATES_DICT['three_star']) / OVERALL_RARITY_RATES_DICT['four_star'],
    'three_star': 0.20,  # Not sure if this is true for two featured weapons
    }

TWO_FEATURED_TARGET_FEATURED_RATES_DICT = {
    'five_star': 0.01,
    'four_star': 0.05,  # Totaling 0.10 across both featured weapons
    'guaranteed_four_star': 0.05 * (OVERALL_RARITY_RATES_DICT['four_star'] + OVERALL_RARITY_RATES_DICT['three_star']) / OVERALL_RARITY_RATES_DICT['four_star'],
    'three_star': 0.10,  # Totaling 0.20 across both featured weapons
    }