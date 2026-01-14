from stroke_ward_model.inputs import g
from stroke_ward_model.trial import Trial
from pathlib import Path

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

my_trial.df_trial_results.to_parquet(
    Path(__file__).parent.joinpath("exp_results/df_trial_results_exp.parquet")
)
my_trial.trial_patient_df.to_parquet(
    Path(__file__).parent.joinpath("exp_results/df_patient_log_exp.parquet")
)
