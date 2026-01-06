from stroke_ward_model.stroke_admission_classes import g, Trial
import streamlit as st
import plotly.express as px
from app_utils import iconMetricContainer

st.set_page_config(layout="wide")

st.logo("app/resources/nhs-logo-colour.png", size="large")

with open("app/resources/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

g.gen_graph = True

with st.sidebar:
    st.subheader("Stroke Ward Configuration")

    number_of_ward_beds = st.slider(
        "Choose the number of beds available in the ward", 1, 100, 49
    )
    g.number_of_ward_beds = number_of_ward_beds

    number_of_sdec_beds = st.slider(
        "Choose the number of beds available in the SDEC", 1, 20, 5
    )
    g.sdec_beds = number_of_sdec_beds

    therapy_sdec = st.toggle("Should the SDEC run with full therapy support?")
    g.therapy_sdec = therapy_sdec

    st.divider()
    st.subheader("Opening Hours")

    set_opening_hours_as_perc = st.toggle(
        "Set the opening hours as a percentage of a day?"
    )

    if set_opening_hours_as_perc:
        sdec_unaval_perc = st.number_input(
            "What percentage of the day should the SDEC be available? (0-100)",
            min_value=0,
            max_value=100,
            value=33,
        )

        st.caption(
            f"This equates to the SDEC being open roughly {24 / 100 * sdec_unaval_perc:.1f} hours a day"
        )

        ctp_unaval_perc = st.number_input(
            "What percentage of the day should the CT Perfusion Scanner (CTP) be available? (0-100)",
            min_value=0.0,
            max_value=100.0,
            value=33.3,
        )

        st.caption(
            f"This equates to the CT perfusion scanner being available roughly {24 / 100 * sdec_unaval_perc:.1f} hours a day"
        )

    else:
        sdec_avail_hours = st.slider(
            "How many hours a day should the SDEC be available?",
            0.0,
            24.0,
            8.0,
            step=0.25,
        )

        st.caption(f"The SDEC is available {sdec_avail_hours / 24.0:.1%} of the time")

        sdec_open_time = st.time_input(
            "What time should the SDEC be open from?", value="08:00", step=60
        )
        g.sdec_opening_hour = sdec_open_time.hour

        sdec_unaval_perc = ((24.0 - sdec_avail_hours) / 24.0) * 100

        ctp_avail_hours = st.slider(
            "How many hours a day should the CT perfusion scanner be available?",
            0.0,
            24.0,
            8.0,
            step=0.25,
        )

        st.caption(
            f"The CTP perfusion scanner is available {ctp_avail_hours / 24.0:.1%} of the time"
        )

        ctp_open_time = st.time_input(
            "What time should the CTP scanner be open from?", value="08:00", step=60
        )

        g.ctp_opening_hour = ctp_open_time.hour

        ctp_unaval_perc = ((24.0 - ctp_avail_hours) / 24.0) * 100

    sdec_available_perc = 100.0 - sdec_unaval_perc
    ctp_available_perc = 100.0 - ctp_unaval_perc

    if sdec_available_perc <= 100 and sdec_available_perc >= 0:
        g.sdec_value = sdec_available_perc
        g.sdec_unav_freq = 1440 * (sdec_available_perc / 100)
        g.sdec_unav_time = 1440 - g.sdec_unav_freq
    elif sdec_available_perc == 100:
        g.sdec_value = sdec_available_perc
        g.sdec_unav_freq = g.sim_duration * 2
        g.sdec_unav_time = 0

    if ctp_available_perc <= 100 and ctp_available_perc >= 0:
        g.ctp_value = ctp_available_perc
        g.ctp_unav_freq = 1440 * (ctp_available_perc / 100)
        g.ctp_unav_time = 1440 - g.ctp_unav_freq
    elif ctp_available_perc == 100:
        g.ctp_value = ctp_available_perc
        g.ctp_unav_freq = g.sim_duration * 2
        g.ctp_unav_time = 0

    st.divider()

    st.subheader("Demand")

    in_hours_demand_start = st.time_input(
        "What time does your in-hours demand start?", "08:00", step=60
    )

    g.in_hours_start = in_hours_demand_start.hour

    in_hours_mean_iat = st.number_input(
        "What is the average time (in minutes) between arrivals at the unit in-hours?",
        min_value=1.0,
        max_value=5000.0,
        value=200.0,
    )

    g.patient_inter_day = in_hours_mean_iat

    out_of_hours_demand_start = st.time_input(
        "What time does your out-of-hours demand start?", "20:00", step=60
    )

    g.ooh_start = out_of_hours_demand_start.hour

    out_of_hours_mean_iat = st.number_input(
        "What is the average time (in minutes) between arrivals at the unit out-of-hours?",
        min_value=1.0,
        max_value=5000.0,
        value=666.67,
    )

    g.patient_inter_night = out_of_hours_mean_iat

    st.divider()

    st.subheader("Model Parameters")

    number_of_runs = st.number_input(
        "Number of Runs", min_value=1, max_value=100, value=10
    )
    g.number_of_runs = number_of_runs

    # TODO: Are people likely to want to simulate partial years?
    # Could switch to number of years slider instead if not for ease.
    sim_duration_days = st.slider(
        "Number of days to simulate", 180, 365 * 5, value=365, step=5
    )
    sim_duration_minutes = sim_duration_days * 24 * 60

    g.sim_duration = sim_duration_minutes

    st.caption(
        f"You are simulating {(sim_duration_days // 365)} year{'' if sim_duration_days // 365 == 1 else 's'} and {sim_duration_days % 365} days"
    )

    warm_up_duration_days = st.slider(
        "Number of days to warm-up", 30, 180, value=180, step=5
    )
    warm_up_duration_minutes = warm_up_duration_days * 24 * 60

    g.warm_up_period = warm_up_duration_minutes

    debug_console = st.toggle("Turn on Debugging Console Messages", value=False)

    g.show_trace = debug_console

    master_seed = st.number_input(
        "Set the master seed",
        value=42,
        min_value=1,
        max_value=None,
        step=1,
        help="This parameter affects the random numbers used",
    )

    g.master_seed = master_seed

button_run_pressed = st.button("Run simulation")

if button_run_pressed:
    with st.spinner("Running Model - Please Wait", show_time=True):
        # Create an instance of the Trial class
        my_trial = Trial()

        # Call the run_trial method of our Trial object
        my_trial.run_trial()

        sim_duration_days = g.sim_duration / 60 / 24
        sim_duration_years = sim_duration_days / 365

        # st.write(my_trial.trial_info)

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "Overview",
                "Output Graphs",
                "Animation",
                "Scenario Comparison",
                "Model Exploration",
            ]
        )

        with tab1:
            st.subheader("Configuration")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                with iconMetricContainer(
                    key="ctp_avail",
                    icon_unicode="ea4a",
                    family="outline",
                    icon_color="black",
                    type="symbols",
                ):
                    st.metric(
                        label=f"CTP scanners",
                        value=g.number_of_ctp,
                        border=True,
                    )

                    st.caption(
                        f"Available from {g.ctp_opening_hour} until {g.ctp_opening_hour + (((24 * 60) - g.ctp_unav_time) / 60)} ({(((24 * 60) - g.ctp_unav_time) / 60):.1f} hours)"
                    )
            with col2:
                with iconMetricContainer(
                    key="sdec_beds",
                    icon_unicode="e4d0",
                    family="outline",
                    icon_color="black",
                    type="symbols",
                ):
                    st.metric(
                        label=f"SDEC beds",
                        value=g.sdec_beds,
                        border=True,
                    )

                    st.caption(
                        f"Open from {g.sdec_opening_hour} until {g.sdec_opening_hour + (((24 * 60) - g.sdec_unav_time) / 60)} ({(((24 * 60) - g.sdec_unav_time) / 60):.1f} hours)"
                    )

            with col3:
                with iconMetricContainer(
                    key="sdec_therapy",
                    icon_unicode="f2c2",
                    family="outline",
                    icon_color="black",
                    type="symbols",
                ):
                    st.metric(
                        label="SDEC Therapy",
                        value="Yes" if g.therapy_sdec else "No",
                        border=True,
                    )

            with col4:
                with iconMetricContainer(
                    key="ward_bed_count",
                    icon_unicode="ea48",
                    family="outline",
                    icon_color="black",
                    type="symbols",
                ):
                    st.metric(
                        label="Standard Ward Beds",
                        value=f"{g.number_of_ward_beds}",
                        border=True,
                    )

            average_patients_per_run = (
                my_trial.trial_patient_df.groupby("run").count().mean().values[0]
            )

            average_patients_per_year = (
                average_patients_per_run / (g.sim_duration / 60 / 24)
            ) * 365

            with col1:
                with iconMetricContainer(
                    key="patients_per_year",
                    icon_unicode="ebcc",
                    family="outline",
                    icon_color="black",
                    type="symbols",
                ):
                    st.metric(
                        label="Average Patients per Year",
                        value=f"{average_patients_per_year:.0f}",
                        border=True,
                    )

            with col2:
                with iconMetricContainer(
                    key="patients_per_day",
                    icon_unicode="e878",
                    family="outline",
                    icon_color="black",
                    type="symbols",
                ):
                    st.metric(
                        label="Average Patients per Day",
                        value=f"{(average_patients_per_year / 365):.0f}",
                        border=True,
                    )

            st.divider()

            st.subheader("Results")

            col1a, col2a, col3a = st.columns(3)

            with col1a:
                with iconMetricContainer(
                    key="thrombolysis_savings",
                    icon_unicode="e133",
                    family="outline",
                    icon_color="black",
                    type="symbols",
                ):
                    st.metric(
                        label="Average Thrombolysis Savings per Year",
                        value=f"£{(my_trial.df_trial_results['Thrombolysis Savings (£)'] / sim_duration_years).mean():,.0f}",
                        border=True,
                    )

                    st.caption(
                        f"Average savings were £{my_trial.df_trial_results['Thrombolysis Savings (£)'].mean():,.0f} across the full model run of {(sim_duration_days // 365)} year{'' if sim_duration_days // 365 == 1 else 's'} and {sim_duration_days % 365} days"
                    )

            with col2a:
                with iconMetricContainer(
                    key="sdec_savings",
                    icon_unicode="e4d0",
                    family="outline",
                    icon_color="black",
                    type="symbols",
                ):
                    st.metric(
                        label="Average SDEC Savings per Year",
                        value=f"£{(my_trial.df_trial_results['SDEC Savings (£)'] / sim_duration_years).mean():,.0f}",
                        border=True,
                    )

                    st.caption(
                        f"Average savings were £{my_trial.df_trial_results['SDEC Savings (£)'].mean():,.0f} across the full model run of {(sim_duration_days // 365)} year{'' if sim_duration_days // 365 == 1 else 's'} and {sim_duration_days % 365} days"
                    )

            with col3a:
                with iconMetricContainer(
                    key="overall_savings",
                    icon_unicode="f04b",
                    family="outline",
                    icon_color="black",
                    type="symbols",
                ):
                    st.metric(
                        label="Average Overall Savings per Year",
                        value=f"£{(my_trial.df_trial_results['Total Savings'] / sim_duration_years).mean():,.0f}",
                        border=True,
                    )

                    st.caption(
                        f"Average savings were £{my_trial.df_trial_results['Total Savings'].mean():,.0f} across the full model run of {(sim_duration_days // 365)} year{'' if sim_duration_days // 365 == 1 else 's'} and {sim_duration_days % 365} days"
                    )

            st.html("<br/>")

            col1b, col2b, col3b = st.columns(3)

            with col1b:
                with iconMetricContainer(
                    key="ward_occupancy",
                    icon_unicode="e13c",
                    family="outline",
                    icon_color="black",
                    type="symbols",
                ):
                    st.metric(
                        label="Mean Ward Occupancy",
                        value=f"{my_trial.df_trial_results['Mean Occupancy'].mean():,.0f} of {g.number_of_ward_beds} beds",
                        border=True,
                    )

                    st.caption(
                        f"This is an average occupancy of {(my_trial.df_trial_results['Mean Occupancy'].mean() / g.number_of_ward_beds):.1%}"
                    )

            with col2b:
                with iconMetricContainer(
                    key="admissions_avoided",
                    icon_unicode="e0b6",
                    family="outline",
                    icon_color="black",
                    type="symbols",
                ):
                    st.metric(
                        label="Average Admissions Avoided per Year",
                        value=f"{(my_trial.df_trial_results['Number of Admissions Avoided In Run'] / sim_duration_years).mean():,.0f}",
                        border=True,
                    )

                    st.caption(
                        f"On average, {my_trial.df_trial_results['Number of Admissions Avoided In Run'].mean():,.0f} admissions were avoided across the full model run of {(sim_duration_days // 365)} year{'' if sim_duration_days // 365 == 1 else 's'} and {sim_duration_days % 365} days"
                    )

            with col3b:
                with iconMetricContainer(
                    key="admission_delays",
                    icon_unicode="f38c",
                    family="outline",
                    icon_color="black",
                    type="symbols",
                ):
                    st.metric(
                        label="Average Admission Delays per Year",
                        value=f"{(my_trial.df_trial_results['Number of Admission Delays'] / sim_duration_years).mean():,.0f}",
                        border=True,
                    )

                    st.caption(
                        f"On average, {my_trial.df_trial_results['Number of Admission Delays'].mean():,.0f} admissions were delayed across the full model run of {(g.sim_duration / 60 / 24):.0f} days"
                    )

            st.subheader("Full Per-Run Results")

            st.dataframe(my_trial.df_trial_results.T)

            st.subheader("Full Per-Patient Results")

            st.dataframe(my_trial.trial_patient_df)

        with tab2:
            # st.write(my_trial.graph_objects)

            # st.subheader("Arrival Time Debugging")

            # my_trial.trial_patient_df["clock_start_day"] = (
            #     my_trial.trial_patient_df["clock_start"] / 60
            # )

            # st.plotly_chart(
            #     px.scatter(
            #         data_frame=my_trial.trial_patient_df,
            #         x="clock_start_day",
            #         y="run",
            #         color="arrived_ooh",
            #     )
            # )

            # st.subheader("Arrival Time Debugging - By Diagnosis (Run 1 Only)")

            # st.plotly_chart(
            #     px.scatter(
            #         data_frame=my_trial.trial_patient_df[
            #             my_trial.trial_patient_df["run"] == 1
            #         ],
            #         x="clock_start_day",
            #         y="patient_diagnosis",
            #         color="arrived_ooh",
            #     )
            # )

            st.dataframe(
                my_trial.trial_patient_df.groupby(["run", "patient_diagnosis"]).size()
            )

            st.dataframe(
                my_trial.trial_patient_df.groupby(["run", "patient_diagnosis"])
                .size()
                .groupby("patient_diagnosis")
                .mean()
            )

        with tab5:

            @st.fragment
            def plot_histogram():
                patient_level_metric_choices = {
                    "Nurse Queue Time": "q_time_nurse",
                    "Ward Queue Time": "q_time_ward",
                    "Onset Type": "onset_type",
                    "MRS Type": "mrs_type",
                    "MRS on Discharge": "mrs_discharge",
                    "Diagnosis": "diagnosis",
                    "Patient Diagnosis": "patient_diagnosis",
                    "Priority": "priority",
                    "Non-Admission": "non_admission",
                    "Advanced CT Pathway": "advanced_ct_pathway",
                    "SDEC Pathway": "sdec_pathway",
                    "Thrombolysis": "thrombolysis",
                    "Thrombectomy": "thrombectomy",
                    "Admission Avoidance": "admission_avoidance",
                    "Ward LOS": "ward_los",
                    "Ward LOS for Thrombolysis Patients": "ward_los_thrombolysis",
                    "SDEC LOS": "sdec_los",
                    "CTP duration": "ctp_duration",
                    "CT duration": "ct_duration",
                    "Arrived OOH": "arrived_ooh",
                    "Patient Diagnosis Type": "patient_diagnosis_type",
                }

                split_vars = {
                    "Onset Type": "onset_type",
                    "MRS Type": "mrs_type",
                    "MRS on Discharge": "mrs_discharge",
                    "Patient Diagnosis": "patient_diagnosis",
                    "Priority": "priority",
                    "Advanced CT Pathway": "advanced_ct_pathway",
                    "SDEC Pathway": "sdec_pathway",
                    "Thrombolysis": "thrombolysis",
                    "Thrombectomy": "thrombectomy",
                    "Admission Avoidance": "admission_avoidance",
                    "Arrived OOH": "arrived_ooh",
                    "Patient Diagnosis Type": "patient_diagnosis_type",
                }

                patient_level_metric_selected = st.multiselect(
                    "Select a metric to view the distribution of",
                    options=list(patient_level_metric_choices.keys()),
                )

                selected_values = ["id", "run"] + [
                    patient_level_metric_choices[k]
                    for k in patient_level_metric_selected
                    if k in patient_level_metric_choices
                ]

                selected_color_var = st.selectbox(
                    "Select a metric to color the values by",
                    options=[None] + list(split_vars.keys()),
                )

                if selected_color_var is not None:
                    selected_color_value = split_vars[selected_color_var]
                else:
                    selected_color_var = None

                if selected_color_var is not None:
                    st.plotly_chart(
                        px.histogram(
                            data_frame=my_trial.trial_patient_df[
                                [selected_color_value] + selected_values
                            ].melt(id_vars=["id", "run", selected_color_value]),
                            x="value",
                            facet_row=selected_color_value,
                            facet_col="variable",
                        )
                    )

                else:
                    st.plotly_chart(
                        px.histogram(
                            data_frame=my_trial.trial_patient_df[selected_values].melt(
                                id_vars=["id", "run"]
                            ),
                            x="value",
                            facet_col="variable",
                        )
                    )

            plot_histogram()
