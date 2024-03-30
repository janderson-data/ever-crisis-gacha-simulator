import pandas as pd
import pytest
from decimal import getcontext
from ever_crisis_gacha_simulator.classes.crystal_pull_session import CrystalPullSession
from ever_crisis_gacha_simulator.classes.stamp_card import StampCard
from ever_crisis_gacha_simulator.banner_info_and_stamp_cards import *
from ever_crisis_gacha_simulator.constants import *


getcontext().prec = 16  # Set Decimal to continue to a max of 16 decimal places


@pytest.fixture()
def test_crystal_pull_session():
    """
    A `CrystalPullSession` object to re-use across tests for the CrystalPullSession class.
    """

    banner_info = ZACK_SEPHIROTH_LIMIT_BREAK_BANNER  # Any tests should be written with this banner in mind
    target_weapon_type = "featured"
    starting_weapon_parts = 0
    session_criterion = "crystals_spent"
    criterion_value = 90_000

    return CrystalPullSession(
        session_criterion=session_criterion,
        criterion_value=criterion_value,
        banner_info=banner_info,
        target_weapon_type=target_weapon_type,
        starting_weapon_parts=starting_weapon_parts
        )

@pytest.fixture()
def test_pre_draw_sc_ops_df():
    """
    Dataframe that will be used for all `pre_draw_stamp_card_operations` tests.
    """

    test_data_dict = {
        "input_ten_draw_stamp_values": [
            1, 5, 3, 6, 4, 2, 12, 1, 1, 1, 12,
            ],

        "expected_pre_draw_stamp_card_values": [
            0, 1, 6, 9, 3, 7, 9, 9, 10, 11, 0
            ],

        "expected_pre_draw_stamp_card_indices": [
            0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3
            ],

        "expected_post_draw_stamp_card_values": [
            1, 6, 9, 3, 7, 9, 9, 10, 11, 0, 0
            ],

        "expected_post_draw_stamp_card_indices": [
            0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 4  # Repeat of "page_ex" will be captured in test for expected rules
            ],

        "expected_rules_for_draw": [
            [], ["guaranteed_featured_five_star_draw"], [], [],
            ["guaranteed_featured_five_star_draw", "guaranteed_five_star_draw"],
            ["guaranteed_featured_five_star_draw"], ["guaranteed_featured_five_star_draw"],
            [], [], ["guaranteed_featured_five_star_draw"],
            ["guaranteed_four_star_draw", "guaranteed_five_star_draw"]
            ],
        }

    return pd.DataFrame(test_data_dict)

def assert_all_cases_pass(test_case_df, expected_col, output_col, input_col=None, print_failures_only=False):
    """Create a dataframe showing test inputs (if not obvious), expected outputs, observed outputs, and whether
    the test case (row) passed or failed, and assert that all of the result columns indicate that tests passed.

    Args:
        test_case_df (pandas.DataFrame): The dataframe containing (at least) columns of expected and observed outputs.
        expected_col (string): Name of the column containing expected output for the test case.
        output_col (string): Name of the column containing observed output for the test case.
        input_col (string): Name of the column containing test inputs (optional)
        print_failures_only (boolean): If true, function should only print out rows for test cases that failed.
    """

    if input_col:
        filtered_test_case_df = test_case_df[[input_col, expected_col, output_col]]
    else:
        filtered_test_case_df = test_case_df[[expected_col, output_col]]

    filtered_test_case_df["result"] = filtered_test_case_df.apply(
        (lambda row: "PASS" if row[expected_col] == row[output_col] else "FAIL"),
        axis=1
    )

    if print_failures_only:
        filtered_test_case_df = filtered_test_case_df.query("result == 'FAIL'")

    print(filtered_test_case_df.to_string())

    assert all(filtered_test_case_df["result"] == "PASS")

def generate_pre_draw_sc_ops_output_df(test_crystal_pull_session, test_pre_draw_sc_ops_df, column_suffix):
    """
    Provided a string of the value we want to test, return a dataframe with the relevant test information.
    """

    output_dict = {
        "output_pre_draw_stamp_card_values": [],
        "output_pre_draw_stamp_card_indices": [],
        "output_post_draw_stamp_card_values": [],
        "output_post_draw_stamp_card_indices": [],
        "output_rules_for_draw": [],
    }


    for value in test_pre_draw_sc_ops_df["input_ten_draw_stamp_values"]:
        output_dict["output_pre_draw_stamp_card_indices"].append(test_crystal_pull_session.current_stamp_card_index)
        output_dict["output_pre_draw_stamp_card_values"].append(test_crystal_pull_session.current_stamp_card.current_stamp_value)

        test_crystal_pull_session.pre_draw_stamp_card_operations(predetermined_stamp_value=value)

        output_dict["output_rules_for_draw"].append(test_crystal_pull_session.rules_for_next_ten_draw)

        test_crystal_pull_session.perform_ten_draw()  # Resets rules for next draw, and it's what always happens next anyway

        output_dict["output_post_draw_stamp_card_values"].append(test_crystal_pull_session.current_stamp_card.current_stamp_value)
        output_dict["output_post_draw_stamp_card_indices"].append(test_crystal_pull_session.current_stamp_card_index)

    for key, value in output_dict.items():
        test_pre_draw_sc_ops_df[key] = value

    filtered_df = test_pre_draw_sc_ops_df[["input_ten_draw_stamp_values"] + [col for col in test_pre_draw_sc_ops_df.columns if column_suffix in col]]

    return filtered_df

def test_determine_stamp_value_for_ten_draw(test_crystal_pull_session):
    """
    Feed a list of predetermined integers through `determine_stamp_value_for_ten_draw` to make sure
    we get the expected output for each integer.
    """

    inputs = [1, 1000, 3000, 4499, 4500,
              4501, 5501, 6501, 7990, 8000,
              8001, 8500, 9000, 9350, 9592,
              9593, 9600, 9650, 9790, 9794,
              9795, 9800, 9900, 9930, 9944,
              9945, 9955, 9965, 9990, 9999,
              10000,]

    expected_incremental_value = [
        1, 1, 1, 1, 1,
        2, 2, 2, 2, 2,
        3, 3, 3, 3, 3,
        4, 4, 4, 4, 4,
        5, 5, 5, 5, 5,
        6, 6, 6, 6, 6,
        12,]

    test_dsv_df = pd.DataFrame(
        {
            "inputs": inputs,
            "expected_incremental_value": expected_incremental_value,
        }
    )

    test_dsv_df["outputs"] = test_dsv_df.apply(
        (lambda row: test_crystal_pull_session.determine_stamp_value_for_ten_draw(predetermined_int=row["inputs"])),
        axis=1
    )

    test_dsv_df["result"] = test_dsv_df.apply(
        (lambda row: "PASS" if row["outputs"] == row["expected_incremental_value"] else "FAIL"),
        axis=1
    )

    print(test_dsv_df.to_string())

    assert all(test_dsv_df["result"] == "PASS")

def test_move_to_next_stamp_card(test_crystal_pull_session):
    """
    Test whether the pull session moves to the correct stamp card when `move_to_next_stamp_card` is called.
    """

    # This is what we would expect if a player completed six stamp cards
    expected_stamp_card_list_keys = ["page_one", "page_two", "page_three", "page_ex", "page_ex", "page_ex",]

    expected_stamp_cards = []

    for stamp_card_key in expected_stamp_card_list_keys:
        expected_stamp_cards.append(StampCard(test_crystal_pull_session.stamp_cards_list[stamp_card_key]).position_and_rule_df.to_dict())

    for _ in range(len(expected_stamp_card_list_keys)):
        test_crystal_pull_session.move_to_next_stamp_card()

    output_cards = test_crystal_pull_session.completed_stamp_cards
    test_outputs = [card.position_and_rule_df.to_dict() for card in output_cards]

    test_move_df = pd.DataFrame(
        {
            "expected": expected_stamp_cards,
            "outputs": test_outputs,
        }
    )

    assert_all_cases_pass(test_case_df=test_move_df, expected_col="expected", output_col="outputs")

def test_pre_draw_stamp_card_operations_pre_draw_stamp_card_values(test_crystal_pull_session, test_pre_draw_sc_ops_df):
    """
    Test whether stamp card VALUES BEFORE each draw are as expected
    """

    column_suffix = "pre_draw_stamp_card_values"

    test_df = generate_pre_draw_sc_ops_output_df(test_crystal_pull_session, test_pre_draw_sc_ops_df, column_suffix=column_suffix)

    assert_all_cases_pass(test_case_df=test_df, expected_col="expected_" + column_suffix, output_col="output_" + column_suffix)


def test_pre_draw_stamp_card_operations_pre_draw_stamp_card_indices(test_crystal_pull_session, test_pre_draw_sc_ops_df):
    """
    Test whether stamp card INDICES BEFORE each draw are as expected
    """

    column_suffix = "pre_draw_stamp_card_indices"

    test_df = generate_pre_draw_sc_ops_output_df(test_crystal_pull_session, test_pre_draw_sc_ops_df, column_suffix=column_suffix)

    assert_all_cases_pass(test_case_df=test_df, expected_col="expected_" + column_suffix, output_col="output_" + column_suffix)


def test_pre_draw_stamp_card_operations_post_draw_stamp_card_values(test_crystal_pull_session, test_pre_draw_sc_ops_df):
    """
    Test whether stamp card VALUES AFTER each draw are as expected
    """

    column_suffix = "post_draw_stamp_card_values"

    test_df = generate_pre_draw_sc_ops_output_df(test_crystal_pull_session, test_pre_draw_sc_ops_df, column_suffix=column_suffix)

    assert_all_cases_pass(test_case_df=test_df, expected_col="expected_" + column_suffix, output_col="output_" + column_suffix)


def test_pre_draw_stamp_card_operations_post_draw_stamp_card_indices(test_crystal_pull_session, test_pre_draw_sc_ops_df):
    """
    Test whether stamp card INDICES AFTER each draw are as expected
    """

    column_suffix = "post_draw_stamp_card_indices"

    test_df = generate_pre_draw_sc_ops_output_df(test_crystal_pull_session, test_pre_draw_sc_ops_df, column_suffix=column_suffix)

    assert_all_cases_pass(test_case_df=test_df, expected_col="expected_" + column_suffix, output_col="output_" + column_suffix)


def test_pre_draw_stamp_card_operations_rules_for_draw(test_crystal_pull_session, test_pre_draw_sc_ops_df):
    """
    Test whether the rules for the next draws are expected, given the input stamp values.
    """

    column_suffix = "rules_for_draw"

    test_df = generate_pre_draw_sc_ops_output_df(test_crystal_pull_session, test_pre_draw_sc_ops_df, column_suffix=column_suffix)

    assert_all_cases_pass(test_case_df=test_df, expected_col="expected_" + column_suffix, output_col="output_" + column_suffix)
