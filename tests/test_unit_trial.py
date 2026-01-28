"""
Unit tests for trial.py
"""

import pandas as pd
import pytest
from unittest.mock import Mock, patch

from stroke_ward_model.trial import Trial


# ----------------------------------------------------------------------------
# Trial.__init__()
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "attr, expected_type, expected_value",
    [
        ("df_trial_results", (pd.DataFrame,), None),
        ("ward_occupancy_audits", (list,), []),
        ("ward_occupancy_df", (pd.DataFrame,), None),
        ("sdec_occupancy_audits", (list,), []),
        ("sdec_occupancy_df", (pd.DataFrame,), None),
        ("model_objects", (list,), []),
        ("trial_patient_dataframes", (list,), []),
        ("trial_patient_df", (pd.DataFrame,), None),
    ],
)
def test_trial_default_attributes(attr, expected_type, expected_value):
    """Check each Trial attribute exists and has the expected default."""
    value = getattr(Trial(), attr)

    assert isinstance(value, expected_type)

    if expected_value is not None:
        assert value == expected_value


def test_trial_df_trial_results_structure():
    """Check df_trial_results has expected columns and initial values."""
    df = Trial().df_trial_results

    # Index
    assert list(df.index) == [0]

    # Columns and order
    expected_columns = [
        "Mean Q Time Nurse (Mins)",
        "Max Q Time Nurse (Mins)",
        "Number of Admissions Avoided In Run",
        "Mean Q Time Ward (Hour)",
        "Max Q Time Ward (Hour)",
        "Mean Occupancy",
        "Number of Admission Delays",
        "Mean Length of Stay Ward (Hours)",
        "Financial Savings of Admissions Avoidance (£)",
        "SDEC Medical Staff Cost (£)",
        "SDEC Savings (£)",
        "Thrombolysis Savings (£)",
        "Total Savings",
        "Mean MRS Change",
        "Mean Number of Patients Assessed",
        "Number of Intracranial Haemhorrhage patients",
        "Number of Ischaemic Stroke patients",
        "Number of TIA patients",
        "Number of Stroke Mimic patients",
        "Number of Non-Stroke patients",
        "Mean Additional Thrombolysed Patients From CTP Running",
    ]
    assert list(df.columns) == expected_columns

    # All initial values should be 0.0
    assert (df.iloc[0] == 0.0).all()


# ----------------------------------------------------------------------------
# Trial.run_trial()
# ----------------------------------------------------------------------------

# Helper functions and fixtures


def create_mock_model():
    """Create a mock Model."""
    mock_model = Mock()

    # Summary metrics
    mock_model.mean_q_time_nurse = 5.2
    mock_model.max_q_time_nurse = 15.3
    mock_model.number_of_admissions_avoided = 3.0
    mock_model.mean_q_time_ward = 2.1
    mock_model.max_q_time_ward = 8.5
    mock_model.mean_ward_occupancy = 0.65
    mock_model.admission_delays = 2.0
    mock_model.mean_los_ward = 24.5
    mock_model.sdec_financial_savings = 5000.0
    mock_model.medical_staff_cost = 2000.0
    mock_model.savings_sdec = 3000.0
    mock_model.thrombolysis_savings = 1500.0
    mock_model.total_savings = 9500.0
    mock_model.mean_mrs_change = 0.45
    mock_model.patient_counter = 50.0
    mock_model.ich_patients_count = 10.0
    mock_model.i_patients_count = 25.0
    mock_model.tia_patients_count = 10.0
    mock_model.stroke_mimic_patient_count = 3.0
    mock_model.non_stroke_patient_count = 2.0
    mock_model.additional_thrombolysis_from_ctp = 2.0

    # Patient objects
    mock_model.patient_objects = [Mock(id=i) for i in range(5)]

    # Occupancy DataFrames
    mock_model.ward_occupancy_graph_df = pd.DataFrame(
        {"time": [0, 1, 2], "occupancy": [10, 15, 12]}
    )
    mock_model.sdec_occupancy_graph_df = pd.DataFrame(
        {"time": [0, 1, 2], "occupancy": [5, 8, 6]}
    )

    return mock_model


def setup_mock_models(mock_model_class, num_runs):
    """
    Create multiple fake Models and configure them for the test.

    Creates `num_runs` separate mock Model instances and tells the mocked
    Model class to return a different one each time Model() is called. This is
    via side_effect:
    - Without side_effect, every call to Model() returns the same mock object.
    - With side_effect each call returns the next item in the list.
    """
    # Create the specified number of model instances
    mock_models = [create_mock_model() for _ in range(num_runs)]
    # Tell the mock Model class: next time someone calls Model(),
    # return the next item from this list
    mock_model_class.side_effect = mock_models
    return mock_models


@pytest.fixture
def mock_setup():
    """Setup mock Model and g before importing Trial."""
    with (
        patch("stroke_ward_model.trial.Model") as mock_model_class,
        patch("stroke_ward_model.trial.g") as mock_g,
    ):
        # When run_trial(), it will get our mock instead when calls Model(),
        # and will get our mock's run() when call my_model.run()
        from stroke_ward_model.trial import Trial

        yield mock_g, mock_model_class, Trial


def _run_trial_test_setup(mock_setup, num_runs, extra_config=None):
    """Runs trial with mocks + specific param + returns results for testing."""
    # Get mock g, mock Model, and the Trial class
    mock_g, mock_model_class, Trial = mock_setup

    # Set parameters for the trial
    mock_g.number_of_runs = num_runs
    mock_g.write_to_csv = False

    # Additional parameters
    if extra_config:
        for key, value in extra_config.items():
            setattr(mock_g, key, value)

    # Setup mock Model
    mock_models = setup_mock_models(mock_model_class, num_runs)

    # Create instance of Trial and call run_trial() method
    trial = Trial()
    trial.run_trial()

    return trial, mock_models, mock_g


# Tests


def test_run_trial_creates_models_and_calls_run(mock_setup):
    """Models created for each run and run() called."""
    trial, mock_models, _ = _run_trial_test_setup(mock_setup, num_runs=3)

    # Verify that three models end up in the trial.model_objects list
    assert len(trial.model_objects) == 3

    # Verify that .run() was called once for each mock model
    for mock_model in mock_models:
        mock_model.run.assert_called_once()


def test_run_trial_df_trial_results(mock_setup):
    """Results aggregated into df_trial_results with correct values."""
    trial, _, _ = _run_trial_test_setup(mock_setup, num_runs=2)

    # Verify structure
    assert len(trial.df_trial_results) == 2
    assert list(trial.df_trial_results.index) == [0, 1]

    # Verify values from models are stored
    assert trial.df_trial_results.iloc[0]["Mean Q Time Nurse (Mins)"] == 5.2
    assert trial.df_trial_results.iloc[1]["Total Savings"] == 9500.0


def test_run_trial_patient_data(mock_setup):
    """Patient data collected and concatenated with run column."""
    trial, _, _ = _run_trial_test_setup(mock_setup, num_runs=2)

    # Individual dataframes have correct run numbers
    assert len(trial.trial_patient_dataframes) == 2
    assert all(trial.trial_patient_dataframes[0]["run"] == 1)
    assert all(trial.trial_patient_dataframes[1]["run"] == 2)

    # Aggregated dataframe contains all runs
    assert not trial.trial_patient_df.empty
    assert set(trial.trial_patient_df["run"].unique()) == {1, 2}


def test_run_trial_occupancy(mock_setup):
    """Ward and SDEC occupancy data collected with run column added."""
    trial, _, _ = _run_trial_test_setup(mock_setup, num_runs=2)

    # Ward occupancy
    assert len(trial.ward_occupancy_audits) == 2
    assert all(trial.ward_occupancy_audits[0]["run"] == 1)
    assert not trial.ward_occupancy_df.empty

    # SDEC occupancy
    assert len(trial.sdec_occupancy_audits) == 2
    assert all(trial.sdec_occupancy_audits[1]["run"] == 2)
    assert not trial.sdec_occupancy_df.empty


def test_run_trial_updates_global_state_dictionaries(mock_setup):
    """Mean/max values stored in g class dict keyed by trial counter."""
    _, _, mock_g = _run_trial_test_setup(
        mock_setup,
        num_runs=1,
        extra_config={
            "trials_run_counter": 1,
            "trial_mean_q_time_nurse": {},
            "trial_max_q_time_nurse": {},
            "trial_mean_occupancy": {},
        },
    )

    # Verify that run_trial() stores trial-level statistics in the global g
    assert 1 in mock_g.trial_mean_q_time_nurse
    assert isinstance(mock_g.trial_mean_q_time_nurse[1], float)


def test_run_trial_respects_csv_export_flag(mock_setup):
    """CSV export respects g.write_to_csv flag."""
    mock_g, mock_model_class, Trial = mock_setup
    mock_g.number_of_runs = 1
    mock_g.write_to_csv = False

    setup_mock_models(mock_model_class, 1)
    trial = Trial()

    # Check that it did not try to call write_to_csv() when g set that as False
    with patch.object(trial.df_trial_results, "to_csv") as mock_to_csv:
        trial.run_trial()
        mock_to_csv.assert_not_called()


def test_run_trial_exports_csv_with_correct_filename(mock_setup):
    """CSV filename includes trial counter when exported."""
    mock_g, mock_model_class, Trial = mock_setup
    mock_g.number_of_runs = 1
    mock_g.trials_run_counter = 3
    mock_g.write_to_csv = True

    setup_mock_models(mock_model_class, 1)
    trial = Trial()

    # Verify that it does write to CSV with correct filename when True
    with patch.object(trial.df_trial_results, "to_csv") as mock_to_csv:
        trial.run_trial()
        mock_to_csv.assert_called_once()
        filename = mock_to_csv.call_args[0][0]
        assert "trial 3" in filename


def test_run_trial_creates_trial_info_string(mock_setup):
    """Verify trial.trial_info string is created with all config details."""
    trial, _, _ = _run_trial_test_setup(
        mock_setup,
        num_runs=1,
        extra_config={
            "trials_run_counter": 2,
            "therapy_sdec": True,
            "sdec_value": 80,
            "ctp_value": 50,
        },
    )

    assert trial.trial_info is not None
    assert "Trial 2" in trial.trial_info
    assert "SDEC Therapy = True" in trial.trial_info
    assert "SDEC Open % = 80" in trial.trial_info
    assert "CTP Open % = 50" in trial.trial_info
