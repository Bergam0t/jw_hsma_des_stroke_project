"""
Unit tests for plots.py
"""

import pandas as pd
import plotly.graph_objects as go

from stroke_ward_model.plots import TrialPlots


class DummyTrial:
    """Simple stand-in for a Trial object with a trial_patient_df attribute."""
    def __init__(self):
        self.trial_patient_df = pd.DataFrame(
            {"sdec_los": [1.0, 2.0, 3.5, 4.0]}
        )


def test_trialplots():
    """plot_los should return a Plotly Figure with sdec_los on the x-axis."""
    # Initialise TrialPlots with a dummy trial instance
    trial = DummyTrial()
    plots = TrialPlots(trial_object=trial)

    # Call the plotting method
    fig = plots.plot_los()

    # Basic type check
    assert isinstance(fig, go.Figure)

    # Check that the x data came from the sdec_los column
    # For px.histogram this is stored in the figure's data[0].x
    assert list(fig.data[0].x) == list(trial.trial_patient_df["sdec_los"])
