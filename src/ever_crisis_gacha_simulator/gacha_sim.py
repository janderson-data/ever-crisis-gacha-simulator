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

    kwargs = {
        "session_criterion": session_criterion,
        "criterion_value": criterion_value,
        "target_weapon_type": target_weapon_type,
        "banner_info": banner_info,
        "starting_weapon_parts": starting_weapon_parts,
    }

    return pd.DataFrame(Parallel(n_jobs=-1)(delayed(return_pull_session_data_dict)(**kwargs) for _ in tqdm(range(num_simulations))))

if __name__=='__main__':
    simulation_output = gacha_sim(
        session_criterion="crystals_spent",
        criterion_value=51_000,
        banner_info=ZACK_SEPHIROTH_LIMIT_BREAK_BANNER,
        target_weapon_type="featured",
        starting_weapon_parts=0,
        num_simulations=100_000,
    )

    simulation_output.to_csv(r'C:\\Users\\jasre\Downloads\\test_simulation_output.csv', index=False)
