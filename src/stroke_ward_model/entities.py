import numpy as np


# MARK: Patient
# Patient class to store patient attributes
class Patient:
    """
    Representation of an individual patient within the simulation.

    A `Patient` object stores all clinical, pathway, and state-related
    attributes required for modelling flow through the stroke/TIA care
    process. Several characteristics (onset type, MRS score, diagnosis
    category, admission likelihood) are randomly generated on creation
    using parameters defined in the global configuration class `g`.

    Parameters
    ----------
    p_id : int or str
        Unique identifier for the patient.

    Attributes
    ----------
    id : int or str
        Patient identifier.
    q_time_nurse : float
        Time spent waiting for nursing assessment or consultation.
    q_time_ward : float
        Time spent waiting for an inpatient ward bed.
    onset_type : int
        Categorisation of onset information:
        - 0 : Known onset
        - 1 : Unknown onset but within CTP window
        - 2 : Unknown onset and outside CTP window
    mrs_type : int
        Modified Rankin Scale score at presentation (0–5).
        Drawn from an exponential distribution and capped at 5.
    mrs_discharge : int
        Modified Rankin Scale score at discharge (set later by the model).
    diagnosis : int
        Raw randomised diagnostic value (0–100). Used to map to a clinical
        category based on thresholds defined in `g`.
    patient_diagnosis : int
        Encoded diagnosis category:
        - 0 : Intracerebral haemorrhage (ICH)
        - 1 : Ischaemic stroke (I)
        - 2 : Transient ischaemic attack (TIA)
        - 3 : Stroke mimic
        - 4 : Non-stroke
    priority : int
        Triage priority level (used for queue ordering).
    non_admission : int
        Randomised admission likelihood score (0–100).
    advanced_ct_pathway : bool
        Whether the patient enters an advanced CT imaging pathway.
    sdec_pathway : bool
        Whether the patient is routed through SDEC.
    thrombolysis : bool
        Whether the patient receives thrombolysis.
    thrombectomy : bool
        Whether the patient receives thrombectomy.
    admission_avoidance : bool
        Whether the patient avoids an admission by being seen in SDEC instead.

    Notes
    -----
    GENAI declaration (SR): this docstring has been generated with the aid
    of ChatGPT 5.1.
    All generated content has been thoroughly reviewed.
    """

    def __init__(self, p_id):
        self.id = p_id
        self.q_time_nurse = np.NaN  # SR NOTE - changed this to NaN by default
        self.q_time_ward = np.NaN  # SR NOTE - changed this to NaN by default
        # 0 = known onset, 1 = unknown onset (in ctp range), 2 = unknown (out of
        # ctp range)
        # SR NOTE: I've moved all random generation to the start of their assessment
        # to allow for reproducibility
        # self.onset_type = random.randint(0, 2)
        self.onset_type = np.NaN
        # Max MRS is set to 5
        # self.mrs_type = min(round(random.expovariate(1.0 / g.mean_mrs)), 5)
        self.mrs_type = np.NaN
        self.mrs_discharge = np.NaN  # SR NOTE - changed this to NaN by default
        # <=5 is ICH, <=55 is I, <= 70 is TIA, <=85 is Stroke Mimic, >85 is non\
        # stroke, this set in g class
        # TODO: SR: This does not appear to be in sync with actual values seen in the g class
        # TODO: SR: Which is correct?
        # self.diagnosis = random.randint(0, 100)
        self.diagnosis = np.NaN
        # 0 = ICH, 1 = I, 2 = TIA, 3 = Stroke Mimic, 4 = non stroke
        self.patient_diagnosis = np.NaN  # SR NOTE - changed this to NaN by default
        self.priority = 1
        # self.non_admission = random.randint(0, 100)
        self.non_admission = np.NaN
        self.advanced_ct_pathway = False
        self.sdec_pathway = False
        self.thrombolysis = False
        self.thrombectomy = False
        self.admission_avoidance = False

        # NOTE: Additional items added by SR
        self.ward_los = np.NaN
        self.ward_los_thrombolysis = np.NaN
        self.sdec_los = np.NaN
        self.ctp_duration = np.NaN
        self.ct_duration = np.NaN
        self.arrived_ooh = False
        self.generated_during_warm_up = False
        self.patient_diagnosis_type = None

        # Recording times of various events for animations
        self.clock_start = np.NaN  # This can be considered to be their arrival time

        self.nurse_q_start_time = np.NaN
        self.nurse_triage_start_time = np.NaN
        self.nurse_triage_end_time = np.NaN

        self.ct_or_ctp_scan_start_time = np.NaN
        self.ct_or_ctp_scan_end_time = np.NaN

        self.sdec_running_when_required = np.NaN
        self.sdec_full_when_required = np.NaN
        self.sdec_admit_time = np.NaN
        self.sdec_discharge_time = np.NaN

        self.ward_q_start_time = np.NaN
        self.ward_admit_time = np.NaN
        self.ward_discharge_time = np.NaN
        self.exit_time = np.NaN

        self.nurse_attending_id = np.NaN
        self.ct_scanner_id = np.NaN
        self.sdec_bed_id = np.NaN
        self.ward_bed_id = np.NaN

        # Flag for optionally removing incomplete journeys or processing them
        # in a different way in results
        self.journey_completed = False
