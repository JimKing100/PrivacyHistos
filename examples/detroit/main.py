import pandas as pd
from pathlib import Path
from loguru import logger
from random import choices

import privacy
from simulate_row import simulate_row

ROOT_DIRECTORY = Path(__file__).absolute().parent.parent.parent
DATA_DIRECTORY = ROOT_DIRECTORY / "data"
ground_truth_file = DATA_DIRECTORY / "ground_truth_detroit.csv"
output_file = DATA_DIRECTORY / "submission.csv"

number_histos = 4
population_queries = 1
sample = 0
sample_size = 1
epsilons = [1.0]

combo_dict = {'type': ['engine_area_c', 'exposure_c', 'incident_type_c', 'property_use_c', 'detector_c', 'structure_stat_c'],
              'injury': ['cinjury_c', 'cfatal_c', 'finjury_c', 'ffatal_c'],
              'call': ['call_month_c', 'call_day_c', 'call_hour_c'],
              'result': ['dispatch_n', 'arrival_n', 'clear_n']
              }

num_dict = {'dispatch_n': [1000, 50, 5000],
            'arrival_n': [1000, 50, 5000],
            'clear_n': [5000, 50, 10000]
            }


def main():

    logger.info("begin pre-processing")
    ground_truth = pd.read_csv(ground_truth_file)
    header = list(ground_truth.columns)
    valid = privacy.check_input(ground_truth, combo_dict, num_dict)
    if valid != 1:
        return

    df, num_decodes, col_decodes = privacy.preprocess(ground_truth, combo_dict, num_dict)
    privacy.histo_test(df, combo_dict)
    logger.info("end pre-processing")

    # main for loop
    for epsilon in epsilons:
        # Create dataframe for final results
        final_df = pd.DataFrame(columns=header)
        final_list = []

        # sensitivity = (histograms x sample size) + population queries
        sensitivity = (number_histos * sample_size) + population_queries

        # Create the incidents - population count
        num_incidents = len(df)
        num_incidents_noise = int(privacy.laplaceMechanism(num_incidents, sensitivity, epsilon))

        # Create the four histograms
        logger.info(f"begin histogram creation {epsilon}")
        type_pop, type_w = privacy.create_private_histo(df, 'type', sample, sample_size, sensitivity, epsilon)
        injury_pop, injury_w = privacy.create_private_histo(df, 'injury', sample, sample_size, sensitivity, epsilon)
        call_pop, call_w = privacy.create_private_histo(df, 'call', sample, sample_size, sensitivity, epsilon)
        result_pop, result_w = privacy.create_private_histo(df, 'result', sample, sample_size, sensitivity, epsilon)

        for i in range(num_incidents_noise):
            type_value = choices(type_pop, type_w, k=1)
            injury_value = choices(injury_pop, injury_w, k=1)
            call_value = choices(call_pop, call_w, k=1)
            result_value = choices(result_pop, result_w, k=1)
            row = simulate_row(i,
                               type_value[0],
                               injury_value[0],
                               call_value[0],
                               result_value[0],
                               num_dict,
                               num_decodes,
                               col_decodes
                               )
            final_list.append(row)

        logger.info('writing data to output file')
        final_df = pd.DataFrame.from_dict(final_list)
        final_df.to_csv(output_file, index=False)


main()
