from decimal import Decimal, getcontext


getcontext().prec = 16  # Set Decimal to continue to a max of 16 decimal places

### STATIC AMOUNTS ###
TEN_DRAW_CRYSTAL_COST = 3000
MAX_STAMP_CARD_VALUE = 12
WEAPON_PARTS_PER_OVERBOOST = 200

### PULL RATE DICTIONARIES ###
OVERALL_RARITY_RATES_DICT = {
    "five_star": Decimal("0.075"),
    "four_star": Decimal("0.225"),
    "three_star": Decimal("0.70"),
}

ONE_FEATURED_TARGET_FEATURED_RATES_DICT = {
    "five_star": Decimal("0.01"),
    "four_star": Decimal("0.10"),
    "guaranteed_four_star": Decimal("0.10")
    * (OVERALL_RARITY_RATES_DICT["four_star"] + OVERALL_RARITY_RATES_DICT["three_star"])
    / OVERALL_RARITY_RATES_DICT["four_star"],
    "three_star": Decimal("0.20"),
}

TWO_FEATURED_TARGET_FEATURED_RATES_DICT = {
    "five_star": Decimal("0.01"),
    "four_star": Decimal("0.05"),  # Totaling 0.10 across both featured weapons
    "guaranteed_four_star": Decimal("0.05")
    * (OVERALL_RARITY_RATES_DICT["four_star"] + OVERALL_RARITY_RATES_DICT["three_star"])
    / OVERALL_RARITY_RATES_DICT["four_star"],
    "three_star": Decimal("0.10"),  # Totaling 0.20 across both featured weapons
}
