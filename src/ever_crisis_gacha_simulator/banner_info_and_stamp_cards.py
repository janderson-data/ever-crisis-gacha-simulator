from decimal import Decimal, getcontext


getcontext().prec = 16  # Set Decimal to continue to a max of 16 decimal places


CLOUD_GLENN_LIMIT_BREAK_BANNER = {
    "metadata": {
        "characters": ["cloud", "glenn"],
        "weapons": ["stream_slasher_glenn", "stream_saber_cloud"],
        "costumes": ["saber_style_cloud", "vanguard_style_glenn"],
        "non_featured_five_star_percent_rate": Decimal("0.01339"),
        "end_date": "Apr 7, 2024",
        },
    "stamp_cards_list": {
        "page_one": [
            {"position": 6, "rule": "guaranteed_featured_five_star_draw"},
            ],
        "page_two": [
            {"position": 4, "rule": "guaranteed_featured_five_star_draw"},
            {"position": 6, "rule": "guaranteed_five_star_draw"},
            {"position": 8, "rule": "guaranteed_featured_five_star_draw"},
            ],
        "page_three": [
            {"position": 6, "rule": "guaranteed_featured_five_star_draw"},
            {"position": 12, "rule": "guaranteed_featured_five_star_draw"},
            ],
        "page_ex": [
            {"position": 6, "rule": "guaranteed_four_star_draw"},
            {"position": 12, "rule": "guaranteed_five_star_draw"},
            ],
        }
    }

ZACK_SEPHIROTH_LIMIT_BREAK_BANNER = {
    "metadata": {
        "characters": ["zack", "sephiroth"],
        "weapons": ["stream_guard_zack", "protectors_blade_sephiroth"],
        "costumes": ["lethal_style_sephiroth", "guardian_style_zack"],
        "non_featured_five_star_percent_rate": Decimal("0.01315"),
        "end_date": "Apr 7, 2024",
        },
    "stamp_cards_list": {
        "page_one": [
            {"position": 6, "rule": "guaranteed_featured_five_star_draw"},
            ],
        "page_two": [
            {"position": 4, "rule": "guaranteed_featured_five_star_draw"},
            {"position": 6, "rule": "guaranteed_five_star_draw"},
            {"position": 8, "rule": "guaranteed_featured_five_star_draw"},
            ],
        "page_three": [
            {"position": 6, "rule": "guaranteed_featured_five_star_draw"},
            {"position": 12, "rule": "guaranteed_featured_five_star_draw"},
            ],
        "page_ex": [
            {"position": 6, "rule": "guaranteed_four_star_draw"},
            {"position": 12, "rule": "guaranteed_five_star_draw"},
            ],
        }
    }