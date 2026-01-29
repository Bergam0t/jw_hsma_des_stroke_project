"""
Functional tests
"""

import pytest
from stroke_ward_model.inputs import g
from stroke_ward_model.model import Model


def run_single_model_with_config(config_overrides=None):
    """
    Run the model once (inc. any overrides) and return total patient count.
    """
    # Model settings
    g.warm_up_period = 2000
    g.sim_duration = 10000
    g.number_of_runs = 1
    g.show_trace = False
    g.master_seed = 42

    # Setting these not to 0 (otherwise will have infinite loop)
    g.ctp_unav_freq = 60
    g.ctp_unav_time = 10
    g.sdec_unav_freq = 60
    g.sdec_unav_time = 10

    # Reset all parameters we override
    # (As otherwise altered values get carried between tests)
    g.patient_inter_day = 200.0
    g.patient_inter_night = 666.666666666667
    g.number_of_nurses = 2
    g.number_of_ctp = 1
    g.sdec_beds = 5
    g.number_of_ward_beds = 1
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
    g.sdec_value = 0
    g.ctp_value = 0
    g.sdec_opening_hour = 0
    g.ctp_opening_hour = 0
    g.in_hours_start = 7
    g.ooh_start = 0

    # Apply any overrides you want to test
    if config_overrides:
        for name, value in config_overrides.items():
            setattr(g, name, value)

    # Run the model and return the number of patients that entered the system
    model = Model(run_number=1)
    model.run()
    return model.patient_counter


# Capture the baseline arrival count
@pytest.fixture(scope="module")
def baseline_arrivals() -> int:
    return run_single_model_with_config()


@pytest.mark.parametrize(
    "overrides",
    [
        {"number_of_nurses": 4},
        {"number_of_ctp": 2},
        {"sdec_beds": 10},
        {"number_of_ward_beds": 3},
        {"mean_n_consult_time": 30},
        {"mean_n_ct_time": 10},
        {"mean_n_sdec_time": 120},
        {"mean_n_i_ward_time_mrs_0": 1440 * 1.5},
        {"mean_n_i_ward_time_mrs_1": 1440 * 3.0},
        {"mean_n_i_ward_time_mrs_2": 1440 * 5.0},
        {"mean_n_i_ward_time_mrs_3": 1440 * 10.0},
        {"mean_n_i_ward_time_mrs_4": 1440 * 20.0},
        {"mean_n_i_ward_time_mrs_5": 1440 * 25.0},
        {"mean_n_ich_ward_time_mrs_0": 1440 * 1.5},
        {"mean_n_ich_ward_time_mrs_1": 1440 * 3.0},
        {"mean_n_ich_ward_time_mrs_2": 1440 * 5.0},
        {"mean_n_ich_ward_time_mrs_3": 1440 * 10.0},
        {"mean_n_ich_ward_time_mrs_4": 1440 * 20.0},
        {"mean_n_ich_ward_time_mrs_5": 1440 * 25.0},
        {"mean_n_non_stroke_ward_time": 1440 * 2},
        {"mean_n_tia_ward_time": 1440 * 2},
        {"thrombolysis_los_save": 0.5},
        {"sdec_dr_cost_min": 1.0},
        {"inpatient_bed_cost": 1000},
        {"inpatient_bed_cost_thrombolysis": 600},
        {"mean_mrs": 3},
        {"ich": 5},
        {"i": 70},
        {"tia": 50},
        {"stroke_mimic": 90},
        {"tia_admission": 5},
        {"stroke_mimic_admission": 50},
        {"sdec_value": 1},
        {"ctp_value": 1},
        {"sdec_opening_hour": 8},
        {"ctp_opening_hour": 8},
        {"sdec_unav_time": 20},
        {"sdec_unav_freq": 120},
        {"ctp_unav_time": 20},
        {"ctp_unav_freq": 120}
        
    ],
)
def test_arrivals_invariant_to_other_params(baseline_arrivals, overrides):
    """Check arrivals remains consistent when other parameters are changed."""
    arrivals = run_single_model_with_config(config_overrides=overrides)
    assert arrivals == baseline_arrivals
