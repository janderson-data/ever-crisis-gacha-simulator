import pandas as pd
import numpy as np
import seaborn as sns
from ever_crisis_gacha_simulator.classes.crystal_pull_session import CrystalPullSession
from ever_crisis_gacha_simulator.banner_info_and_stamp_cards import *
from joblib import Parallel, delayed
from tqdm import tqdm


class GachaSim:
    """
    Class representing a gacha simulation, based on input parameters.
    """
    def __init__(
            self,
            session_criterion,
            criterion_value,
            target_weapon_type,
            banner_info,
            seed_value=None,
            starting_weapon_parts=0,
            num_simulations=10_000
            ):

        self.sim_results = None

        self.metadata = {
            "session_criterion": session_criterion,
            "criterion_value": criterion_value,
            "target_weapon_type": target_weapon_type,
            "banner_info": banner_info,
            "seed_value": seed_value,
            "starting_weapon_parts": starting_weapon_parts,
            "num_simulations": num_simulations,
        }

    def set_seed(self, seed_value=None):
        """
        A method to alter the seed value that will be used for simulations.

        Using the method without entering a seed value will remove any currently-set seed value.

        Args:
            seed_value (int): A seed value. The value will be passed to `np.random.seed()` whenever
                `run_sims` is called, but not before.
        """
        self.metadata["seed_value"] = seed_value


    @staticmethod
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

    def run_sims(self, n_jobs=2):

        """
        Simulate pull sessions and store them as a pandas DataFrame in self.sim_results.

        Args:
            n_jobs (int): Number of CPU cores to utilize for simulations. This value is passed directly
                as the `n_jobs` parameter in joblib.Parallel. Passing a value of `-1` will utilize all
                of your machine's CPU cores. Default value of 2.

        """

        np.random.seed(self.metadata["seed_value"])

        kwargs = {
            "session_criterion": self.metadata["session_criterion"],
            "criterion_value": self.metadata["criterion_value"],
            "target_weapon_type": self.metadata["target_weapon_type"],
            "banner_info": self.metadata["banner_info"],
            "starting_weapon_parts": self.metadata["starting_weapon_parts"],
        }

        self.sim_results = pd.DataFrame(Parallel(n_jobs=n_jobs)(delayed(GachaSim.return_pull_session_data_dict)(**kwargs) for _ in tqdm(range(self.metadata["num_simulations"]))))

    def visualize_results(self, outcome):
        # Ensure user has already generated sim results
        if self.sim_results is None:
            print("You need to run a simulation (use the `run_sims` method) before you can visualize the results.")
            return

        # Validate outcome paramter
        ACCEPTABLE_OUTCOMES = ["targeted_weapon_parts", "num_crystals_spent", "total_stamps_earned"]

        if outcome not in ACCEPTABLE_OUTCOMES:
            print("Only acceptable outcomes for this function are `targeted_weapon_parts`, `num_crystals_spent`, and `total_stamps_earned`.")

        # Make sure user isn't visualizing the session criterion by mistake.
        BAD_VIZ_DICT = {
            "overboost": "targeted_weapon_parts",
            "crystals_spent": "num_crystals_spent",
            "stamps_earned": "total_stamps_earned",
        }

        for k, v in BAD_VIZ_DICT.items():
            if self.metadata["session_criterion"] == k and outcome == v:
                print("You've set your outcome to your session criterion, which is constant. Use a different outcome.")
                return

        # Programmatically generate title and subtitle
        if self.metadata["session_criterion"] == "overboost":
            TITLE_STRING = f"FF7 Ever Crisis: Pulling Until Overboost {self.metadata['criterion_value']} is Achieved"
        else:
            TITLE_STRING = f"FF7 Ever Crisis: Pulling Until {self.metadata['criterion_value']:,} {self.metadata['session_criterion'].replace('_', ' ').title()}"

        SUBTITLE_STRING = f"Results from {self.metadata['num_simulations']:,} Simulated Sessions"

        X_AXIS_LABEL_MAPPING = {
            "targeted_weapon_parts": "Weapon Parts for Targeted Weapon",
            "num_crystals_spent": "Number of Crystals Spent",
            "total_stamps_earned": "Total Stamps Earned",
        }

        NUM_FEATURED_WEAPONS = len(self.metadata["banner_info"]["metadata"]["weapons"])

        if self.metadata["session_criterion"] == "overboost" or outcome == "targeted_weapon_parts":
            FULL_SET_TITLE_STRING = f"{TITLE_STRING}\n{SUBTITLE_STRING}\nTarget Weapon Type: {self.metadata['target_weapon_type'].title()}\nNumber of Featured Weapons: {NUM_FEATURED_WEAPONS}"
        else:
            FULL_SET_TITLE_STRING = f"{TITLE_STRING}\n{SUBTITLE_STRING}"

        # Plotting
        plot = sns.displot(
            data=self.sim_results,
            x=outcome,
            kind="ecdf",
            stat="percent",
            complementary=True if outcome in ["targeted_weapon_parts", "stamps_earned"] else False,
        )

        plot.ax.set_title(f"{FULL_SET_TITLE_STRING}")
        plot.ax.set_xlabel(f"{X_AXIS_LABEL_MAPPING[outcome]}")
        plot.ax.set_ylabel("Outcome Probability (%)")

        return plot