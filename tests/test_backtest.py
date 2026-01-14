import pandas as pd
from pathlib import Path
from stroke_ward_model.inputs import g
from stroke_ward_model.trial import Trial


def test_reproduction():
    g.show_trace = False
    g.number_of_runs = 2
    g.sim_duration = 24 * 60 * 180

    g.sdec_value = 33.3
    g.sdec_unav_freq = 1440 * (g.sdec_value / 100)
    g.sdec_unav_time = 1440 - g.sdec_unav_freq

    g.ctp_value = 33.3
    g.ctp_unav_freq = 1440 * (g.ctp_value / 100)
    g.ctp_unav_time = 1440 - g.ctp_unav_freq

    g.sdec_opening_hour = 7
    g.ctp_opening_hour = 7

    my_trial = Trial()

    # Call the run_trial method of our Trial object
    my_trial.run_trial()

    df_trial_results = my_trial.df_trial_results
    df_patient_log = my_trial.trial_patient_df

    df_trial_results.to_parquet(
        Path(__file__).parent.joinpath(
            "exp_results/df_trial_results_test_comparison.parquet"
        )
    )
    df_patient_log.to_parquet(
        Path(__file__).parent.joinpath(
            "exp_results/df_patient_log_test_comparison.parquet"
        )
    )

    # Read in previously generated results
    df_trial_results_exp = pd.read_parquet(
        Path(__file__).parent.joinpath("exp_results/df_trial_results_exp.parquet")
    )
    df_patient_log_exp = pd.read_parquet(
        Path(__file__).parent.joinpath("exp_results/df_patient_log_exp.parquet")
    )

    # Check trial-level results are identical
    pd.testing.assert_frame_equal(
        df_trial_results,
        df_trial_results_exp,
    )

    # Check patient-level results are identical
    pd.testing.assert_frame_equal(
        df_patient_log,
        df_patient_log_exp,
    )
