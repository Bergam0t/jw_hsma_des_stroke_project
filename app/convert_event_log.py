import pandas as pd
from vidigi.prep import reshape_for_animations, generate_animation_df
from vidigi.animation import (
    generate_animation,
    animate_activity_log,
    add_repeating_overlay,
)
from vidigi.utils import EventPosition, create_event_position_df

EVENT_POSITION_DF = create_event_position_df(
    [
        EventPosition(event="arrival", x=50, y=875, label="Arrival"),
        EventPosition(
            event="nurse_q_start_time", x=205, y=800, label="Waiting for Nurse"
        ),
        EventPosition(
            event="nurse_triage_start_time",
            x=205,
            y=700,
            resource="number_of_nurses",
            label="Being Triaged by Nurse",
        ),
        EventPosition(
            event="ct_or_ctp_scan_start_time",
            x=205,
            y=600,
            label="Undergoing CT or CTP Scan",
        ),
        EventPosition(
            event="sdec_admit_time",
            x=605,
            y=400,
            resource="sdec_beds",
            label="In SDEC",
        ),
        EventPosition(
            event="ward_q_start_time",
            x=205,
            y=400,
            label="Waiting for Bed\non Main Stroke Ward",
        ),
        EventPosition(
            event="ward_admit_time",
            x=605,
            y=150,
            resource="number_of_ward_beds",
            label="In Stroke Ward",
        ),
        EventPosition(event="depart", x=805, y=100, label="Exit"),
    ]
)


def convert_event_log(patient_df, run=1):
    patient_df_single_run = patient_df[patient_df["run"] == run]

    patient_df_single_run_times = patient_df_single_run[
        [
            "id",
            "patient_diagnosis_type",
            "thrombolysis",
            "admission_avoidance",
            "arrived_ooh",
            "advanced_ct_pathway",
            "clock_start",
            "nurse_q_start_time",
            "nurse_triage_start_time",
            "nurse_triage_end_time",
            "ct_or_ctp_scan_start_time",
            "ct_or_ctp_scan_end_time",
            "sdec_admit_time",
            "sdec_discharge_time",
            "ward_q_start_time",
            "ward_admit_time",
            "ward_discharge_time",
            "exit_time",
        ]
    ].copy()

    patient_df_single_run_ids = patient_df_single_run[
        ["id", "nurse_attending_id", "ct_scanner_id", "sdec_bed_id", "ward_bed_id"]
    ]

    # Fix people with no exit time - for our purposes, it just needs to be the max observed time in their row
    row_max = patient_df_single_run_times[
        [
            "clock_start",
            "nurse_q_start_time",
            "nurse_triage_start_time",
            "nurse_triage_end_time",
            "ct_or_ctp_scan_start_time",
            "ct_or_ctp_scan_end_time",
            "sdec_admit_time",
            "sdec_discharge_time",
            "ward_q_start_time",
            "ward_admit_time",
            "ward_discharge_time",
            "exit_time",
        ]
    ].max(axis=1)

    patient_df_single_run_times["exit_time"] = patient_df_single_run_times[
        "exit_time"
    ].fillna(row_max)

    patient_df_single_run_times_long = patient_df_single_run_times.melt(
        id_vars=[
            "id",
            "patient_diagnosis_type",
            "thrombolysis",
            "admission_avoidance",
            "advanced_ct_pathway",
            "arrived_ooh",
        ]
    ).rename(columns={"variable": "event", "value": "time"})

    event_map = {
        "clock_start": "arrival_departure",
        "nurse_q_start_time": "queue",
        "nurse_triage_start_time": "resource_use",
        "nurse_triage_end_time": "resource_use_end",
        "ct_or_ctp_scan_start_time": "resource_use",
        "ct_or_ctp_scan_end_time": "resource_use_end",
        "sdec_admit_time": "resource_use",
        "sdec_discharge_time": "resource_use_end",
        "ward_q_start_time": "queue",
        "ward_admit_time": "resource_use",
        "ward_discharge_time": "resource_use_end",
        "exit_time": "arrival_departure",
    }

    patient_df_single_run_times_long["event_type"] = patient_df_single_run_times_long[
        "event"
    ].apply(lambda x: event_map[x])

    patient_df_single_run_resource_ids = patient_df_single_run[
        ["id", "nurse_attending_id", "sdec_bed_id", "ward_bed_id"]
    ]

    patient_df_single_run_resource_ids = patient_df_single_run_resource_ids.melt(
        id_vars="id", value_name="resource_id"
    )

    resource_mapping_df = pd.DataFrame(
        [
            {"variable": "nurse_attending_id", "event": "nurse_triage_start_time"},
            {"variable": "nurse_attending_id", "event": "nurse_triage_end_time"},
            {"variable": "sdec_bed_id", "event": "sdec_admit_time"},
            {"variable": "sdec_bed_id", "event": "sdec_discharge_time"},
            {"variable": "ward_bed_id", "event": "ward_admit_time"},
            {"variable": "ward_bed_id", "event": "ward_discharge_time"},
        ]
    )

    patient_df_single_run_resource_ids = patient_df_single_run_resource_ids.merge(
        resource_mapping_df, on="variable", how="inner"
    ).drop(columns=["variable"])

    event_log = patient_df_single_run_times_long.merge(
        patient_df_single_run_resource_ids, on=["id", "event"], how="outer"
    ).dropna(subset="time")

    event_log["event"] = event_log["event"].apply(
        lambda x: "arrival" if x == "clock_start" else x
    )
    event_log["event"] = event_log["event"].apply(
        lambda x: "depart" if x == "exit_time" else x
    )

    return event_log


def create_vidigi_animation_simple(
    event_log,
    scenario,
    limit_duration=60 * 24 * 7 * 16,  # Default = 16 weeks
    event_position_df=EVENT_POSITION_DF,
):
    return animate_activity_log(
        event_log=event_log,
        event_position_df=event_position_df,
        entity_col_name="id",
        scenario=scenario,
        debug_mode=True,
        setup_mode=False,
        every_x_time_units=30,
        include_play_button=True,
        resource_icon_size=15,
        text_size=20,
        entity_icon_size=13,
        gap_between_entities=6,
        gap_between_queue_rows=25,
        gap_between_resource_rows=25,
        plotly_height=900,
        frame_duration=200,
        plotly_width=1200,
        override_x_max=800,
        override_y_max=900,
        limit_duration=limit_duration,
        wrap_queues_at=25,
        step_snapshot_max=125,
        time_display_units="dhm_ampm",
        display_stage_labels=True,
    )


def create_vidigi_animation_advanced(
    event_log,
    scenario,
    event_position_df=EVENT_POSITION_DF,
    snapshot_interval=30,
    step_snapshot_max=100,
    entity_col_name="id",
    gap_between_resource_rows=50,
    gap_between_resources=20,
):
    warm_up_threshold = scenario.warm_up_period + (scenario.sdec_opening_hour * 60)

    limit_duration = (scenario.sim_duration / 12) + warm_up_threshold

    print(f"Limit duration: {limit_duration}")

    full_patient_df = reshape_for_animations(
        event_log,
        entity_col_name=entity_col_name,
        limit_duration=limit_duration,
        every_x_time_units=snapshot_interval,
        step_snapshot_max=step_snapshot_max,
    )

    print("Full patient df (5 rows)")
    print(full_patient_df.head())

    print(f"Warm-up duration: {warm_up_threshold}")

    # Remove the warm-up period from the event log
    full_patient_df = full_patient_df[
        full_patient_df["snapshot_time"] >= warm_up_threshold
    ]

    full_patient_df_plus_pos = generate_animation_df(
        full_entity_df=full_patient_df,
        entity_col_name=entity_col_name,
        event_position_df=event_position_df,
        wrap_queues_at=25,
        step_snapshot_max=step_snapshot_max,
        gap_between_entities=15,
        gap_between_queue_rows=30,
        gap_between_resource_rows=gap_between_resource_rows,
        debug_mode=True,
        step_snapshot_limit_gauges=True,
        gap_between_resources=gap_between_resources,
    )

    final_df = full_patient_df_plus_pos.copy()

    # return final_df

    # Change icon depending on stroke type
    final_df["icon"] = final_df.apply(
        lambda x: "🩸" if x["patient_diagnosis_type"] == "ICH" else x["icon"], axis=1
    )
    final_df["icon"] = final_df.apply(
        lambda x: "⌚" if x["patient_diagnosis_type"] == "I" else x["icon"], axis=1
    )
    final_df["icon"] = final_df.apply(
        lambda x: "➡️" if x["patient_diagnosis_type"] == "TIA" else x["icon"], axis=1
    )
    final_df["icon"] = final_df.apply(
        lambda x: "🪞" if x["patient_diagnosis_type"] == "Stroke Mimic" else x["icon"],
        axis=1,
    )
    final_df["icon"] = final_df.apply(
        lambda x: "🚷" if x["patient_diagnosis_type"] == "Non Stroke" else x["icon"],
        axis=1,
    )
    final_df["icon"] = final_df.apply(
        lambda x: x["icon"] + "*" if x["admission_avoidance"] else x["icon"], axis=1
    )

    fig = generate_animation(
        full_entity_df_plus_pos=final_df,
        event_position_df=event_position_df,
        scenario=scenario,
        entity_col_name=entity_col_name,
        plotly_height=900,
        frame_duration=600,
        frame_transition_duration=800,
        plotly_width=1200,
        override_x_max=800,
        override_y_max=900,
        entity_icon_size=20,
        gap_between_resource_rows=gap_between_resource_rows,
        include_play_button=True,
        add_background_image=None,
        display_stage_labels=True,
        time_display_units="day_clock_ampm",
        simulation_time_unit="minutes",
        setup_mode=False,
        debug_mode=True,
        resource_icon_size=15,
        text_size=20,
        start_time=f"{scenario.sdec_opening_hour}:00:00",
        gap_between_resources=gap_between_resources,
    )

    return fig
