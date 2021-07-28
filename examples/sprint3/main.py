import pandas as pd
from pathlib import Path
from loguru import logger
from random import choices

import privacy
import trips
from simulate_row import simulate_row

ROOT_DIRECTORY = Path("/Users/JKMacBook/Documents/Lambda/Product/final")
DATA_DIRECTORY = ROOT_DIRECTORY / "data"
ground_truth_file = DATA_DIRECTORY / "ground_truth_s3.csv"
output_file = ROOT_DIRECTORY / "submission.csv"

header = ['epsilon', 'shift', 'company_id', 'pickup_community_area',
          'dropoff_community_area', 'payment_type', 'fare', 'tips',
          'trip_total', 'trip_seconds', 'trip_miles']

number_histos = 3
population_queries = 2
epsilons = [1.0, 10.0]
max_records = 17000000
mrpi = 200
sample = 1

combo_dict = {'spd': ['shift_c', 'pca_c', 'dca_c'],
              'cp': ['company_c', 'payment_c'],
              'fare': ['fare_n', 'tips_n', 'seconds_n', 'miles_n']
              }

num_dict = {'fare_n': [55, 5, 100],
            'tips_n': [22, 2, 50],
            'seconds_n': [5100, 100, 10000],
            'miles_n': [22, 2, 50]
            }


def main():

    counter = 0
    e_counter = 1
    filenames = []

    logger.info("begin pre-processing")
    ground_truth = pd.read_csv(ground_truth_file)
    valid = privacy.check_input(ground_truth, combo_dict, num_dict)
    if valid != 1:
        return
    prox_dict = trips.proximity(ground_truth)
    df, num_decodes, col_decodes = privacy.preprocess(ground_truth, combo_dict, num_dict)
    privacy.histo_test(df, combo_dict)
    logger.info("end pre-processing")

    # main for loop
    for epsilon in epsilons:
        # Create dataframe for final results and initialize lists
        front_list = []
        end_list = []
        final_df = pd.DataFrame(columns=header)

        # sample_size represents max_records_per_individual used
        if epsilon < 5.0:
            sample_size = 10
        else:
            sample_size = 30
        # sensitivity = (histograms x max_records_per_individual) + population queries
        sensitivity = (number_histos * sample_size) + population_queries

        # Create the taxi_drivers - 1st population count
        drivers = df['taxi_id_i'].unique().tolist()
        num_drivers = len(drivers)
        num_drivers_noise = int(privacy.laplaceMechanism(num_drivers, sensitivity, epsilon))

        # Create the three histograms
        logger.info(f"begin histogram creation {epsilon}")
        spd_pop, spd_w = privacy.create_private_histo(df, 'spd', sample, sample_size, sensitivity, epsilon)
        cp_pop, cp_w = privacy.create_private_histo(df, 'cp', sample, sample_size, sensitivity, epsilon)
        fr_pop, fr_w = privacy.create_private_histo(df, 'fare', sample, sample_size, sensitivity, epsilon)

        # Create the trips - 2nd population count
        tr_pop, tr_w = trips.create_trips_histo(df, 'taxi_id_i', sensitivity, epsilon, mrpi, e_counter)
        logger.info(f"end histogram creation {epsilon}")

        # Initialize initial_driver (taxi_id) and counters
        initial_driver = 1000000
        all_counter = 0

        # Create a list of random combined features equal to max_records length
        shift_pca_dca = choices(spd_pop, spd_w, k=max_records)
        fares = choices(fr_pop, fr_w, k=max_records)
        # test = len(shift_pca_dca)

        # The driver (taxi_id) for loop
        for driver in range(initial_driver, (initial_driver + num_drivers_noise)):
            counter += 1
            if counter % 1000 == 0:
                logger.info(f"processing {counter} drivers {all_counter}")

            # Create the number of trips for a driver
            num_trips = choices(tr_pop, tr_w)[0]
            if num_trips > mrpi:
                num_trips = mrpi

            # Select random company and payment type for a driver
            company_payment = choices(cp_pop, cp_w, k=1)

            # The trip for loop
            for trip in range(num_trips):
                row, row1 = simulate_row(epsilon,
                                         driver,
                                         shift_pca_dca[all_counter],
                                         company_payment[0],
                                         fares[all_counter],
                                         prox_dict,
                                         num_dict,
                                         num_decodes,
                                         col_decodes
                                         )
                all_counter += 1
                # Create two lists
                #   - front_list contains epsilon, driver, spd, cp, sec_estimate
                #   - end_list contains fare, tips, trip_total, trip_seconds, trip_miles
                front_list.append(row)
                end_list.append(row1)

        # Concatenate the two list sorted by seconds estimate and trip_seconds
        logger.info("concatenation start")
        front_df = pd.DataFrame.from_dict(front_list)
        front1_df = front_df.sort_values(by=['sec_estimate'])
        front1_df = front_df.drop(columns=['sec_estimate'])
        end_df = pd.DataFrame.from_dict(end_list)
        end1_df = end_df.sort_values(by=['trip_seconds'])
        final_df = pd.concat([front1_df, end1_df], axis=1)
        logger.info("concatenation end")

        # Output to a file
        logger.info(f"writing temp file for epsilon {epsilon}")
        f_name = 'temp' + str(e_counter) + '.csv'
        epsilon_file = DATA_DIRECTORY / f_name
        if e_counter == 1:
            final_df.to_csv(epsilon_file, index=False)
        else:
            final_df.to_csv(epsilon_file, header=False, index=False)
        e_counter += 1
        filenames.append(epsilon_file)
        logger.info(f"done for epsilon {epsilon}")

    logger.info("writing submission.csv")
    with open(output_file, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)


main()
