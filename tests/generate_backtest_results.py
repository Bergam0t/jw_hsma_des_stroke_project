from stroke_ward_model.inputs import g
from stroke_ward_model.trial import Trial
from pathlib import Path

g.master_seed = 42
g.show_trace = False
g.number_of_runs = 2
g.sim_duration = 24 * 60 * 180
g.warm_up_period = g.sim_duration / 5

g.patient_inter_day = 200.0
g.patient_inter_night = 666.666666666667

g.sdec_opening_hour = 7
g.ctp_opening_hour = 7

g.sdec_value = 33.3
g.sdec_unav_freq = 1440 * (g.sdec_value / 100)
g.sdec_unav_time = 1440 - g.sdec_unav_freq

g.ctp_value = 33.3
g.ctp_unav_freq = 1440 * (g.ctp_value / 100)
g.ctp_unav_time = 1440 - g.ctp_unav_freq

g.in_hours_start = 7
g.ooh_start = 0

# Setting of relative frequencies of onsets

g.in_hours_known_onset = 1.0 / 3.0
g.in_hours_unknown_onset_inside_ctp = 1.0 / 3.0
g.in_hours_unknown_onset_outside_ctp = 1.0 / 3.0

g.out_of_hours_known_onset = 1.0 / 3.0
g.out_of_hours_unknown_onset_inside_ctp = 1.0 / 3.0
g.out_of_hours_unknown_onset_outside_ctp = 1.0 / 3.0

g.number_of_nurses = 2
g.number_of_ctp = 1
g.sdec_beds = 5
g.number_of_ward_beds = 49

g.mean_n_consult_time = 60
g.mean_n_ct_time = 20
g.mean_n_sdec_time = 240

g.mean_n_i_ward_time_mrs_0 = 1440 * 2.88
g.mean_n_i_ward_time_mrs_1 = 1440 * 4.54
g.mean_n_i_ward_time_mrs_2 = 1440 * 7.4
g.mean_n_i_ward_time_mrs_3 = 1440 * 14.14
g.mean_n_i_ward_time_mrs_4 = 1440 * 26.06
g.mean_n_i_ward_time_mrs_5 = 1440 * 29.7

g.mean_n_ich_ward_time_mrs_0 = 1440 * 2.62
g.mean_n_ich_ward_time_mrs_1 = 1440 * 7.03
g.mean_n_ich_ward_time_mrs_2 = 1440 * 12.15
g.mean_n_ich_ward_time_mrs_3 = 1440 * 18.91
g.mean_n_ich_ward_time_mrs_4 = 1440 * 32.45
g.mean_n_ich_ward_time_mrs_5 = 1440 * 41.83

# Set parameters for mild (TIA) and non-stroke stays
g.mean_n_non_stroke_ward_time = 1440 * 3  # 4320
g.mean_n_tia_ward_time = 1440 * 1

g.thrombolysis_los_save = 0.75

g.sdec_dr_cost_min = 0.50

g.inpatient_bed_cost = 876
g.inpatient_bed_cost_thrombolysis = 528.17

g.mean_mrs = 2

g.ich = 10
g.i = 60
g.tia = 70
g.stroke_mimic = 80

g.tia_admission = 10
g.stroke_mimic_admission = 30

my_trial = Trial()

# Call the run_trial method of our Trial object
my_trial.run_trial()

my_trial.df_trial_results.to_parquet(
    Path(__file__).parent.joinpath("exp_results/df_trial_results_exp.parquet")
)
my_trial.trial_patient_df.to_parquet(
    Path(__file__).parent.joinpath("exp_results/df_patient_log_exp.parquet")
)
