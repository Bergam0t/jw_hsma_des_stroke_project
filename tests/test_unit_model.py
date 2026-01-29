"""
Unit tests for model.py
"""

import pandas as pd
import pytest
import simpy
from unittest.mock import patch

from stroke_ward_model.inputs import g
from stroke_ward_model.model import Model


# ----------------------------------------------------------------------------
# Model.__init__()
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "attr, expected_type, expected_value",
    [
        # SimPy environment
        ("env", (simpy.core.Environment,), None),
        # Counter attributes
        ("patient_counter", (int,), 0),
        ("sdec_freeze_counter", (int,), 0),
        ("i_patients_count", (int,), 0),
        ("ich_patients_count", (int,), 0),
        ("tia_patients_count", (int,), 0),
        ("stroke_mimic_patient_count", (int,), 0),
        ("non_stroke_patient_count", (int,), 0),
        ("additional_thrombolysis_from_ctp", (int,), 0),
        # Numeric metrics
        ("mean_q_time_nurse", (float, int), 0),
        ("max_q_time_nurse", (float, int), 0),
        ("mean_q_time_ward", (float, int), 0),
        ("max_q_time_ward", (float, int), 0),
        ("mean_los_ward", (float, int), 0),
        ("thrombolysis_savings", (float, int), 0),
        # Run number
        ("run_number", (int,), None),
        # List attributes
        ("q_for_assessment", (list,), []),
        ("sdec_occupancy", (list,), []),
        ("admission_avoidance", (list,), []),
        ("ward_occupancy", (list,), []),
        ("non_admissions", (list,), []),
        ("patient_objects", (list,), []),
        # DataFrame attributes
        ("results_df", (pd.DataFrame,), None),
        ("nurse_q_graph_df", (pd.DataFrame,), None),
        ("ward_occupancy_graph_df", (pd.DataFrame,), None),
        ("sdec_occupancy_graph_df", (pd.DataFrame,), None),
    ],
)
def test_model_default_attributes(attr, expected_type, expected_value):
    """Check each Model attribute exists and has the expected default type."""
    model = Model(run_number=1)
    value = getattr(model, attr)

    # Check type
    assert isinstance(
        value, expected_type
    ), f"{attr} should be type {expected_type}, got {type(value)}"

    # Check value if specified
    if expected_value is not None:
        assert (
            value == expected_value
        ), f"{attr} should be {expected_value}, got {value}"


def test_model_resources_initialised():
    """Check that SimPy environment and resources are properly initialised."""
    model = Model(run_number=1)

    # Check env is a SimPy environment
    assert isinstance(model.env, simpy.core.Environment)
    assert hasattr(model.env, "now")
    assert model.env.now == 0

    # Check resources exist
    assert hasattr(model, "nurse")
    assert hasattr(model, "ctp_scanner")
    assert hasattr(model, "sdec_bed")
    assert hasattr(model, "ward_bed")

    # Number of VidigiResource items equals configured number of nurses
    assert len(model.nurse.items) == g.number_of_nurses
    assert len(model.ctp_scanner.items) == g.number_of_ctp
    assert len(model.sdec_bed.items) == g.sdec_beds
    assert len(model.ward_bed.items) == g.number_of_ward_beds


def test_model_results_df_structure():
    """Check results_df has expected columns, index, and initial values."""
    model = Model(run_number=1)
    df = model.results_df

    # Check index is set to "Patient ID"
    assert df.index.name == "Patient ID"
    assert list(df.index) == [1]

    expected_schema = {
        "Q Time Nurse": "numeric",
        "Time with Nurse": "numeric",
        "Q Time Ward": "numeric",
        "Ward LOS": "numeric",
        "Time with CTP": "numeric",
        "Time with CT": "numeric",
        "Time in SDEC": "numeric",
        "CTP Status": "string",
        "SDEC Status": "string",
        "Thrombolysis": "string",
        "SDEC Occupancy": "numeric",
        "Admission Avoidance": "string",
        "SDEC Savings": "numeric",
        "MRS Type": "numeric",
        "MRS DC": "numeric",
        "MRS Change": "numeric",
        "Onset Type": "numeric",
        "Diagnosis Type": "string",
        "Thrombolysis Savings": "numeric",
        "Ward Occupancy": "numeric",
        "Arrival Time": "numeric",
        "Patient Gen 1 Status": "string",
        "Patient Gen 2 Status": "string",
    }

    # Columns and order
    expected_columns = list(expected_schema.keys())
    assert list(df.columns) == expected_columns

    # Typed defaults in first row
    row = df.loc[1]
    for col, kind in expected_schema.items():
        val = row[col]
        if kind == "numeric":
            assert isinstance(val, (int, float))
            assert val == 0 or val == 0.0
        elif kind == "string":
            assert isinstance(val, str)
            assert val == ""
        else:
            raise AssertionError(f"Unknown kind '{kind}' for column '{col}'")


def test_model_nurse_q_graph_df_structure():
    """Check nurse_q_graph_df has expected columns & initial values."""
    model = Model(run_number=1)
    df = model.nurse_q_graph_df

    expected_columns = ["Time", "Patients in Assessment Queue"]
    assert list(df.columns) == expected_columns
    assert list(df.index) == [0]
    assert df.loc[0, "Time"] == 0.0
    assert df.loc[0, "Patients in Assessment Queue"] == 0.0


def test_model_ward_occupancy_graph_df_structure():
    """Check ward_occupancy_graph_df has expected columns & initial values."""
    model = Model(run_number=1)
    df = model.ward_occupancy_graph_df

    expected_columns = ["Time", "Occupancy", "During Warm-Up"]
    assert list(df.columns) == expected_columns
    assert list(df.index) == [0]
    assert df.loc[0, "Time"] == 0.0
    assert df.loc[0, "Occupancy"] == 0.0
    assert df.loc[0, "During Warm-Up"]


def test_model_sdec_occupancy_graph_df_structure():
    """Check sdec_occupancy_graph_df has expected columns & initial values."""
    model = Model(run_number=1)
    df = model.sdec_occupancy_graph_df

    expected_columns = ["Time", "Occupancy", "During Warm-Up"]
    assert list(df.columns) == expected_columns
    assert list(df.index) == [0]
    assert df.loc[0, "Time"] == 0.0
    assert df.loc[0, "Occupancy"] == 0.0
    assert df.loc[0, "During Warm-Up"]


@pytest.mark.parametrize("run_number", [1, 5, 42, 999])
def test_model_run_number_assignment(run_number):
    """Check that the run_number parameter is correctly assigned."""
    model = Model(run_number=run_number)

    assert model.run_number == run_number


def test_model_initialise_distributions_called():
    """Check that initialise_distributions() is called during __init__."""
    # This test uses a mock to verify the method was called
    from unittest.mock import patch

    with patch.object(Model, "initialise_distributions") as mock_init:
        _ = Model(run_number=1)
        mock_init.assert_called_once()


def test_model_instances_independent_lists():
    """Check that list attributes are independent between Model instances."""
    model1 = Model(run_number=1)
    model2 = Model(run_number=2)

    # Modify model1's list
    model1.q_for_assessment.append("test")

    # Check model2's list is unaffected
    assert model2.q_for_assessment == []


def test_model_instances_independent_dataframes():
    """Check DataFrame attributes are independent between Model instances."""
    model1 = Model(run_number=1)
    model2 = Model(run_number=2)

    # Modify model1's dataframe
    model1.results_df.loc[1, "Q Time Nurse"] = 10.0

    # Check model2's dataframe is unaffected
    assert model2.results_df.loc[1, "Q Time Nurse"] == 0.0


# ----------------------------------------------------------------------------
# Test is_in_hours()
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "in_hours_start, ooh_start, time_of_day, expected",
    [
        # Normal case: in-hours is 8am-8pm (480-1200 minutes)
        (8, 20, 600, True),  # 10am - in hours
        (8, 20, 300, False),  # 5am - out of hours
        (8, 20, 1300, False),  # 9:40pm - out of hours
        (8, 20, 480, True),  # Exactly 8am - in hours (boundary)
        (8, 20, 1199, True),  # Just before 8pm - in hours
        (8, 20, 1200, False),  # Exactly 8pm - out of hours
        # Wraps over midnight: in-hours is 8pm-8am (1200-480 minutes)
        (20, 8, 1300, True),  # 9:40pm - in hours
        (20, 8, 100, True),  # 1:40am - in hours
        (20, 8, 600, False),  # 10am - out of hours
        (20, 8, 1200, True),  # Exactly 8pm - in hours (boundary)
        (20, 8, 480, False),  # Exactly 8am - out of hours
    ],
)
def test_model_is_in_hours(in_hours_start, ooh_start, time_of_day, expected):
    """Test is_in_hours() with various time ranges including midnight wrap."""
    with patch.object(g, "in_hours_start", in_hours_start), patch.object(
        g, "ooh_start", ooh_start
    ):
        model = Model(run_number=1)
        result = model.is_in_hours(time_of_day)
        assert result == expected, (
            f"is_in_hours({time_of_day}) with in_hours={in_hours_start}, "
            f"ooh={ooh_start} should be {expected}, got {result}"
        )


# ----------------------------------------------------------------------------
# Test is_out_of_hours()
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "in_hours_start, ooh_start, time_of_day, expected",
    [
        (8, 20, 600, False),  # 10am - in hours, so NOT out of hours
        (8, 20, 300, True),  # 5am - out of hours
        (8, 20, 1300, True),  # 9:40pm - out of hours
        (20, 8, 1300, False),  # 9:40pm - in hours (wraps), so NOT out of hours
        (20, 8, 600, True),  # 10am - out of hours (wraps)
    ],
)
def test_model_is_out_of_hours(
    in_hours_start, ooh_start, time_of_day, expected
):
    """Test is_out_of_hours() is inverse of is_in_hours()."""
    with patch.object(g, "in_hours_start", in_hours_start), patch.object(
        g, "ooh_start", ooh_start
    ):
        model = Model(run_number=1)
        result = model.is_out_of_hours(time_of_day)
        assert result == expected


# ----------------------------------------------------------------------------
# Test generator_patient_arrivals()
# ----------------------------------------------------------------------------


def test_model_generator_patient_arrivals():
    """Check in-hours patient generator creates at least one patient."""
    # Make the whole day 'in hours' so the condition always passes
    with (
        patch.object(g, "in_hours_start", 0),
        patch.object(g, "ooh_start", 1440),
        patch.object(g, "show_trace", False),
    ):
        # Set up model, replacing distribution with frequent arrivals
        model = Model(run_number=1)
        model.patient_inter_day_dist.sample = lambda: 10

        # Run the generator
        model.env.process(model.generator_patient_arrivals())
        model.env.run(until=100)

        # We don't care what stroke_assessment did, only that arrivals happened
        assert model.patient_counter > 0
        assert len(model.patient_objects) > 0


def test_model_generator_patient_arrivals_ooh():
    """Check out-of-hours patient generator creates at least 1 OOH patient."""
    # Make the whole day 'out of hours' so the condition always passes
    with (
        patch.object(g, "in_hours_start", 480),  # 08:00
        patch.object(g, "ooh_start", 0),  # 00:00 -> wrap so everything is OOH
        patch.object(g, "show_trace", False),
    ):
        # Set up model, replacing distribution with frequent arrivals
        model = Model(run_number=1)
        model.patient_inter_night_dist.sample = lambda: 10

        # Run the OOH generator
        model.env.process(model.generator_patient_arrivals_ooh())
        model.env.run(until=100)

        # We don't care what stroke_assessment did, only that arrivals happened
        assert model.patient_counter > 0
        assert len(model.patient_objects) > 0
        assert any(p.arrived_ooh for p in model.patient_objects)


# ----------------------------------------------------------------------------
# Test obstruct_ctp()
# ----------------------------------------------------------------------------


def test_model_obstruct_ctp():
    """CTP obstruction should set ctp_unav=True for the configured duration."""
    with (
        patch.object(g, "ctp_opening_hour", 0),
        patch.object(g, "ctp_unav_freq", 10),  # first downtime at t=10
        patch.object(g, "ctp_unav_time", 30),  # stays down for 30 minutes
        patch.object(g, "show_trace", False),
    ):
        model = Model(run_number=1)

        # Start the obstruction process
        model.env.process(model.obstruct_ctp())

        # Just before downtime starts: flag should still be False
        model.env.run(until=9)
        assert g.ctp_unav is False

        # During downtime window: flag should be True
        model.env.run(until=15)
        assert g.ctp_unav is True

        # After downtime ends (10 + 30 = 40): flag should be False again
        model.env.run(until=45)
        assert g.ctp_unav is False


# ----------------------------------------------------------------------------
# Test obstruct_sdec()
# ----------------------------------------------------------------------------


def test_model_obstruct_sdec():
    """SDEC obstruction should sdec_unav=True and increment freeze counter."""
    with (
        patch.object(g, "sdec_opening_hour", 0),
        patch.object(g, "sdec_unav_freq", 10),  # first freeze at t=10
        patch.object(g, "sdec_unav_time", 30),  # frozen until t=40
        patch.object(g, "warm_up_period", 0),  # so freezes are counted
        patch.object(g, "show_trace", False),
    ):
        model = Model(run_number=1)

        # Start obstruction process
        model.env.process(model.obstruct_sdec())

        # Just before freeze: SDEC available, no freezes counted
        model.env.run(until=9)
        assert g.sdec_unav is False
        assert model.sdec_freeze_counter == 0

        # During freeze: SDEC unavailable
        model.env.run(until=15)
        assert g.sdec_unav is True

        # After first freeze ends: SDEC available again, counter incremented
        model.env.run(until=45)
        assert g.sdec_unav is False
        assert model.sdec_freeze_counter >= 1


# ----------------------------------------------------------------------------
# Test stroke_assessment()
# ----------------------------------------------------------------------------


def test_model_stroke_assessment():
    """Test that stroke_assessment process runs to completion for a patient."""
    with (
        patch.object(g, "warm_up_period", 0),
        patch.object(g, "ctp_unav", False),
        patch.object(g, "sdec_unav", False),
        patch.object(g, "sdec_beds", 10),
    ):

        model = Model(run_number=1)

        # Create a mock patient with required attributes
        from stroke_ward_model.entities import Patient

        patient = Patient(1)

        # Start the assessment process
        model.env.process(model.stroke_assessment(patient))

        # Run simulation for sufficient time
        model.env.run(until=5000)

        # Patient should have completed journey
        assert hasattr(patient, "journey_completed")
        assert patient.journey_completed


# ----------------------------------------------------------------------------
# Test calculate_run_results()
# ----------------------------------------------------------------------------


def test_model_calculate_run_results():
    """Test that calculate_run_results processes data and calculates KPIs."""
    model = Model(run_number=1)

    # Add some dummy data to results_df (beyond the initial row)
    model.results_df.loc[2] = {
        "Q Time Nurse": 10.0,
        "Time with Nurse": 15.0,
        "Q Time Ward": 120.0,
        "Ward LOS": 2880.0,
        "Time with CTP": 0.0,
        "Time with CT": 20.0,
        "Time in SDEC": 0.0,
        "CTP Status": False,
        "SDEC Status": False,
        "Thrombolysis": False,
        "SDEC Occupancy": 2.0,
        "Admission Avoidance": False,
        "SDEC Savings": 0.0,
        "MRS Type": 2.0,
        "MRS DC": 1.0,
        "MRS Change": 1.0,
        "Onset Type": 0,
        "Diagnosis Type": "I",
        "Thrombolysis Savings": 0.0,
        "Ward Occupancy": 5.0,
        "Arrival Time": 100.0,
        "Patient Gen 1 Status": True,
        "Patient Gen 2 Status": False,
    }

    model.results_df.loc[3] = model.results_df.loc[2].copy()

    # Run calculation
    model.calculate_run_results()

    # Check that KPIs have been calculated
    assert hasattr(model, "mean_q_time_nurse")
    assert (
        model.mean_q_time_nurse == 10.0
    ), "mean_q_time_nurse should be calculated from results_df"

    assert hasattr(model, "mean_q_time_ward")
    assert (
        model.mean_q_time_ward == 2.0
    ), "mean_q_time_ward should be 120 minutes / 60 = 2 hours"

    assert hasattr(model, "mean_los_ward")
    assert (
        model.mean_los_ward == 48.0
    ), "mean_los_ward should be 2880 minutes / 60 = 48 hours"


# ----------------------------------------------------------------------------
# Test track_days()
# ----------------------------------------------------------------------------


def test_model_track_days():
    """Test that track_days process runs and yields at correct intervals."""
    with (
        patch.object(g, "sim_duration", 2880),
        patch.object(g, "show_trace", False)
    ):

        model = Model(run_number=1)

        # Start track_days process
        model.env.process(model.track_days())

        # Run for 3 days (3 * 1440 minutes)
        model.env.run(until=4320)

        # Process should complete without error
        assert model.env.now == 4320


# ----------------------------------------------------------------------------
# Test run()
# ----------------------------------------------------------------------------


def test_model_run():
    """Lightweight smoke test that Model.run() advances the environment."""
    with (
        patch.object(g, "sim_duration", 5),  # tiny run
        patch.object(g, "warm_up_period", 0),
        patch.object(g, "ctp_opening_hour", 9999),  # never obstruct
        patch.object(g, "sdec_opening_hour", 9999),  # never obstruct
        patch.object(g, "write_to_csv", False),
        patch.object(g, "gen_graph", False),
        patch.object(g, "show_trace", False),
    ):
        model = Model(run_number=1)

        # Prevent any patient arrivals by making inter-arrival times huge
        model.patient_inter_day_dist.sample = lambda: 1e9
        model.patient_inter_night_dist.sample = lambda: 1e9

        # Don’t execute heavy post-processing, just assert it was invoked
        with patch.object(model, "calculate_run_results") as mock_calc:
            model.run()

        assert model.env.now == 5
        mock_calc.assert_called_once()
