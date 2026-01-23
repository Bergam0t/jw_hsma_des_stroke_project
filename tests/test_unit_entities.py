"""
Unit tests for entities.py
"""

import numpy as np
import pytest

from stroke_ward_model.entities import Patient


@pytest.mark.parametrize(
    "attr, expected_type, allowed_values, is_nan, default_value",
    [
        # Identifiers
        ("id", (int, str), None, False, 123),

        # Queue times
        ("q_time_nurse", (float, np.floating), None, True, None),
        ("q_time_ward", (float, np.floating), None, True, None),

        # Onset, MRS, diagnosis
        ("onset_type",
         (int, float, np.floating), {0, 1, 2, np.NaN}, True, None),
        ("mrs_type", (int, float, np.floating), None, True, None),
        ("mrs_discharge", (int, float, np.floating), None, True, None),
        ("diagnosis", (int, float, np.floating), None, True, None),
        ("patient_diagnosis",
         (int, float, np.floating), {0, 1, 2, 3, 4, np.NaN}, True, None),
        ("patient_diagnosis_type", (str,), {"None", None}, False, "None"),

        # Priority and admission likelihood
        ("priority", (int,), {1}, False, 1),
        ("non_admission", (int, float, np.floating), None, True, None),

        # Pathway flags
        ("advanced_ct_pathway",
         (bool, type(None)), {True, False, None}, False, None),
        ("sdec_pathway", (bool, type(None)), {True, False, None}, False, None),
        ("thrombolysis", (bool, type(None)), {True, False, None}, False, None),
        ("thrombectomy", (bool, type(None)), {True, False, None}, False, None),
        ("admission_avoidance",
         (bool, type(None)), {True, False, None}, False, None),
        ("non_admitted_tia_ns_sm",
         (bool, type(None)), {True, False, None}, False, None),

        # Lengths of stay and durations
        ("ward_los", (float, np.floating), None, True, None),
        ("ward_los_thrombolysis", (float, np.floating), None, True, None),
        ("sdec_los", (float, np.floating), None, True, None),
        ("ctp_duration", (float, np.floating), None, True, None),
        ("ct_duration", (float, np.floating), None, True, None),

        # Arrival timing
        ("arrived_ooh", (bool, type(None)), {True, False, None}, False, None),

        # Clock / event times
        ("clock_start", (float, np.floating), None, True, None),
        ("nurse_q_start_time", (float, np.floating), None, True, None),
        ("nurse_triage_start_time", (float, np.floating), None, True, None),
        ("nurse_triage_end_time", (float, np.floating), None, True, None),

        # CT / CTP timing
        ("ct_scan_start_time", (float, np.floating), None, True, None),
        ("ct_scan_end_time", (float, np.floating), None, True, None),
        ("ctp_scan_start_time", (float, np.floating), None, True, None),
        ("ctp_scan_end_time", (float, np.floating), None, True, None),

        # SDEC timings
        ("sdec_admit_time", (float, np.floating), None, True, None),
        ("sdec_discharge_time", (float, np.floating), None, True, None),

        # Ward timings
        ("ward_q_start_time", (float, np.floating), None, True, None),
        ("ward_admit_time", (float, np.floating), None, True, None),
        ("ward_discharge_time", (float, np.floating), None, True, None),
        ("exit_time", (float, np.floating), None, True, None),

        # Resource IDs
        ("nurse_attending_id", (int, float, np.floating), None, True, None),
        ("ct_scanner_id", (int, float, np.floating), None, True, None),
        ("sdec_bed_id", (int, float, np.floating), None, True, None),
        ("ward_bed_id", (int, float, np.floating), None, True, None),

        # SDEC state flags
        ("sdec_running_when_required",
         (bool, type(None)), {True, False, None}, False, None),
        ("sdec_full_when_required",
         (bool, type(None)), {True, False, None}, False, None),

        # Warm-up / journey flags
        ("generated_during_warm_up",
         (bool, type(None)), {True, False, None}, False, None),
        ("journey_completed",
         (bool,), {True, False}, False, False),
    ],
)
def test_patient_default_attributes(
    attr, expected_type, allowed_values, is_nan, default_value
):
    """Check each Patient attribute has the expected type and default value."""
    # Make a patient and get the attribute
    patient = Patient(p_id=123)
    value = getattr(patient, attr)

    # Check the type (also allow None if expected)
    assert isinstance(value, expected_type) or value is None

    # Check defaults - either should be NaN, or should be the specified default
    if is_nan:
        assert isinstance(value, (float, np.floating))
        assert np.isnan(value)
    else:
        if default_value is not None:
            assert value == default_value

    # If we have a list of allowed values, check the value is in it
    if allowed_values is not None:
        if isinstance(value, float) and np.isnan(value):
            # Handle NaN separately: make sure NaN is allowed
            assert any(isinstance(v, float) and np.isnan(v)
                       for v in allowed_values)
        else:
            assert value in allowed_values
