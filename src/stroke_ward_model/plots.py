import plotly.express as px

class TrialPlots:
    def __init__(self, trial_object):
        self.trial_object = trial_object
        self.trial_patient_df = self.trial_object.trial_patient_df

    def plot_los(self):
        return px.histogram(data=self.trial_patient_df, x="sdec_los")


if __name__ == "__ main __":
    from stroke_ward_model.inputs import g
    from stroke_ward_model.trial import Trial

    g.number_of_ward_beds = 30
    g.sim_duration = 365 * 24 * 60
    g.sdec_beds = 8
    sdec_value = 33.3
    g.sdec_value = sdec_value
    g.sdec_unav_freq = 1440 * (sdec_value / 100)
    g.sdec_unav_time = 1440 - g.sdec_unav_freq

    ctp_value = 50
    g.ctp_value = ctp_value
    g.ctp_unav_freq = 1440 * (ctp_value / 100)
    g.ctp_unav_time = 1440 - g.ctp_unav_freq
    ctp_input = True

    my_trial = Trial()

    # Call the run_trial method of our Trial object
    my_trial.run_trial()

    print(my_trial.trial_info)

    print(my_trial.df_trial_results.T)

    print(my_trial.trial_patient_df.head())

    plots = TrialPlots(my_trial)

    plots.plot_los()
