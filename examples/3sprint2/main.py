# Imports
import pandas as pd
import numpy as np
from pathlib import Path
from loguru import logger
from random import choices

import privacy
from simulate_row import simulate_row

ROOT_DIRECTORY = Path("/Users/JKMacBook/Documents/Lambda/Product/final")
DATA_DIRECTORY = ROOT_DIRECTORY / "data"
ground_truth_file = DATA_DIRECTORY / "ground_truth_s2.csv"
output_file = ROOT_DIRECTORY / "submission1.csv"

header = ['PUMA', 'YEAR', 'HHWT', 'GQ', 'PERWT', 'SEX', 'AGE', 'MARST', 'RACE',
          'HISPAN', 'CITIZEN', 'SPEAKENG', 'HCOVANY', 'HCOVPRIV', 'HINSEMP',
          'HINSCAID', 'HINSCARE', 'EDUC', 'EMPSTAT', 'EMPSTATD', 'LABFORCE',
          'WRKLSTWK', 'ABSENT', 'LOOKING', 'AVAILBLE', 'WRKRECAL', 'WORKEDYR',
          'INCTOT', 'INCWAGE', 'INCWELFR', 'INCINVST', 'INCEARN', 'POVERTY',
          'DEPARTS', 'ARRIVES', 'sim_individual_id'
          ]

number_histos = 7
population_queries = 1
epsilons = [0.1, 1.0, 10.0]
max_records = 1350000
mrpi = 7
sample = 0

combo_dict = {  # 'HHWT': ['HHWT_n'],
              'DEMO': ['GQ_c', 'SEX_c', 'MARST_c', 'RACE_c', 'HISPAN_c',
                       'CITIZEN_c', 'SPEAKENG_c'],
              'AGEEDUC': ['AGE_c', 'EDUC_c'],
              'HEALTH': ['HCOVANY_c', 'HCOVPRIV_c', 'HINSEMP_c', 'HINSCAID_c',
                         'HINSCARE_c'],
              'WORK': ['EMPSTAT_c', 'EMPSTATD_c', 'LABFORCE_c', 'WRKLSTWK_c',
                       'ABSENT_c', 'LOOKING_c', 'AVAILBLE_c', 'WRKRECAL_c',
                       'WORKEDYR_c'],
              'INCOME': ['INCTOT_n', 'INCWAGE_n', 'INCINVST_n', 'POVERTY_n']
              #  'DEPARTS': ['DEPARTS_n']
              }

depart_list = [0, 300, 330, 400, 430, 500, 530, 600, 630, 700, 730, 800, 830, 900,
               930, 1000, 1030, 1100, 1130, 1200, 1230, 1300, 1330, 1400, 1430, 1500,
               1530, 1600, 1630, 1700, 1730, 1800, 1830, 1900, 1930, 2000, 2030, 2100,
               2130, 2200, 2230, 2300, 2330]

num_dict = {  # 'HHWT_n': [480, 20, 500],
            'INCTOT_n': [240000, 10000, 300000],
            'INCWAGE_n': [240000, 10000, 300000],
            'INCINVST_n': [150000, 10000, 250000],
            'POVERTY_n': [500, 100, 600]
            #  'DEPARTS_n': [2300, 25, 2359]
            }


# Creates the weights for the bins adding noise to the bin counts
# using the Laplace mechanism
#    df - the input dataframe
#    c - the column
#    b - the bins (population)
#    m - max_records_per_individual
#    h - number of histograms
#    e - epsilon
#    return the weights for the population
def weight(df, c, b, m, h, e):

    new_df = df[c].groupby(pd.cut(df[c], b)).count()

    for i in range(len(new_df)):
        new_df[i] = privacy.laplaceMechanism(new_df[i], (m * h) + 1, e)

    final_df = new_df / new_df.sum()
    w = []
    for i in range(len(final_df.index)):
        w.append(final_df[i])
    return w


# The main procedure
def main():

    logger.info("begin pre-processing")
    ground_truth = pd.read_csv(ground_truth_file)
    valid = privacy.check_input(ground_truth, combo_dict, num_dict)
    if valid != 1:
        return
    df, num_decodes, col_decodes = privacy.preprocess(ground_truth, combo_dict, num_dict)
    privacy.histo_test(df, combo_dict)
    logger.info("end pre-processing")

    # Initialize variables
    pumas = df['PUMA_x'].unique().tolist()
    years = df['YEAR_x'].unique().tolist()
    num_pumas = len(pumas)
    num_years = len(years)
    num_records = len(df.index)
    rows_per_py = int((max_records - num_records)/(num_pumas * num_years))
    sensitivity = (number_histos * mrpi) + population_queries

    # Create dataframe for final results and initialize final list
    final_df = pd.DataFrame(columns=header)
    final_list = []

    # The main loop
    # For each epsilon cycle through the PUMA-years
    #     For epsilons <= 1.0 use all the data
    #     For epsilons > 1.0 use PUMA data
    for epsilon in epsilons:
        if epsilon <= 1.0:
            logger.info(f"begin histogram creation {epsilon}")

            hhwt_bins = np.r_[np.arange(0, 500, 20), np.inf]
            hhwt_pop = [i * 20 for i in range(len(hhwt_bins))]
            hhwt_pop.pop()
            hhwt_w = weight(df, 'HHWT_x', hhwt_bins, mrpi, number_histos, epsilon)

            # hhwt_pop, hhwt_w = utilities.create_private_histo(puma_data, 'HHWT', sample, mrpi, sensitivity, epsilon)
            demo_pop, demo_w = privacy.create_private_histo(df, 'DEMO', sample, mrpi, sensitivity, epsilon)
            ageeduc_pop, ageeduc_w = privacy.create_private_histo(df, 'AGEEDUC', sample, mrpi, sensitivity, epsilon)
            health_pop, health_w = privacy.create_private_histo(df, 'HEALTH', sample, mrpi, sensitivity, epsilon)
            work_pop, work_w = privacy.create_private_histo(df, 'WORK', sample, mrpi, sensitivity, epsilon)
            income_pop, income_w = privacy.create_private_histo(df, 'INCOME', sample, mrpi, sensitivity, epsilon)

            departs_bins = [-np.inf, 0, 300, 330, 400, 430, 500, 530, 600, 630, 700, 730, 800, 830, 900,
                            930, 1000, 1030, 1100, 1130, 1200, 1230, 1300, 1330, 1400, 1430, 1500,
                            1530, 1600, 1630, 1700, 1730, 1800, 1830, 1900, 1930, 2000, 2030, 2100,
                            2130, 2200, 2230, np.inf]
            departs_pop = [0, 300, 330, 400, 430, 500, 530, 600, 630, 700, 730, 800, 830, 900,
                           930, 1000, 1030, 1100, 1130, 1200, 1230, 1300, 1330, 1400, 1430, 1500,
                           1530, 1600, 1630, 1700, 1730, 1800, 1830, 1900, 1930, 2000, 2030, 2100,
                           2130, 2200, 2230, 2300]
            departs_w = weight(df, 'DEPARTS_x', departs_bins, mrpi, number_histos, epsilon)

            # departs_pop, departs_w = utilities.create_private_histo(df, 'DEPARTS', sample, mrpi, sensitivity, epsilon)
            logger.info(f"end histogram creation {epsilon}")

        i = 1
        for puma in pumas:
            logger.info(f"processing {epsilon} {puma}")
            for year in years:
                if epsilon > 1.0:
                    puma_data = df[(df['PUMA_x'] == puma)]
                    # logger.info(f"begin histogram creation {epsilon}")

                    hhwt_bins = np.r_[np.arange(0, 500, 20), np.inf]
                    hhwt_pop = [i * 20 for i in range(len(hhwt_bins))]
                    hhwt_pop.pop()
                    hhwt_w = weight(puma_data, 'HHWT_x', hhwt_bins, mrpi, number_histos, epsilon)

                    # hhwt_pop, hhwt_w = utilities.create_private_histo(puma_data, 'HHWT', sample, mrpi, sensitivity, epsilon)
                    demo_pop, demo_w = privacy.create_private_histo(puma_data, 'DEMO', sample, mrpi, sensitivity, epsilon)
                    ageeduc_pop, ageeduc_w = privacy.create_private_histo(puma_data, 'AGEEDUC', sample, mrpi, sensitivity, epsilon)
                    health_pop, health_w = privacy.create_private_histo(puma_data, 'HEALTH', sample, mrpi, sensitivity, epsilon)
                    work_pop, work_w = privacy.create_private_histo(puma_data, 'WORK', sample, mrpi, sensitivity, epsilon)
                    income_pop, income_w = privacy.create_private_histo(puma_data, 'INCOME', sample, mrpi, sensitivity, epsilon)

                    departs_bins = [-np.inf, 0, 300, 330, 400, 430, 500, 530, 600, 630, 700, 730, 800, 830, 900,
                                    930, 1000, 1030, 1100, 1130, 1200, 1230, 1300, 1330, 1400, 1430, 1500,
                                    1530, 1600, 1630, 1700, 1730, 1800, 1830, 1900, 1930, 2000, 2030, 2100,
                                    2130, 2200, 2230, np.inf]
                    departs_pop = [0, 300, 330, 400, 430, 500, 530, 600, 630, 700, 730, 800, 830, 900,
                                   930, 1000, 1030, 1100, 1130, 1200, 1230, 1300, 1330, 1400, 1430, 1500,
                                   1530, 1600, 1630, 1700, 1730, 1800, 1830, 1900, 1930, 2000, 2030, 2100,
                                   2130, 2200, 2230, 2300]
                    departs_w = weight(puma_data, 'DEPARTS_x', departs_bins, mrpi, number_histos, epsilon)

                    # departs_pop, departs_w = utilities.create_private_histo(df, 'DEPARTS', sample, mrpi, sensitivity, epsilon)
                    # logger.info(f"end histogram creation {epsilon}")

                # Create simulated individuals for each PUMA-year
                puma_year = df[(df['PUMA_x'] == puma) &
                               (df['YEAR_x'] == year)]
                sim_count = len(puma_year.index)
                sim_count_noise = int(privacy.laplaceMechanism(sim_count, sensitivity, epsilon))

                # Check for bias
                if ((sim_count_noise - sim_count) > rows_per_py):
                    sim_count_noise = sim_count + rows_per_py - 1
                elif (((sim_count_noise - sim_count) < -rows_per_py)):
                    sim_count_noise = sim_count - rows_per_py + 1

                # For each PUMA-year create simulated individuals
                for j in range(sim_count_noise):
                    hhwt_value = choices(hhwt_pop, hhwt_w, k=1)
                    demo_value = choices(demo_pop, demo_w, k=1)
                    ageeduc_value = choices(ageeduc_pop, ageeduc_w, k=1)
                    health_value = choices(health_pop, health_w, k=1)
                    work_value = choices(work_pop, work_w, k=1)
                    income_value = choices(income_pop, income_w, k=1)
                    departs_value = choices(departs_pop, departs_w, k=1)
                    row = simulate_row(epsilon,
                                       puma,
                                       year,
                                       hhwt_value[0],
                                       demo_value[0],
                                       ageeduc_value[0],
                                       health_value[0],
                                       work_value[0],
                                       income_value[0],
                                       departs_value[0],
                                       num_dict,
                                       num_decodes,
                                       col_decodes
                                       )
                    row['sim_individual_id'] = i
                    i = i + 1
                    final_list.append(row)

    logger.info('writing data to output file')
    final_df = pd.DataFrame.from_dict(final_list)
    final_df.to_csv(output_file, index=False)


main()
