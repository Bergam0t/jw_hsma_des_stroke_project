import pandas as pd
from stroke_ward_model.inputs import g
from stroke_ward_model.trial import Trial

g.sdec_opening_hour = 8
g.ctp_opening_hour = 9
g.in_hours_start = 8
g.ooh_start = 0

# This code asks the user if they want to generate cvs per run
csv_input = False

while csv_input == False:
    csv_value = input("Write results to CSV? Yes / No")
    if csv_value == "Yes" or csv_value == "yes":
        g.write_to_csv = True
        csv_input = True
    elif csv_value == "No" or csv_value == "no":
        g.write_to_csv = False
        csv_input = True
    else:
        print("Invalid Input Please Try Again")

# This code asks the user if they want to generate a graph per run
graph_input = False

while graph_input == False:
    graph_value = input("Generate graph per run? Yes / No")
    if graph_value == "Yes" or graph_value == "yes":
        g.gen_graph = True
        graph_input = True
    elif graph_value == "No" or graph_value == "no":
        g.gen_graph = False
        graph_input = True
    else:
        print("Invalid Input Please Try Again")


for x in range(3):
    # Code to ask the user how many beds are active on the unit.
    user_ward_beds = False

    while user_ward_beds == False:
        g.number_of_ward_beds = int(input("Choose Number of Ward Beds"))
        if g.number_of_ward_beds > 0:
            user_ward_beds = True
        else:
            print("Invalid Input Please Try Again")

    # This code asks if the user wants to have full therapy support for the SDEC

    therapy_input = False

    while therapy_input == False:
        therapy_value = input("Run SDEC with Full Therapy Support? Yes / No")
        if therapy_value == "Yes" or therapy_value == "yes":
            g.therapy_sdec = True
            therapy_input = True
        elif therapy_value == "No" or therapy_value == "no":
            g.therapy_sdec = False
            therapy_input = True
        else:
            print("Invalid Input Please Try Again")

    # This code asks the user how long the SDEC should be unavailable for, as a
    # % of days.

    sdec_input = False

    while sdec_input == False:
        sdec_value = int(
            input("What percentage of the day should the SDEC be available? (0-100)")
        )
        if sdec_value <= 100 and sdec_value >= 0:
            g.sdec_value = sdec_value
            g.sdec_unav_freq = 1440 * (sdec_value / 100)
            g.sdec_unav_time = 1440 - g.sdec_unav_freq
            sdec_input = True
        elif sdec_value == 100:
            g.sdec_value = sdec_value
            g.sdec_unav_freq = g.sim_duration * 2
            g.sdec_unav_time = 0
            sdec_input = True
        else:
            print("Invalid Input Please Try Again")

    # This code asks the user how long the SDEC should be unavailable for, as a
    # % of days.

    ctp_input = False

    while ctp_input == False:
        ctp_value = int(
            input("What percentage of the day should the CTP be available? (0-100)")
        )
        if ctp_value <= 100 and ctp_value >= 0:
            g.ctp_value = ctp_value
            g.ctp_unav_freq = 1440 * (ctp_value / 100)
            g.ctp_unav_time = 1440 - g.ctp_unav_freq
            ctp_input = True
        # TODO: SR - JW I think this might be a typo?
        # TODO SR - it was elif sdec_value == 100
        # TODO SR - I have changed it to `elif ctp_value == 100:`
        elif ctp_value == 100:
            g.ctp_value = ctp_value
            g.ctp_unav_freq = g.sim_duration * 2
            g.ctp_unav_time = 0
            sdec_input = True
        else:
            print("Invalid Input Please Try Again")

    # Create an instance of the Trial class
    my_trial = Trial()

    # Call the run_trial method of our Trial object
    my_trial.run_trial()

    g.trials_run_counter += 1

print("All Trials Completed")


# Combine all trial results into a single dictionary, I am
# currently unaware were the trial_sdec_finacial_savings is stored in class g
# but it works so I'll leave it for now...
trial_numbers = g.trial_sdec_financial_savings.keys()
combined_results = {
    trial: {
        "Mean Q Time Nurse (Mins)": g.trial_mean_q_time_nurse.get(trial, None),
        "Number of Admissions Avoided In Run": g.trial_number_of_admissions_avoided.get(
            trial, None
        ),
        "Mean Q Time Ward (Hours)": g.trial_mean_q_time_ward.get(trial, None),
        "Mean Occupancy": g.trial_mean_occupancy.get(trial, None),
        "Number of Admission Delays": g.trial_number_of_admission_delays.get(
            trial, None
        ),
        "Total SDEC Savings (£)": g.trial_financial_savings_of_a_a.get(trial, None),
        "Total SDEC Staff Cost (£)": g.sdec_medical_cost.get(trial, None),
        "SDEC Savings - Costs (£)": g.trial_sdec_financial_savings.get(trial, None),
        "Thrombolysis Savings (£)": g.trial_thrombolysis_savings.get(trial, None),
        "Total Savings (£)": g.trial_total_savings.get(trial, None),
        "Mean MRS Change": g.trial_mrs_change.get(trial, None),
        "Mean Patients Generated in Run": g.trial_avg_patients.get(trial, None)
    }
    for trial in trial_numbers
}

df_all_trial_results = pd.DataFrame.from_dict(combined_results, orient="index")
df_all_trial_results.index.name = "Trial Number"

if g.write_to_csv == True:
    df_all_trial_results.to_csv("experiments/all_trial_results.csv", index=False)
