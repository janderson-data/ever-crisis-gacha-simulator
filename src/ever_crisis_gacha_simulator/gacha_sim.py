import pandas as pd
from ever_crisis_gacha_simulator.classes.crystal_pull_session import CrystalPullSession
from ever_crisis_gacha_simulator.banner_info_and_stamp_cards import *
from joblib import Parallel, delayed
from tqdm import tqdm


def return_pull_session_data_dict(
    session_criterion,
    criterion_value,
    banner_info,
    target_weapon_type,
    starting_weapon_parts,
    ):

    """
    Execute a crystal pull session and return a dictionary with its results (data).

    Args:
        session_criterion (str): One of 'crystals_spent', 'overboost', or 'stamps_earned',
            to determine the stopping criterion for a crystal pull session.
        criterion_value (int): The value at which the pull session should stop, corresponding
            with `session_criterion` (e.g., stop once 30,000 crystals have been spent).
        banner_info (dict): Banner information, including the stamp cards for pulls and other
            banner metadata.
        target_weapon_type (str): One of 'featured' or 'wishlisted'.
        starting_weapon_parts (int): The number of weapons parts the pull session should start
            with (e.g., already having weapon- or character-specific parts for the character to
            whom the targeted weapon belongs).

    Returns:
        dict: Dictionary containing the results of a simulated crystal pull session.
            targeted_weapon_parts: Number of weapon parts pulled for the targeted weapon.
                Divide by 200, subtract 1, and round down to get the weapon's overboost
                level (e.g.: (525 weapon parts / 200) = 2.625;  2.625 - 1 = 1.625; OB1)
            total_stamps_earned: Number of stamps earned during the pull session.
                Divide by 12 and round down to get the number of stamp cards completed.
            num_crystals_spent: The number of crystals spent during the pull session. This
                will always be a multiple of 3,000, as the simulator does not support
                single pulls, which cost 300.
            targeted_five_stars_drawn: The number of times that the targeted weapon was
                drawn at a 5* level.
            targeted_four_stars_draw: The number of times that the targeted weapon was
                drawn at a 4* level.
            targeted_three_stars_drawn: The number of times that the targeted weapon was
                drawn at a 3* level.
            nontargeted_featured_five_stars_drawn: The number of times that a featured,
                nontargeted weapon was drawn at a 5* level. NOTE: This value is only
                trustworthy when target_weapon_type == 'featured'!
            nontargeted_featured_four_stars_drawn: The number of times that a featured,
                nontargeted weapon was drawn at a 4* level.
            nontargeted_featured_three_starts_drawn: The number of times that a featured,
                nontargeted weapon was drawn at a 4* level.
            nontargeted_five_stars_drawn: The number of times that a nontargeted weapon
                was drawn at a 5* level. This value EXCLUDES featured weapons. NOTE: This
                value is only trustworthy when target_weapon_type == 'featured'!
            nontargeted_four_stars_drawn: The number of times that a nontargeted weapon
                was drawn at a 4* level. This value EXCLUDES featured weapons.
            nontargeted_three_stars_drawn: The number of times that a nontargeted weapon
                was drawn at a 3* level. This value EXCLUDES featured weapons.
    """

    cps = CrystalPullSession(
        session_criterion=session_criterion,
        criterion_value=criterion_value,
        banner_info=banner_info,
        target_weapon_type=target_weapon_type,
        starting_weapon_parts=starting_weapon_parts,
    )

    cps.execute_pull_session()

    return cps.data

def gacha_sim(session_criterion, criterion_value, target_weapon_type, banner_info, starting_weapon_parts=0, num_simulations=100_000):

    """
    Simulate a number of pull sessions  given input paramters and return a pandas DataFrame of the results.

    Args:
        session_criterion (str): One of 'crystals_spent', 'overboost', or 'stamps_earned',
            to determine the stopping criterion for a crystal pull session.
        criterion_value (int): The value at which the pull session should stop, corresponding
            with `session_criterion` (e.g., stop once 30,000 crystals have been spent).
        banner_info (dict): Banner information, including the stamp cards for pulls and other
            banner metadata.
        target_weapon_type (str): One of 'featured' or 'wishlisted'.
        starting_weapon_parts (int): The number of weapons parts the pull session should start
            with (e.g., already having weapon- or character-specific parts for the character to
            whom the targeted weapon belongs).
        num_simulations (int): The number of times to repeat the simulation. Each simulation's
            results will have a corresponding row in the returned dataframe.

    Returns:
        pandas.DataFrame: A dataframe containing simulation results.
    """

    kwargs = {
        "session_criterion": session_criterion,
        "criterion_value": criterion_value,
        "target_weapon_type": target_weapon_type,
        "banner_info": banner_info,
        "starting_weapon_parts": starting_weapon_parts,
    }

    return pd.DataFrame(Parallel(n_jobs=-1)(delayed(return_pull_session_data_dict)(**kwargs) for _ in tqdm(range(num_simulations))))
