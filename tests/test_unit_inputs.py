"""
Unit tests for inputs.py
"""

import numpy as np
import pytest

from stroke_ward_model.inputs import g


@pytest.mark.parametrize(
    "attr, expected_type, expected_value, allowed_values",
    [
        # Simulation runtime
        ("sim_duration", (int,), 525600, None),
        ("number_of_runs", (int,), 10, None),
        ("warm_up_period", (float, int, np.floating), g.sim_duration / 5, None),

        # Patient interarrival times
        ("patient_inter_day", (float, np.floating), 200.0, None),
        ("patient_inter_night", (float, np.floating), 666.666666666667, None),

        # Capacities
        ("number_of_nurses", (int,), 2, None),
        ("number_of_ctp", (int,), 1, None),
        ("sdec_beds", (int,), 5, None),
        ("number_of_ward_beds", (int,), 1, None),

        # Process times
        ("mean_n_consult_time", (int,), 60, None),
        ("mean_n_ct_time", (int,), 20, None),
        ("mean_n_sdec_time", (int,), 240, None),

        # Ischaemic LOS by MRS
        ("mean_n_i_ward_time_mrs_0", (float, np.floating), 1440 * 2.88, None),
        ("mean_n_i_ward_time_mrs_1", (float, np.floating), 1440 * 4.54, None),
        ("mean_n_i_ward_time_mrs_2", (float, np.floating), 1440 * 7.4, None),
        ("mean_n_i_ward_time_mrs_3", (float, np.floating), 1440 * 14.14, None),
        ("mean_n_i_ward_time_mrs_4", (float, np.floating), 1440 * 26.06, None),
        ("mean_n_i_ward_time_mrs_5", (float, np.floating), 1440 * 29.7, None),

        # ICH LOS by MRS
        ("mean_n_ich_ward_time_mrs_0",
         (float, np.floating), 1440 * 2.62, None),
        ("mean_n_ich_ward_time_mrs_1",
         (float, np.floating), 1440 * 7.03, None),
        ("mean_n_ich_ward_time_mrs_2",
         (float, np.floating), 1440 * 12.15, None),
        ("mean_n_ich_ward_time_mrs_3",
         (float, np.floating), 1440 * 18.91, None),
        ("mean_n_ich_ward_time_mrs_4",
         (float, np.floating), 1440 * 32.45, None),
        ("mean_n_ich_ward_time_mrs_5",
         (float, np.floating), 1440 * 41.83, None),

        # Other LOS
        ("mean_n_non_stroke_ward_time", (int,), 1440 * 3, None),
        ("mean_n_tia_ward_time", (int,), 1440 * 1, None),
        ("thrombolysis_los_save", (float, np.floating), 0.75, None),

        # Diagnosis mix and MRS
        ("mean_mrs", (int,), 2, None),
        ("ich", (int,), 10, None),
        ("i", (int,), 60, None),
        ("tia", (int,), 70, None),
        ("stroke_mimic", (int,), 80, None),
        ("tia_admission", (int,), 10, None),
        ("stroke_mimic_admission", (int,), 30, None),

        # Operational unavailability parameters
        ("sdec_unav_time", (int,), 0, None),
        ("sdec_unav_freq", (int,), 0, None),
        ("ctp_unav_time", (int,), 0, None),
        ("ctp_unav_freq", (int,), 0, None),

        # User-settable value placeholders
        ("sdec_value", (int,), 0, None),
        ("ctp_value", (int,), 0, None),
        ("sdec_opening_hour", (int,), 0, None),
        ("ctp_opening_hour", (int,), 0, None),
        ("in_hours_start", (int,), 7, None),
        ("ooh_start", (int,), 0, None),

        # Boolean runtime flags
        ("sdec_unav", (bool,), False, {True, False}),
        ("ctp_unav", (bool,), False, {True, False}),
        ("write_to_csv", (bool,), False, {True, False}),
        ("gen_graph", (bool,), False, {True, False}),
        ("therapy_sdec", (bool,), False, {True, False}),
        ("patient_arrival_gen_1", (bool,), False, {True, False}),
        ("patient_arrival_gen_2", (bool,), False, {True, False}),
        ("show_trace", (bool,), False, {True, False}),

        # Trace config
        ("tracked_cases", (list,), list(range(1, 1500)), None),
        ("trace_config", (dict,), {"tracked": list(range(1, 1500))}, None),

        # Seeds and counters
        ("trials_run_counter", (int,), 1, None),
        ("master_seed", (int,), 42, None),
    ],
)
def test_g_default_attributes(
    attr, expected_type, expected_value, allowed_values
):
    """Check each g attribute exists and has the expected default."""
    value = getattr(g, attr)

    assert isinstance(value, expected_type)
    assert value == expected_value

    # If an allowed_values set is provided, ensure value is in it
    if allowed_values is not None:
        assert value in allowed_values
