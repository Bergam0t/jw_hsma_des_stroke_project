"""
Unit tests for distributions.py
"""

import numpy as np
import pytest
from sim_tools.time_dependent import nspp_simulation

from stroke_ward_model.inputs import g
from stroke_ward_model.distributions import initialise_distributions


class Dummy:
    def __init__(self, run_number=0):
        self.run_number = run_number


@pytest.mark.parametrize(
    "dist_attr, exp_mean_attr",
    [
        ("patient_inter_day_dist", "patient_inter_day"),
        ("patient_inter_night_dist", "patient_inter_night"),
        ("nurse_consult_time_dist", "mean_n_consult_time"),
        ("ct_time_dist", "mean_n_ct_time"),
        ("sdec_time_dist", "mean_n_sdec_time"),
        ("i_ward_time_mrs_0_dist", "mean_n_i_ward_time_mrs_0"),
        ("i_ward_time_mrs_1_dist", "mean_n_i_ward_time_mrs_1"),
        ("i_ward_time_mrs_2_dist", "mean_n_i_ward_time_mrs_2"),
        ("i_ward_time_mrs_3_dist", "mean_n_i_ward_time_mrs_3"),
        ("i_ward_time_mrs_4_dist", "mean_n_i_ward_time_mrs_4"),
        ("i_ward_time_mrs_5_dist", "mean_n_i_ward_time_mrs_5"),
        ("ich_ward_time_mrs_0_dist", "mean_n_ich_ward_time_mrs_0"),
        ("ich_ward_time_mrs_1_dist", "mean_n_ich_ward_time_mrs_1"),
        ("ich_ward_time_mrs_2_dist", "mean_n_ich_ward_time_mrs_2"),
        ("ich_ward_time_mrs_3_dist", "mean_n_ich_ward_time_mrs_3"),
        ("ich_ward_time_mrs_4_dist", "mean_n_ich_ward_time_mrs_4"),
        ("ich_ward_time_mrs_5_dist", "mean_n_ich_ward_time_mrs_5"),
        ("tia_ward_time_dist", "mean_n_tia_ward_time"),
        ("non_stroke_ward_time_dist", "mean_n_non_stroke_ward_time"),
        ("mrs_type_distribution", "mean_mrs"),
        ("ich_range_distribution", "ich"),
        ("i_range_distribution", "i"),
        ("tia_range_distribution", "tia"),
        ("stroke_mimic_range_distribution", "stroke_mimic"),
        ("non_stroke_range_distribution", "stroke_mimic"),
        ("tia_admission_chance_distribution", "tia_admission"),
        ("stroke_mimic_admission_chance_distribution", "stroke_mimic_admission"),
    ],
)
def test_dist_mean(dist_attr, exp_mean_attr):
    """Check that distribution mean matches the expected mean"""
    dummy = Dummy(run_number=0)
    initialise_distributions(dummy)

    dist = getattr(dummy, dist_attr)
    expected_mean = getattr(g, exp_mean_attr)

    assert dist.mean == expected_mean


@pytest.mark.parametrize(
    "dist_attr, exp_values, exp_freq",
    [
        ("onset_type_distribution", [0, 1, 2], [1, 1, 1]),
        ("diagnosis_distribution", list(range(0, 101)), [1] * 101),
        ("non_admission_distribution", list(range(0, 101)), [1] * 101),
        ("mrs_reduction_during_stay", [0, 1], [1, 1]),
        ("mrs_reduction_during_stay_thrombolysed", [0, 1, 2], [1, 1, 1]),
    ],
)
def test_discrete_empirical_parameters(dist_attr, exp_values, exp_freq):
    """Check that DiscreteEmpirical use the expected support and weights."""
    dummy = Dummy(run_number=0)
    initialise_distributions(dummy)

    dist = getattr(dummy, dist_attr)

    assert np.array_equal(dist.values, np.array(exp_values))
    assert np.array_equal(dist.freq, np.array(exp_freq))


def test_unique_seeds():
    """All distributions should have a unique random seed."""
    dummy = Dummy(run_number=0)
    initialise_distributions(dummy)

    # Collect all attributes that look like distributions by filtering to
    # those with a random_attribute, and save that seed in a list
    seeds = []
    for _, value in dummy.__dict__.items():
        if hasattr(value, "random_seed"):
            seeds.append(value.random_seed)

    # Check all seeds are unique
    assert len(seeds) == len(set(seeds)), (
        "Distributions must use unique random_seed values"
    )


def test_nspp():
    # Code modified from
    # https://sim-tools.github.io/sim-tools/01_sampling/04_time_dependent_examples.html#check-nspp-is-working-as-expected
    dummy = Dummy(run_number=0)
    initialise_distributions(dummy)

    data = getattr(dummy, "iat_dataframe")

    days = 365
    n_reps = 50
    z_tol = 0.003

    nspp_replications = nspp_simulation(
        arrival_profile=data, run_length=60 * 24 * days, n_reps=n_reps
    )
    # re-label columns
    nspp_replications.columns = data["t"].values

    ## banks data converted from arrivals per min to arrivals per hour
    data["arrival_rate"] = 1 / data["mean_iat"]
    data["expected_mean_arrivals_hr"] = data["arrival_rate"] * 60.0
    data["simulated_mean_arrivals_hr"] = nspp_replications.mean(axis=0).values / days

    data.round(6).to_csv("nspp_test_output.csv")

    for _, row in data.iterrows():
        expected = row["expected_mean_arrivals_hr"]
        simulated = row["simulated_mean_arrivals_hr"]

        np.testing.assert_allclose(
            simulated,
            expected,
            rtol=0.15,  # 15% relative tolerance
            atol=0.02,
        )
