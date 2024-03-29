import pandas as pd
import pytest
from decimal import Decimal, getcontext
from ever_crisis_gacha_simulator.classes.ten_draw import TenDraw
from ever_crisis_gacha_simulator.classes.stamp_card import StampCard
from ever_crisis_gacha_simulator.constants import *
from ever_crisis_gacha_simulator.classes.crystal_pull_session import (
    generate_target_probabilities,
)


getcontext().prec = 16  # Set Decimal to continue to a max of 16 decimal places


@pytest.fixture()
def dpr_test_cases_df():
    """
    A dataframe containing the expected results for a predetermined set of float values that will be
    used to test the `determine_pull_results()` method under various conditions.
    """

    pull_float_list = [
        0.001,
        0.0099,
        0.01,
        0.018,
        0.02,
        0.075,
        0.10,
        0.125,
        0.165,
        0.175,
        0.286,
        0.29,
        0.3,
        0.35,
        0.4,
        0.486,
        0.49,
        0.50,
        0.99999,
    ]

    one_no_gfs_feat = (
        [  # One featured weapon, no guaranteed_four_star, target featured weapon
            "targeted_five_star",
            "targeted_five_star",
            "nontargeted_five_star",
            "nontargeted_five_star",
            "nontargeted_five_star",
            "targeted_four_star",
            "targeted_four_star",
            "targeted_four_star",
            "targeted_four_star",
            "nontargeted_four_star",
            "nontargeted_four_star",
            "nontargeted_four_star",
            "targeted_three_star",
            "targeted_three_star",
            "targeted_three_star",
            "targeted_three_star",
            "targeted_three_star",
            "nontargeted_three_star",
            "nontargeted_three_star",
        ]
    )

    one_no_gfs_wish = (
        [  # One featured weapon, no gauranteed_four_star, target wishlisted weapon
            "targeted_five_star",
            "targeted_five_star",
            "nontargeted_five_star",
            "nontargeted_five_star",
            "nontargeted_five_star",
            "targeted_four_star",
            "nontargeted_four_star",
            "nontargeted_four_star",
            "nontargeted_four_star",
            "nontargeted_four_star",
            "nontargeted_four_star",
            "nontargeted_four_star",
            "targeted_three_star",
            "nontargeted_three_star",
            "nontargeted_three_star",
            "nontargeted_three_star",
            "nontargeted_three_star",
            "nontargeted_three_star",
            "nontargeted_three_star",
        ]
    )

    one_yes_gfs_feat = [
        "targeted_five_star",
        "targeted_five_star",
        "nontargeted_five_star",
        "nontargeted_five_star",
        "nontargeted_five_star",
        "targeted_four_star",
        "targeted_four_star",
        "targeted_four_star",
        "targeted_four_star",
        "targeted_four_star",
        "targeted_four_star",
        "targeted_four_star",
        "targeted_four_star",
        "targeted_four_star",
        "targeted_four_star",
        "targeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
    ]

    one_yes_gfs_wish = [
        "targeted_five_star",
        "targeted_five_star",
        "nontargeted_five_star",
        "nontargeted_five_star",
        "nontargeted_five_star",
        "targeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
    ]

    two_no_gfs_feat = [
        "targeted_five_star",
        "targeted_five_star",
        "nontargeted_featured_five_star",
        "nontargeted_featured_five_star",
        "nontargeted_five_star",
        "targeted_four_star",
        "targeted_four_star",
        "nontargeted_featured_four_star",
        "nontargeted_featured_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "targeted_three_star",
        "targeted_three_star",
        "nontargeted_featured_three_star",
        "nontargeted_featured_three_star",
        "nontargeted_featured_three_star",
        "nontargeted_three_star",
        "nontargeted_three_star",
    ]

    two_no_gfs_wish = [
        "targeted_five_star",
        "nontargeted_five_star",
        "nontargeted_five_star",
        "nontargeted_five_star",
        "nontargeted_five_star",
        "targeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "targeted_three_star",
        "nontargeted_three_star",
        "nontargeted_three_star",
        "nontargeted_three_star",
        "nontargeted_three_star",
        "nontargeted_three_star",
        "nontargeted_three_star",
    ]

    two_yes_gfs_feat = [
        "targeted_five_star",
        "targeted_five_star",
        "nontargeted_featured_five_star",
        "nontargeted_featured_five_star",
        "nontargeted_five_star",
        "targeted_four_star",
        "targeted_four_star",
        "targeted_four_star",
        "targeted_four_star",
        "targeted_four_star",
        "nontargeted_featured_four_star",
        "nontargeted_featured_four_star",
        "nontargeted_featured_four_star",
        "nontargeted_featured_four_star",
        "nontargeted_featured_four_star",
        "nontargeted_featured_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
    ]

    two_yes_gfs_wish = [
        "targeted_five_star",
        "nontargeted_five_star",
        "nontargeted_five_star",
        "nontargeted_five_star",
        "nontargeted_five_star",
        "targeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
        "nontargeted_four_star",
    ]

    dpr_test_cases_df = pd.DataFrame(
        data={
            "pull_float": pull_float_list,
            "one_no_gfs_feat": one_no_gfs_feat,
            "one_no_gfs_wish": one_no_gfs_wish,
            "one_yes_gfs_feat": one_yes_gfs_feat,
            "one_yes_gfs_wish": one_yes_gfs_wish,
            "two_no_gfs_feat": two_no_gfs_feat,
            "two_no_gfs_wish": two_no_gfs_wish,
            "two_yes_gfs_feat": two_yes_gfs_feat,
            "two_yes_gfs_wish": two_yes_gfs_wish,
        }
    )

    return dpr_test_cases_df


@pytest.fixture()
def non_featured_five_star_percent_rate():
    """
    Returns the rate at which 5* weapons that are not featured or wishlisted will appear during draws.
    Currently set to the number of weapons when development on the gacha simulator first began.
    """
    non_featured_non_wishlisted_five_star_rate = Decimal("1.5")
    number_of_non_featured_no_wishlisted_weapons = Decimal("105")
    non_featured_five_star_percent_rate = (
        non_featured_non_wishlisted_five_star_rate
        / number_of_non_featured_no_wishlisted_weapons
    )

    return non_featured_five_star_percent_rate


@pytest.fixture()
def special_rule_test_inputs_df():
    """
    Create a dataframe consisting of test inputs for `draws_for_special_rules`.
    """

    # Pull enums from an arbitrary StampCard object for convenience
    stamp_card_rule_enum = StampCard(
        [{"position": 1, "rule": "guaranteed_five_star_draw"}]
    ).rule_enum

    test_inputs_dict = {}

    for rule in stamp_card_rule_enum:
        test_inputs_dict[rule] = None
        rule_array = ((rule + " ") * 10_000).split(" ")[
            :-1
        ]  # List with 10,000 instances of the rule, minus the last element, which is just a space
        test_inputs_dict[rule] = rule_array

    test_inputs_df = pd.DataFrame(test_inputs_dict)

    return test_inputs_df


@pytest.fixture()
def special_rule_acceptable_outputs_dict():
    """
    A dictionary containing acceptable outputs for special draws. Keys are special draw rules, and values are acceptable outputs for that rule.
    Also includes functionality to detect whether someone has added a new special rule to StampCard without updating the special_draw tests.
    """

    # Pull enums from an arbitrary StampCard object so the test will alert developer to update it if new enums are added
    stamp_card_rule_enum = StampCard(
        [{"position": 1, "rule": "guaranteed_five_star_draw"}]
    ).rule_enum

    acceptable_outputs_dict = {
        "guaranteed_featured_five_star_draw": ["targeted_five_star"],
        "guaranteed_five_star_draw": [
            "targeted_five_star",
            "nontargeted_featured_five_star",
            "nontargeted_five_star",
        ],
        "guaranteed_four_star_draw": [
            "targeted_five_star",
            "nontargeted_featured_five_star",
            "nontargeted_five_star",
            "targeted_four_star",
            "nontargeted_featured_four_star",
            "nontargeted_four_star",
        ],
        "guaranteed_not_desired_five_star_draw": [
            "nontargeted_featured_five_star",
            "nontargeted_five_star",
        ],
    }

    for rule in stamp_card_rule_enum:
        missing_rule_list = []
        if rule not in acceptable_outputs_dict.keys():
            missing_rule_list.append(rule)

    if len(missing_rule_list) > 0:
        raise KeyError(
            "Need new test and update to pytest.fixture `special_rule_acceptable_outputs_dict` for the following new enum(s):\n",
            missing_rule_list,
        )

    return acceptable_outputs_dict


def run_parameterized_dpr_test(
    num_featured_weapons,
    target_weapon_type,
    guaranteed_four_star,
    dpr_test_cases_df,
    non_featured_five_star_percent_rate,
):
    """
    Generates appropriate test code for `determine_pull_result()` based on input paramaters.
    """

    if num_featured_weapons == 1:
        featured_weapon_count_string = "one"
    elif num_featured_weapons == 2:
        featured_weapon_count_string = "two"
    else:
        raise ValueError(
            "Unsupported number of featured weapons (should be 1 or 2).\nProvided: ",
            num_featured_weapons,
        )

    gfs_string = "yes_gfs" if guaranteed_four_star else "no_gfs"

    if target_weapon_type == "featured":
        fow_string = "feat"
    elif target_weapon_type == "wishlisted":
        fow_string = "wish"
    else:
        raise ValueError(
            "`target_weapon_type` should only be 'featured' or 'wishlisted'.\nProvided: ",
            target_weapon_type,
        )

    # TenDraw class objects require `target_weapon_rates_dict` as input
    target_weapon_rates_dict = generate_target_probabilities(
        num_featured_weapons=num_featured_weapons,
        target_weapon_type=target_weapon_type,
        non_featured_five_star_percent_rate=non_featured_five_star_percent_rate,
    )

    test_ten_draw = TenDraw(
        rules_for_next_ten_draw=[],
        target_weapon_rates_dict=target_weapon_rates_dict,
        target_weapon_type=target_weapon_type,
        num_featured_weapons=num_featured_weapons,
    )

    # Filter down the `dpr_test_cases_df` fixture for easier viewing of relevant columns if a test fails
    select_test_cases_df = dpr_test_cases_df[
        ["pull_float", f"{featured_weapon_count_string}_{gfs_string}_{fow_string}"]
    ].copy()

    # Generate all of my test results
    select_test_cases_df["output"] = [
        test_ten_draw.determine_pull_result(
            pull_float,
            guaranteed_four_star=guaranteed_four_star,
        )
        for pull_float in select_test_cases_df["pull_float"]
    ]

    select_test_cases_df["result"] = select_test_cases_df.apply(
        (
            lambda row: (
                "PASS"
                if row["output"]
                == row[f"{featured_weapon_count_string}_{gfs_string}_{fow_string}"]
                else "FAIL"
            )
        ),
        axis=1,
    )

    df_for_print = select_test_cases_df[
        [
            "pull_float",
            "output",
            f"{featured_weapon_count_string}_{gfs_string}_{fow_string}",
            "result",
        ]
    ].rename(
        columns={"pull_float": "input"},
        inplace=False,
    )

    print(df_for_print.to_string())

    assert all(
        select_test_cases_df["output"]
        == select_test_cases_df[
            f"{featured_weapon_count_string}_{gfs_string}_{fow_string}"
        ]
    )


def run_parameterized_special_rules_test(
    special_rule,
    special_rule_test_inputs_df,
    non_featured_five_star_percent_rate,
    special_rule_acceptable_outputs_dict,
):
    """
    Tests `draws_for_special_rules` for a specific special rule, filtering the inputs df to only what's needed.
    """

    # These inputs allow the full range of values to be tested
    num_featured_weapons = 2
    target_weapon_type = "featured"

    target_weapon_rates_dict = generate_target_probabilities(
        num_featured_weapons=num_featured_weapons,
        target_weapon_type=target_weapon_type,
        non_featured_five_star_percent_rate=non_featured_five_star_percent_rate,
    )

    special_rule_test_inputs_df[special_rule].tolist()

    test_ten_draw = TenDraw(
        rules_for_next_ten_draw=special_rule_test_inputs_df[special_rule].tolist(),
        target_weapon_rates_dict=target_weapon_rates_dict,
        target_weapon_type=target_weapon_type,
        num_featured_weapons=num_featured_weapons,
    )

    special_draws_output = test_ten_draw.draws_for_special_rules()

    test_output_df = special_rule_test_inputs_df.copy()
    test_output_df["outputs"] = special_draws_output
    test_output_df["result"] = test_output_df.apply(
        (
            lambda row: (
                "PASS"
                if row["outputs"] in special_rule_acceptable_outputs_dict[special_rule]
                else "FAIL"
            )
        ),
        axis=1,
    )
    test_output_df.rename(columns={special_rule: "inputs"}, inplace=True)

    deduplicated_test_output_df = test_output_df[
        ["inputs", "outputs", "result"]
    ].drop_duplicates()

    print(deduplicated_test_output_df.to_string())

    assert all(deduplicated_test_output_df["result"] == "PASS")


def test_determine_pull_result_one_no_gfs_feat(
    dpr_test_cases_df, non_featured_five_star_percent_rate
):
    """
    Tests `determine_pull_result()` with one featured weapon, no guaranteed four star, and targeting the featured weapon.
    """

    num_featured_weapons = 1
    guaranteed_four_star = False
    target_weapon_type = "featured"

    run_parameterized_dpr_test(
        target_weapon_type=target_weapon_type,
        num_featured_weapons=num_featured_weapons,
        guaranteed_four_star=guaranteed_four_star,
        dpr_test_cases_df=dpr_test_cases_df,
        non_featured_five_star_percent_rate=non_featured_five_star_percent_rate,
    )


def test_determine_pull_result_one_no_gfs_wish(
    dpr_test_cases_df, non_featured_five_star_percent_rate
):
    """
    Tests `determine_pull_result()` with one featured weapon, no guaranteed four star, and targeting a wishlisted weapon.
    """

    num_featured_weapons = 1
    guaranteed_four_star = False
    target_weapon_type = "wishlisted"

    run_parameterized_dpr_test(
        target_weapon_type=target_weapon_type,
        num_featured_weapons=num_featured_weapons,
        guaranteed_four_star=guaranteed_four_star,
        dpr_test_cases_df=dpr_test_cases_df,
        non_featured_five_star_percent_rate=non_featured_five_star_percent_rate,
    )


def test_determine_pull_result_one_yes_gfs_feat(
    dpr_test_cases_df, non_featured_five_star_percent_rate
):
    """
    Tests `determine_pull_result()` with one featured weapon, guaranteed four star, and targeting the featured weapon.
    """

    num_featured_weapons = 1
    guaranteed_four_star = True
    target_weapon_type = "featured"

    run_parameterized_dpr_test(
        target_weapon_type=target_weapon_type,
        num_featured_weapons=num_featured_weapons,
        guaranteed_four_star=guaranteed_four_star,
        dpr_test_cases_df=dpr_test_cases_df,
        non_featured_five_star_percent_rate=non_featured_five_star_percent_rate,
    )


def test_determine_pull_result_one_yes_gfs_wish(
    dpr_test_cases_df, non_featured_five_star_percent_rate
):
    """
    Tests `determine_pull_result()` with one featured weapon, guaranteed four star, and targeting a wishlisted weapon.
    """

    num_featured_weapons = 1
    guaranteed_four_star = True
    target_weapon_type = "wishlisted"

    run_parameterized_dpr_test(
        target_weapon_type=target_weapon_type,
        num_featured_weapons=num_featured_weapons,
        guaranteed_four_star=guaranteed_four_star,
        dpr_test_cases_df=dpr_test_cases_df,
        non_featured_five_star_percent_rate=non_featured_five_star_percent_rate,
    )


def test_determine_pull_result_two_no_gfs_feat(
    dpr_test_cases_df, non_featured_five_star_percent_rate
):
    """
    Tests `determine_pull_result()` with two featured weapons, no guaranteed four star, and targeting a featured weapon.
    """

    num_featured_weapons = 2
    guaranteed_four_star = False
    target_weapon_type = "featured"

    run_parameterized_dpr_test(
        target_weapon_type=target_weapon_type,
        num_featured_weapons=num_featured_weapons,
        guaranteed_four_star=guaranteed_four_star,
        dpr_test_cases_df=dpr_test_cases_df,
        non_featured_five_star_percent_rate=non_featured_five_star_percent_rate,
    )


def test_determine_pull_result_two_no_gfs_wish(
    dpr_test_cases_df, non_featured_five_star_percent_rate
):
    """
    Tests `determine_pull_result()` with two featured weapons, no guaranteed four star, and targeting a wishlisted weapon.
    """

    num_featured_weapons = 2
    guaranteed_four_star = False
    target_weapon_type = "wishlisted"

    run_parameterized_dpr_test(
        target_weapon_type=target_weapon_type,
        num_featured_weapons=num_featured_weapons,
        guaranteed_four_star=guaranteed_four_star,
        dpr_test_cases_df=dpr_test_cases_df,
        non_featured_five_star_percent_rate=non_featured_five_star_percent_rate,
    )


def test_determine_pull_result_two_yes_gfs_feat(
    dpr_test_cases_df, non_featured_five_star_percent_rate
):
    """
    Tests `determine_pull_result()` with two featured weapons, guaranteed four star, and targeting a featured weapon.
    """

    num_featured_weapons = 2
    guaranteed_four_star = True
    target_weapon_type = "featured"

    run_parameterized_dpr_test(
        target_weapon_type=target_weapon_type,
        num_featured_weapons=num_featured_weapons,
        guaranteed_four_star=guaranteed_four_star,
        dpr_test_cases_df=dpr_test_cases_df,
        non_featured_five_star_percent_rate=non_featured_five_star_percent_rate,
    )


def test_determine_pull_result_two_yes_gfs_wish(
    dpr_test_cases_df, non_featured_five_star_percent_rate
):
    """
    Tests `determine_pull_result()` with two featured weapons, guaranteed four star, and targeting a wishlisted weapon.
    """

    num_featured_weapons = 2
    guaranteed_four_star = True
    target_weapon_type = "wishlisted"

    run_parameterized_dpr_test(
        target_weapon_type=target_weapon_type,
        num_featured_weapons=num_featured_weapons,
        guaranteed_four_star=guaranteed_four_star,
        dpr_test_cases_df=dpr_test_cases_df,
        non_featured_five_star_percent_rate=non_featured_five_star_percent_rate,
    )


def test_convert_pull_result_to_weapon_parts():
    """
    Ensures that `convert_pull_result_to_weapon_parts` always returns the correct number of
    weapon parts for its inputs.
    """

    cpr_test_case_df = pd.DataFrame(
        {
            "inputs": [
                "targeted_five_star",
                "nontargeted_featured_five_star",
                "nontargeted_five_star",
                "targeted_four_star",
                "nontargeted_featured_four_star",
                "nontargeted_four_star",
                "targeted_three_star",
                "nontargeted_featured_three_star",
                "nontargeted_three_star",
            ],
            "expected_results": [
                200,
                0,
                0,
                10,
                0,
                0,
                1,
                0,
                0,
            ],
        }
    )

    cpr_test_case_df["outputs"] = [
        TenDraw.convert_pull_result_to_weapon_parts(pull_result_string=input)
        for input in cpr_test_case_df["inputs"]
    ]

    cpr_test_case_df["result"] = cpr_test_case_df.apply(
        (lambda row: ("PASS" if row["outputs"] == row["expected_results"] else "FAIL")),
        axis=1,
    )

    print(cpr_test_case_df.to_string())

    assert all(cpr_test_case_df["outputs"]) == all(cpr_test_case_df["expected_results"])


def test_draws_for_special_rules_featured_five_star_draw(
    non_featured_five_star_percent_rate,
    special_rule_test_inputs_df,
    special_rule_acceptable_outputs_dict,
):
    """
    Tests that, over a number of draws (given RNG), special draws for the 'guaranteed_featured_five_star_draw' rule are producing valid output.
    """

    special_rule = "guaranteed_featured_five_star_draw"

    run_parameterized_special_rules_test(
        special_rule=special_rule,
        special_rule_test_inputs_df=special_rule_test_inputs_df,
        non_featured_five_star_percent_rate=non_featured_five_star_percent_rate,
        special_rule_acceptable_outputs_dict=special_rule_acceptable_outputs_dict,
    )


def test_draws_for_special_rules_five_star_draw(
    non_featured_five_star_percent_rate,
    special_rule_test_inputs_df,
    special_rule_acceptable_outputs_dict,
):
    """
    Tests that, over a number of draws (given RNG), special draws for the 'guaranteed_five_star_draw' rule are producing valid output.
    """

    special_rule = "guaranteed_five_star_draw"

    run_parameterized_special_rules_test(
        special_rule=special_rule,
        special_rule_test_inputs_df=special_rule_test_inputs_df,
        non_featured_five_star_percent_rate=non_featured_five_star_percent_rate,
        special_rule_acceptable_outputs_dict=special_rule_acceptable_outputs_dict,
    )


def test_draws_for_special_rules_four_star_draw(
    non_featured_five_star_percent_rate,
    special_rule_test_inputs_df,
    special_rule_acceptable_outputs_dict,
):
    """
    Tests that, over a number of draws (given RNG), special draws for the 'guaranteed_four_star_draw' rule are producing valid output.
    """

    special_rule = "guaranteed_four_star_draw"

    run_parameterized_special_rules_test(
        special_rule=special_rule,
        special_rule_test_inputs_df=special_rule_test_inputs_df,
        non_featured_five_star_percent_rate=non_featured_five_star_percent_rate,
        special_rule_acceptable_outputs_dict=special_rule_acceptable_outputs_dict,
    )


def test_draws_for_special_rules_not_desired_five_star_draw(
    non_featured_five_star_percent_rate,
    special_rule_test_inputs_df,
    special_rule_acceptable_outputs_dict,
):
    """
    Tests that, over a number of draws (given RNG), special draws for the 'guaranteed_not_desired_five_star_draw' rule are producing valid output.
    """

    special_rule = "guaranteed_not_desired_five_star_draw"

    run_parameterized_special_rules_test(
        special_rule=special_rule,
        special_rule_test_inputs_df=special_rule_test_inputs_df,
        non_featured_five_star_percent_rate=non_featured_five_star_percent_rate,
        special_rule_acceptable_outputs_dict=special_rule_acceptable_outputs_dict,
    )
