import plotly.express as px
import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def plot_occupancy(
    occupancy_df,
    total_sim_duration_days,
    warm_up_duration_days,
    plot_confidence_intervals=False,
    lower_ci=0.1,
    upper_ci=0.9,
):
    occupancy_df["Days"] = occupancy_df["Time"] / 60 / 24

    # Define regular grid
    grid_days = np.arange(
        0,
        total_sim_duration_days,
        1 / 24,  # hourly
    )

    resampled = []

    for run, g in occupancy_df.sort_values("Days").groupby("run"):
        g = g.set_index("Days")[["Occupancy"]]
        g = g.reindex(grid_days, method="ffill")
        g["run"] = run
        g = g.reset_index(names="Days")
        resampled.append(g)

    grid_df = pd.concat(resampled, ignore_index=True)

    mean_df = grid_df.groupby("Days", as_index=False)["Occupancy"].mean()

    if plot_confidence_intervals:
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

        occupancy_fig.add_trace(
            go.Scatter(
                x=summary_df["Days"],
                y=summary_df["max"],
                mode="lines",
                line=dict(width=0),
                line_shape="hv",
                showlegend=False,
            )
        )

        occupancy_fig.add_trace(
            go.Scatter(
                x=summary_df["Days"],
                y=summary_df["min"],
                mode="lines",
                line=dict(width=0),
                line_shape="hv",
                fill="tonexty",
                name="Min–Max",
                fillcolor="rgba(0, 100, 200, 0.15)",
            )
        )

        # --- 10–90% band ---
        occupancy_fig.add_trace(
            go.Scatter(
                x=summary_df["Days"],
                y=summary_df["p90"],
                mode="lines",
                line=dict(width=0),
                line_shape="hv",
                showlegend=False,
            )
        )

        occupancy_fig.add_trace(
            go.Scatter(
                x=summary_df["Days"],
                y=summary_df["p10"],
                mode="lines",
                line=dict(width=0),
                line_shape="hv",
                fill="tonexty",
                name="10–90%",
                fillcolor="rgba(0, 100, 200, 0.35)",
            )
        )

        # --- 25–75% band (darkest) ---
        occupancy_fig.add_trace(
            go.Scatter(
                x=summary_df["Days"],
                y=summary_df["p75"],
                mode="lines",
                line=dict(width=0),
                line_shape="hv",
                showlegend=False,
            )
        )

        occupancy_fig.add_trace(
            go.Scatter(
                x=summary_df["Days"],
                y=summary_df["p25"],
                mode="lines",
                line=dict(width=0),
                line_shape="hv",
                fill="tonexty",
                name="25–75%",
                fillcolor="rgba(0, 100, 200, 0.6)",
            )
        )

        # --- Median line ---
        occupancy_fig.add_trace(
            go.Scatter(
                x=summary_df["Days"],
                y=summary_df["median"],
                mode="lines",
                line_shape="hv",
                name="Median",
                line=dict(width=1.5, color="black"),
            )
        )

        occupancy_fig.update_layout(
            xaxis_title="Days",
            yaxis_title="Occupancy",
        )

    else:
        mean_df["rolling_mean_7"] = (
            mean_df["Occupancy"].rolling(window=7, center=True).mean()
        )

        # Create a line plot with one line per
        occupancy_fig = px.line(occupancy_df, x="Days", y="Occupancy", color="run")

        occupancy_fig.update_traces(opacity=0.3)

        # Add mean line
        occupancy_fig.add_scatter(
            x=mean_df["Days"],
            y=mean_df["Occupancy"],
            mode="lines",
            name="Mean across runs",
            line=dict(width=2, color="black"),
        )

        # Add rolling mean line
        occupancy_fig.add_scatter(
            x=mean_df["Days"],
            y=mean_df["rolling_mean_7"],
            mode="lines",
            name="7-day rolling mean",
            line=dict(width=1, color="green"),
        )

    occupancy_fig.add_vline(
        x=warm_up_duration_days,
        line_width=3,
        line_dash="dash",
        line_color="red",
    )

    return occupancy_fig
