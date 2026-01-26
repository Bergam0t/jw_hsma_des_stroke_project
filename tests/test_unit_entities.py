"""
Unit tests for entities.py
"""

import numpy as np
import pytest

from stroke_ward_model.entities import Patient


@pytest.mark.parametrize(
    "attr, expected_type, default_kind, default_value, allowed_values",
    [
        # Identifiers
        ("id", (int, str), "value", 123, None),

        # Queue times
        ("q_time_nurse", (float, np.floating), "nan", None, None),
        ("q_time_ward", (float, np.floating), "nan", None, None),

        # Onset, MRS, diagnosis
        ("onset_type", (float, np.floating), "nan", None, {0, 1, 2}),
        ("mrs_type", (float, np.floating), "nan", None, None),
        ("mrs_discharge", (float, np.floating), "nan", None, None),
        ("diagnosis", (float, np.floating), "nan", None, None),
        ("patient_diagnosis",
         (float, np.floating), "nan", None, {0, 1, 2, 3, 4}),
        ("patient_diagnosis_type", (str,), "value", "None", {"None"}),

        # Priority and admission likelihood
        ("priority", (int,), "value", 1, {1}),
        ("non_admission", (float, np.floating), "nan", None, None),

        # Pathway flags
        ("advanced_ct_pathway", (bool,), "none", None, None),
        ("sdec_pathway", (bool,), "none", None, None),
        ("thrombolysis", (bool,), "none", None, None),
        ("thrombectomy", (bool,), "none", None, None),
        ("admission_avoidance", (bool,), "none", None, None),
        ("non_admitted_tia_ns_sm", (bool,), "none", None, None),

        # Lengths of stay and durations
        ("ward_los", (float, np.floating), "nan", None, None),
        ("ward_los_thrombolysis", (float, np.floating), "nan", None, None),
        ("sdec_los", (float, np.floating), "nan", None, None),
        ("ctp_duration", (float, np.floating), "nan", None, None),
        ("ct_duration", (float, np.floating), "nan", None, None),

        # Arrival timing
        ("arrived_ooh", (bool,), "none", None, None),

        # Clock / event times
        ("clock_start", (float, np.floating), "nan", None, None),
        ("nurse_q_start_time", (float, np.floating), "nan", None, None),
        ("nurse_triage_start_time", (float, np.floating), "nan", None, None),
        ("nurse_triage_end_time", (float, np.floating), "nan", None, None),

        # CT / CTP timing
        ("ct_scan_start_time", (float, np.floating), "nan", None, None),
        ("ct_scan_end_time", (float, np.floating), "nan", None, None),
        ("ctp_scan_start_time", (float, np.floating), "nan", None, None),
        ("ctp_scan_end_time", (float, np.floating), "nan", None, None),

        # SDEC timings
        ("sdec_admit_time", (float, np.floating), "nan", None, None),
        ("sdec_discharge_time", (float, np.floating), "nan", None, None),

        # Ward timings
        ("ward_q_start_time", (float, np.floating), "nan", None, None),
        ("ward_admit_time", (float, np.floating), "nan", None, None),
        ("ward_discharge_time", (float, np.floating), "nan", None, None),
        ("exit_time", (float, np.floating), "nan", None, None),

        # Resource IDs
        ("nurse_attending_id", (float, np.floating), "nan", None, None),
        ("ct_scanner_id", (float, np.floating), "nan", None, None),
        ("sdec_bed_id", (float, np.floating), "nan", None, None),
        ("ward_bed_id", (float, np.floating), "nan", None, None),

        # SDEC state flags
        ("sdec_running_when_required", (bool,), "none", None, None),
        ("sdec_full_when_required", (bool,), "none", None, None),

        # Warm-up / journey flags
        ("generated_during_warm_up", (bool,), "none", None, None),
        ("journey_completed", (bool,), "value", False, {True, False}),
    ],
)
def test_patient_default_attributes(
    attr, expected_type, default_kind, default_value, allowed_values
):
    """Check each Patient attribute exists and has the expected default."""
    patient = Patient(p_id=123)
    value = getattr(patient, attr)

    # Check that the attribute has the correct default state:
    # "nan" - numeric but intentionally uninitialised
    # "none" - intentionally unset
    # "value" - concrete default value
    if default_kind == "nan":
        assert isinstance(value, expected_type)
        assert np.isnan(value)

    elif default_kind == "none":
        assert value is None

    elif default_kind == "value":
        assert isinstance(value, expected_type)
        assert value == default_value

    else:
        pytest.fail(f"Unknown default_kind '{default_kind}'")

    # If a real (non-None, non-NaN) value exists, ensure it is within the
    # allowed set of values
    if allowed_values is not None and value is not None and not (
        isinstance(value, float) and np.isnan(value)
    ):
        assert value in allowed_values
