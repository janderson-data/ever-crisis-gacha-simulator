import pandas as pd
import numpy as np
from ever_crisis_gacha_simulator.classes.crystal_pull_session import CrystalPullSession
from joblib import Parallel, delayed
from tqdm import tqdm


class GachaSim:
    """
    Class for generating, storing, and visualizing gacha simulation data.
    """

    def __init__(
        self,
        session_criterion,
        criterion_value,
        target_weapon_type,
        banner_info,
        seed_value=None,
        starting_weapon_parts=0,
        num_simulations=100_000,
    ):

        self.metadata = {
            "session_criterion": session_criterion,
            "criterion_value": criterion_value,
            "target_weapon_type": target_weapon_type,
            "num_featured_weapons": len(banner_info["metadata"]["weapons"]),
            "seed_value": seed_value,
            "num_simulations": num_simulations,
            "starting_weapon_parts": starting_weapon_parts,
        }

    def return_pull_session_data_dict(self):
        """
        Execute a crystal pull session and return a dictionary with its results (data).

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
            session_criterion=self.metadata["session_criterion"],
            criterion_value=self.metadata["criterion_value"],
            banner_info=self.metadata["banner_info"],
            target_weapon_type=self.metadata["target_weapon_type"],
            starting_weapon_parts=self.metadata["starting_weapon_parts"],
        )

        cps.execute_pull_session()

        return cps.data

    def set_seed(self, seed_value=None):
        """
        Store a new seed value within the GachaSim object. This seed value will only be
        run through `np.random.seed()` once simulations actually begin. Running this method
        with no input will clear any seed value that is currently stored within the class
        object.

        Args:
            seed_value (int, optional): Seed value to be passed through`np.random.seed()`.
                Defaults to None.
        """
        self.metadata["seed_value"] = seed_value

    def run_simulations(self):
        """
        Executes simulations based on options currently stored in self.metadata. Simulation
        results are stored in self.simulation_data as a pandas DataFrame.
        """
        if self.metadata["seed_value"]:
            np.random.seed(self.metadata["seed_value"])

        self.simulation_data = pd.DataFrame(
            Parallel(n_jobs=-1)(
                delayed(self.return_pull_session_data_dict)()
                for _ in tqdm(range(self.metadata["num_simulations"]))
            )
        )
