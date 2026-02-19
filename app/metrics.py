import pandas as pd
import numpy as np


class Metrics:
    def __init__(self, g, patient_df_including_warmup, df_trial_results):

        self.patient_df_including_warmup = patient_df_including_warmup
        self.g = g
        self.df_trial_results = df_trial_results

        # Filter out any patients who were generated before the warm-up
        # period elapsed
        self.patient_df = self.patient_df_including_warmup[
            ~self.patient_df_including_warmup["generated_during_warm_up"]
        ]

        # Time attributes
        self.sim_duration_days = g.sim_duration / 60 / 24
        self.sim_duration_years = self.sim_duration_days / 365
        self.sim_duration_display = f"""
{(self.sim_duration_days // 365):.0f}
year{"" if self.sim_duration_days // 365 == 1 else "s"} and
{(self.sim_duration_days % 365):.0f} days
            """

        self.start_hour_ctp = g.ctp_opening_hour
        self.duration_hours_ctp = ((24 * 60) - g.ctp_unav_time) / 60
        self.end_hour_ctp = (self.start_hour_ctp + self.duration_hours_ctp) % 24

        self.start_hour_sdec = g.sdec_opening_hour
        self.duration_hours_sdec = ((24 * 60) - g.sdec_unav_time) / 60
        self.end_hour_sdec = (self.start_hour_sdec + self.duration_hours_sdec) % 24

        # Patients per run
        self.average_patients_per_run = self.patient_df.groupby("run").size().mean()
        self.min_patients_per_run = self.patient_df.groupby("run").size().min()
        self.max_patients_per_run = self.patient_df.groupby("run").size().max()

        self.average_patients_per_year = self.scale_to_year(
            self.average_patients_per_run
        )

        self.average_patients_per_day = self.average_patients_per_year / 365

        self.in_hours_arrivals = (
            self.patient_df[self.patient_df["arrived_ooh"] == False]
            .groupby("run")
            .size()
        )

        self.ooh_arrivals = (
            self.patient_df[self.patient_df["arrived_ooh"] == True]
            .groupby("run")
            .size()
        )

        # Trial-level results

        # Add container with SDEC savings per year
        self.sdec_yearly_save = (
            self.df_trial_results["SDEC Savings (£)"] / self.sim_duration_years
        ).mean()

        # Add container with overall savings per year
        self.overall_yearly_save = (
            self.df_trial_results["Total Savings"] / self.sim_duration_years
        ).mean()

        self.extra_throm = g.trial_additional_thrombolysis_from_ctp[
            g.trials_run_counter
        ]
        self.extra_throm_yearly = (self.extra_throm / (g.sim_duration / 60 / 24)) * 365

        self.avoid_yearly = (
            self.df_trial_results["Number of Admissions Avoided In Run"]
            / self.sim_duration_years
        ).mean()

        self.avoid_yearly_min = (
            self.df_trial_results["Number of Admissions Avoided In Run"]
            / self.sim_duration_years
        ).min()

        self.avoid_yearly_max = (
            self.df_trial_results["Number of Admissions Avoided In Run"]
            / self.sim_duration_years
        ).max()

        self.admit_delay_yearly = (
            self.df_trial_results["Number of Admission Delays"]
            / self.sim_duration_years
        ).mean()

        self.admit_delay_yearly_min = (
            self.df_trial_results["Number of Admission Delays"]
            / self.sim_duration_years
        ).min()

        self.admit_delay_yearly_max = (
            self.df_trial_results["Number of Admission Delays"]
            / self.sim_duration_years
        ).max()

        self.mean_ward_occ = self.df_trial_results["Mean Occupancy"].mean()

        self.diagnosis_by_stroke_type_count = pd.DataFrame()
        self.diagnosis_by_stroke_type_count_per_year = pd.DataFrame()
        self.diagnosis_by_stroke_type_count_per_day = pd.DataFrame()

        self.patients_inside_sdec_operating_hours = np.NaN
        self.patients_inside_sdec_operating_hours_per_year = np.NaN
        self.patients_outside_sdec_operating_hours_per_year = np.NaN

        self.sdec_full = np.NaN
        self.sdec_full_per_year = np.NaN

        self.create_diagnosis_by_stroke_type_count()
        self.calculate_missed_opportunities()

    def create_diagnosis_by_stroke_type_count(self):

        self.diagnosis_by_stroke_type_count = (
            self.patient_df.groupby(["run", "patient_diagnosis_type"])
            .size()
            .groupby("patient_diagnosis_type")
            .mean()
            .reset_index(name="mean_patients_per_run")
        )

        self.diagnosis_by_stroke_type_count["patient_diagnosis_type"] = pd.Categorical(
            self.diagnosis_by_stroke_type_count["patient_diagnosis_type"],
            categories=["ICH", "I", "TIA", "Stroke Mimic", "Non Stroke"],
            ordered=True,
        )

        self.diagnosis_by_stroke_type_count = (
            self.diagnosis_by_stroke_type_count.sort_values("patient_diagnosis_type")
        )

        self.diagnosis_by_stroke_type_count["mean_patients_per_run"] = (
            self.diagnosis_by_stroke_type_count["mean_patients_per_run"]
            / (self.g.sim_duration / 60 / 24)
            * 365
        )

        self.diagnosis_by_stroke_type_count_per_year = (
            self.diagnosis_by_stroke_type_count.copy()
        )

        self.diagnosis_by_stroke_type_count_per_day = (
            self.diagnosis_by_stroke_type_count_per_year.copy()
        )

        self.diagnosis_by_stroke_type_count = (
            self.diagnosis_by_stroke_type_count.rename(
                columns={
                    "patient_diagnosis_type": "Diagnosis",
                    "mean_patients_per_run": "Count",
                }
            )
        )

        self.diagnosis_by_stroke_type_count_per_year = (
            self.diagnosis_by_stroke_type_count_per_year.rename(
                columns={
                    "patient_diagnosis_type": "Diagnosis",
                    "mean_patients_per_run": "Count",
                }
            )
        )

        self.diagnosis_by_stroke_type_count_per_day["mean_patients_per_run"] = (
            self.diagnosis_by_stroke_type_count_per_day["mean_patients_per_run"] / 365
        )

        self.diagnosis_by_stroke_type_count_per_day = (
            self.diagnosis_by_stroke_type_count_per_day.rename(
                columns={
                    "patient_diagnosis_type": "Diagnosis",
                    "mean_patients_per_run": "Count",
                }
            )
        )

    def calculate_missed_opportunities(self):
        self.patients_inside_sdec_operating_hours = (
            self.patient_df[(self.patient_df["sdec_running_when_required"] == True)]
            .groupby("run")
            .size()
            .mean()
        )

        self.patients_inside_sdec_operating_hours_per_year = (
            self.patients_inside_sdec_operating_hours / (self.g.sim_duration / 60 / 24)
        ) * 365

        self.patients_outside_sdec_operating_hours_per_year = (
            self.average_patients_per_year
            - self.patients_inside_sdec_operating_hours_per_year
        )

        self.sdec_full = (
            self.patient_df[self.patient_df["sdec_full_when_required"] == True]
            .groupby("run")
            .size()
            .mean()
        )

        self.sdec_full_per_year = (
            self.sdec_full / (self.g.sim_duration / 60 / 24)
        ) * 365

        self.sdec_full_min = (
            self.patient_df[self.patient_df["sdec_full_when_required"] == True]
            .groupby("run")
            .size()
            .min()
        )

        self.sdec_full_per_year_min = (
            self.sdec_full_min / (self.g.sim_duration / 60 / 24)
        ) * 365

        self.sdec_full_min = (
            self.patient_df[self.patient_df["sdec_full_when_required"] == True]
            .groupby("run")
            .size()
            .max()
        )

        self.sdec_full_per_year_max = self.scale_to_year(self.sdec_full_min)

    def scale_to_year(self, value):
        return (value / (self.g.sim_duration / 60 / 24)) * 365
