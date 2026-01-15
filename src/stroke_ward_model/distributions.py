from stroke_ward_model.inputs import g
from sim_tools.distributions import Gamma, Exponential, Normal, DiscreteEmpirical
import numpy as np


##############################
# MARK: Set up distributions #
##############################
def initialise_distributions(self):
    """
    Set up distributions for sampling from.
    Pulls distribution parameters from g class where relevant.
    Use of Seed
    """
    ss = np.random.SeedSequence(g.master_seed + self.run_number)
    seeds = ss.spawn(35)

    # Inter-arrival times
    self.patient_inter_day_dist = Exponential(
        mean=g.patient_inter_day, random_seed=seeds[0]
    )

    self.patient_inter_night_dist = Exponential(
        mean=g.patient_inter_night, random_seed=seeds[1]
    )

    self.nurse_consult_time_dist = Exponential(
        mean=g.mean_n_consult_time, random_seed=seeds[2]
    )
    self.ct_time_dist = Exponential(mean=g.mean_n_ct_time, random_seed=seeds[3])
    self.sdec_time_dist = Exponential(mean=g.mean_n_sdec_time, random_seed=seeds[4])

    # self.i_ward_time_mrs_0_dist = Exponential(
    #     mean=g.mean_n_i_ward_time_mrs_0, random_seed=seeds[5]
    # )
    # self.i_ward_time_mrs_1_dist = Exponential(
    #     mean=g.mean_n_i_ward_time_mrs_1, random_seed=seeds[6]
    # )
    # self.i_ward_time_mrs_2_dist = Exponential(
    #     mean=g.mean_n_i_ward_time_mrs_2, random_seed=seeds[7]
    # )
    # self.i_ward_time_mrs_3_dist = Exponential(
    #     mean=g.mean_n_i_ward_time_mrs_3, random_seed=seeds[8]
    # )
    # self.i_ward_time_mrs_4_dist = Exponential(
    #     mean=g.mean_n_i_ward_time_mrs_4, random_seed=seeds[9]
    # )
    # self.i_ward_time_mrs_5_dist = Exponential(
    #     mean=g.mean_n_i_ward_time_mrs_5, random_seed=seeds[10]
    # )

    # self.ich_ward_time_mrs_0_dist = Exponential(
    #     mean=g.mean_n_ich_ward_time_mrs_0, random_seed=seeds[11]
    # )
    # self.ich_ward_time_mrs_1_dist = Exponential(
    #     mean=g.mean_n_ich_ward_time_mrs_1, random_seed=seeds[12]
    # )
    # self.ich_ward_time_mrs_2_dist = Exponential(
    #     mean=g.mean_n_ich_ward_time_mrs_2, random_seed=seeds[13]
    # )
    # self.ich_ward_time_mrs_3_dist = Exponential(
    #     mean=g.mean_n_ich_ward_time_mrs_3, random_seed=seeds[14]
    # )
    # self.ich_ward_time_mrs_4_dist = Exponential(
    #     mean=g.mean_n_ich_ward_time_mrs_4, random_seed=seeds[15]
    # )
    # self.ich_ward_time_mrs_5_dist = Exponential(
    #     mean=g.mean_n_ich_ward_time_mrs_5, random_seed=seeds[16]
    # )

    # self.tia_ward_time_dist = Exponential(
    #     mean=g.mean_n_non_stroke_ward_time, random_seed=seeds[17]
    # )
    # self.non_stroke_ward_time_dist = Exponential(
    #     mean=g.mean_n_tia_ward_time, random_seed=seeds[18]
    # )

    self.i_ward_time_mrs_0_dist = Gamma(
        alpha=g.i_shape,
        beta=g.mean_n_i_ward_time_mrs_0 / g.i_shape,
        random_seed=seeds[5],
    )
    self.i_ward_time_mrs_1_dist = Gamma(
        alpha=g.i_shape,
        beta=g.mean_n_i_ward_time_mrs_1 / g.i_shape,
        random_seed=seeds[6],
    )
    self.i_ward_time_mrs_2_dist = Gamma(
        alpha=g.i_shape,
        beta=g.mean_n_i_ward_time_mrs_2 / g.i_shape,
        random_seed=seeds[7],
    )
    self.i_ward_time_mrs_3_dist = Gamma(
        alpha=g.i_shape,
        beta=g.mean_n_i_ward_time_mrs_3 / g.i_shape,
        random_seed=seeds[8],
    )
    self.i_ward_time_mrs_4_dist = Gamma(
        alpha=g.i_shape,
        beta=g.mean_n_i_ward_time_mrs_4 / g.i_shape,
        random_seed=seeds[9],
    )
    self.i_ward_time_mrs_5_dist = Gamma(
        alpha=g.i_shape,
        beta=g.mean_n_i_ward_time_mrs_5 / g.i_shape,
        random_seed=seeds[10],
    )

    self.ich_ward_time_mrs_0_dist = Gamma(
        alpha=g.ich_shape,
        beta=g.mean_n_ich_ward_time_mrs_0 / g.ich_shape,
        random_seed=seeds[11],
    )
    self.ich_ward_time_mrs_1_dist = Gamma(
        alpha=g.ich_shape,
        beta=g.mean_n_ich_ward_time_mrs_1 / g.ich_shape,
        random_seed=seeds[12],
    )
    self.ich_ward_time_mrs_2_dist = Gamma(
        alpha=g.ich_shape,
        beta=g.mean_n_ich_ward_time_mrs_2 / g.ich_shape,
        random_seed=seeds[13],
    )
    self.ich_ward_time_mrs_3_dist = Gamma(
        alpha=g.ich_shape,
        beta=g.mean_n_ich_ward_time_mrs_3 / g.ich_shape,
        random_seed=seeds[14],
    )
    self.ich_ward_time_mrs_4_dist = Gamma(
        alpha=g.ich_shape,
        beta=g.mean_n_ich_ward_time_mrs_4 / g.ich_shape,
        random_seed=seeds[15],
    )
    self.ich_ward_time_mrs_5_dist = Gamma(
        alpha=g.ich_shape,
        beta=g.mean_n_ich_ward_time_mrs_5 / g.ich_shape,
        random_seed=seeds[16],
    )

    self.tia_ward_time_dist = Gamma(
        alpha=g.tia_shape,
        beta=g.mean_n_non_stroke_ward_time / g.tia_shape,
        random_seed=seeds[17],
    )

    self.non_stroke_ward_time_dist = Gamma(
        alpha=g.non_stroke_shape,
        beta=g.mean_n_tia_ward_time / g.non_stroke_shape,
        random_seed=seeds[18],
    )

    # Patient Attribute Distributions
    self.onset_type_distribution = DiscreteEmpirical(
        values=[0, 1, 2],
        freq=[1, 1, 1],  # equal weight of all possibilities
        random_seed=seeds[19],
    )

    self.mrs_type_distribution = Exponential(g.mean_mrs, random_seed=seeds[20])

    self.diagnosis_distribution = DiscreteEmpirical(
        values=list(range(0, 101)),  # 0 to 100 (upper is exclusive)
        freq=[1 for _ in range(101)],  # equal weight of all possibilities
        random_seed=seeds[21],
    )

    self.non_admission_distribution = DiscreteEmpirical(
        values=list(range(0, 101)),  # 0 to 100 (upper is exclusive)
        freq=[1 for _ in range(101)],  # equal weight of all possibilities
        random_seed=seeds[22],
    )

    # TODO: Is this the best distribution for this?
    # Per-patient diagnosis randomisation
    # self.ich_range = random.normalvariate(g.ich, 1)
    self.ich_range_distribution = Normal(g.ich, 1, random_seed=seeds[23])
    # self.i_range = max(random.normalvariate(g.i, 1), self.ich_range)
    self.i_range_distribution = Normal(g.i, 1, random_seed=seeds[24])
    # self.tia_range = max(random.normalvariate(g.tia, 1), self.i_range)
    self.tia_range_distribution = Normal(g.tia, 1, random_seed=seeds[25])
    # self.stroke_mimic_range = max(
    #     random.normalvariate(g.stroke_mimic, 1), self.tia_range
    # )
    self.stroke_mimic_range_distribution = Normal(
        g.stroke_mimic, 1, random_seed=seeds[26]
    )
    # self.non_stroke_range = max(
    #     random.normalvariate(g.stroke_mimic, 1), self.stroke_mimic_range
    # )
    self.non_stroke_range_distribution = Normal(
        g.stroke_mimic, 1, random_seed=seeds[27]
    )

    # TODO: Is this the best distribution for this?
    # Admission chance distributions
    # self.tia_admission_chance = random.normalvariate(g.tia_admission, 1)
    self.tia_admission_chance_distribution = Normal(
        g.tia_admission, 1, random_seed=seeds[28]
    )
    # self.stroke_mimic_admission_chance = random.normalvariate(
    #     g.stroke_mimic_admission, 1
    # )
    self.stroke_mimic_admission_chance_distribution = Normal(
        g.stroke_mimic_admission, 1, random_seed=seeds[29]
    )

    # MRS on discharge distribution
    self.mrs_reduction_during_stay = DiscreteEmpirical(
        values=[0, 1],
        freq=[1, 1],
        random_seed=seeds[30],
    )

    self.mrs_reduction_during_stay_thrombolysed = DiscreteEmpirical(
        values=[0, 1, 2],
        freq=[1, 1, 1],
        random_seed=seeds[31],
    )
