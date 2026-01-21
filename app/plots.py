"""
Create occupancy plot.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_occupancy(
    occupancy_df,
    total_sim_duration_days,
    warm_up_duration_days,
    plot_confidence_intervals=False,
):
    """
    Plot occupancy over time, optionally with confidence bands.

    Parameters
    ----------
    occ_df : pd.DataFrame
        Data frame with columns "Time" (minutes), "Occupancy", and "run".
    total_sim_days : float
        Total simulation duration in days.
    warm_up_days : float
        Warm-up duration in days; shown as a vertical line.
    plot_confidence_intervals : bool, optional
        If True, plot median and quantile bands across runs.
        If False, plot individual runs plus mean and rolling mean.

    Returns
    -------
    plotly.graph_objects.Figure
        Plotly figure showing occupancy trajectories.
    """
    # Convert from minutes to days
    occupancy_df["Days"] = occupancy_df["Time"] / 60 / 24

    # Define regular grid
    grid_days = np.arange(
        0,
        total_sim_duration_days,
        1 / 24,  # hourly
    )

    # Resample each run to the common grid (step-wise, ffill)
    resampled = []
    for run, g in occupancy_df.sort_values("Days").groupby("run"):
        g = g.set_index("Days")[["Occupancy"]]
        g = g.reindex(grid_days, method="ffill")
        g["run"] = run
        g = g.reset_index(names="Days")
        resampled.append(g)

    grid_df = pd.concat(resampled, ignore_index=True)

    # Mean occupancy across runs on the grid
    mean_df = grid_df.groupby("Days", as_index=False)["Occupancy"].mean()

    if plot_confidence_intervals:
        # Summary quantiles across runs at each time point
        summary_df = (
            grid_df.groupby("Days")["Occupancy"]
            .agg(
                min="min",
                p10=lambda x: x.quantile(0.1),
                p25=lambda x: x.quantile(0.25),
                median="median",
                p75=lambda x: x.quantile(0.75),
                p90=lambda x: x.quantile(0.9),
                max="max",
            )
            .reset_index()
        )

        occupancy_fig = go.Figure()

        # Min-max band (lightest)
        occupancy_fig.add_trace(
            go.Scatter(
                x=summary_df["Days"],
                y=summary_df["max"],
                mode="lines",
                line={"width": 0},
                line_shape="hv",
                showlegend=False,
            )
        )

        occupancy_fig.add_trace(
            go.Scatter(
                x=summary_df["Days"],
                y=summary_df["min"],
                mode="lines",
                line={"width": 0},
                line_shape="hv",
                fill="tonexty",
                name="Min–Max",
                fillcolor="rgba(0, 100, 200, 0.15)",
            )
        )

        # 10-90% band
        occupancy_fig.add_trace(
            go.Scatter(
                x=summary_df["Days"],
                y=summary_df["p90"],
                mode="lines",
                line={"width": 0},
                line_shape="hv",
                showlegend=False,
            )
        )

        occupancy_fig.add_trace(
            go.Scatter(
                x=summary_df["Days"],
                y=summary_df["p10"],
                mode="lines",
                line={"width": 0},
                line_shape="hv",
                fill="tonexty",
                name="10–90%",
                fillcolor="rgba(0, 100, 200, 0.35)",
            )
        )

        # 25=75% band (darkest)
        occupancy_fig.add_trace(
            go.Scatter(
                x=summary_df["Days"],
                y=summary_df["p75"],
                mode="lines",
                line={"width": 0},
                line_shape="hv",
                showlegend=False,
            )
        )

        occupancy_fig.add_trace(
            go.Scatter(
                x=summary_df["Days"],
                y=summary_df["p25"],
                mode="lines",
                line={"width": 0},
                line_shape="hv",
                fill="tonexty",
                name="25–75%",
                fillcolor="rgba(0, 100, 200, 0.6)",
            )
        )

        # Median line
        occupancy_fig.add_trace(
            go.Scatter(
                x=summary_df["Days"],
                y=summary_df["median"],
                mode="lines",
                line_shape="hv",
                name="Median",
                line={"width": 1.5, "color": "black"},
            )
        )

        occupancy_fig.update_layout(
            xaxis_title="Days",
            yaxis_title="Occupancy",
        )

    else:
        # Rolling mean of mean occupancy (7-day window)
        mean_df["rolling_mean_7"] = (
            mean_df["Occupancy"].rolling(window=7, center=True).mean()
        )

        # Create a line plot with one line per run
        occupancy_fig = px.line(
            occupancy_df, x="Days", y="Occupancy", color="run"
        )
        occupancy_fig.update_traces(opacity=0.3)

        # Add mean line across runs
        occupancy_fig.add_scatter(
            x=mean_df["Days"],
            y=mean_df["Occupancy"],
            mode="lines",
            name="Mean across runs",
            line={"width": 2, "color": "black"},
        )

        # Add rolling mean line
        occupancy_fig.add_scatter(
            x=mean_df["Days"],
            y=mean_df["rolling_mean_7"],
            mode="lines",
            name="7-day rolling mean",
            line={"width": 1, "color": "green"},
        )

    # Mark warm-up period end
    occupancy_fig.add_vline(
        x=warm_up_duration_days,
        line_width=3,
        line_dash="dash",
        line_color="red",
    )

    return occupancy_fig
