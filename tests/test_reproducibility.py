"""
Check that seeds are working as expected
"""

import pandas as pd
from stroke_ward_model.inputs import g
from stroke_ward_model.trial import Trial


def assert_frame_not_equal(*args, **kwargs):
    try:
        pd.testing.assert_frame_equal(*args, **kwargs)
    except AssertionError:
        # frames are not equal
        pass
    else:
        # frames are equal
        raise AssertionError


def _configure_for_trial():
    g.show_trace = False

    g.sdec_value = 33.3
    g.sdec_unav_freq = 1440 * (g.sdec_value / 100)
    g.sdec_unav_time = 1440 - g.sdec_unav_freq

    g.ctp_value = 33.3
    g.ctp_unav_freq = 1440 * (g.ctp_value / 100)
    g.ctp_unav_time = 1440 - g.ctp_unav_freq

    g.sdec_opening_hour = 7
    g.ctp_opening_hour = 7

    g.number_of_runs = 2
    g.sim_duration = 24 * 60 * 90
    g.master_seed = 5


def test_reproduction():
    _configure_for_trial()

    my_trial = Trial()
    my_trial.run_trial()
    df_trial_results_1 = my_trial.df_trial_results
    df_patient_log_1 = my_trial.trial_patient_df

    _configure_for_trial()

    my_trial = Trial()
    my_trial.run_trial()
    df_trial_results_2 = my_trial.df_trial_results
    df_patient_log_2 = my_trial.trial_patient_df

    # Check trial-level results are identical
    pd.testing.assert_frame_equal(
        df_trial_results_1,
        df_trial_results_2,
    )

    # Check patient-level results are identical
    pd.testing.assert_frame_equal(
        df_patient_log_1,
        df_patient_log_2,
    )


def test_different_seed_different_results():
    _configure_for_trial()

    my_trial = Trial()
    my_trial.run_trial()
    df_trial_results_1 = my_trial.df_trial_results
    df_patient_log_1 = my_trial.trial_patient_df

    _configure_for_trial()

    # Change seed
    g.master_seed = 134

    my_trial = Trial()
    my_trial.run_trial()
    df_trial_results_2 = my_trial.df_trial_results
    df_patient_log_2 = my_trial.trial_patient_df

    # Check trial-level results are identical
    assert_frame_not_equal(
        df_trial_results_1,
        df_trial_results_2,
    )

    # Check patient-level results are identical
    assert_frame_not_equal(
        df_patient_log_1,
        df_patient_log_2,
    )
