import pandas as pd
from pathlib import Path
from random import choices
import privacy

# Set data directories
ROOT_DIRECTORY = Path("/Users/JKMacBook/Documents/Lambda/Product1/PrivacyHistos")
DATA_DIRECTORY = ROOT_DIRECTORY / "data"
ground_truth_file = DATA_DIRECTORY / "ground_truth_test.csv"

number_histos = 3
sample = 1
sample_size = 3
population_queries = 2
epsilon = 10.0

sensitivity = (number_histos * sample_size) + population_queries

combo_dict = {'spd': ['shift_c', 'pca_c', 'dca_c'],
              'cp': ['company_c', 'payment_c'],
              'fare': ['fare_n', 'tips_n', 'seconds_n', 'miles_n']
              }

num_dict = {'fare_n': [50, 5, 100],
            'tips_n': [20, 2, 50],
            'seconds_n': [5000, 100, 10000],
            'miles_n': [20, 2, 50]
            }

ground_truth = pd.read_csv(ground_truth_file)

valid = privacy.check_input(ground_truth, combo_dict, num_dict)

df, num_decode, col_decode = privacy.preprocess(ground_truth, combo_dict, num_dict)
print(df, num_decode, col_decode)

privacy.histo_test(df, combo_dict)

spd_population, spd_weights = privacy.create_private_histo(df, 'spd', sample, sample_size, sensitivity, epsilon)
cp_population, cp_weights = privacy.create_private_histo(df, 'cp', sample, sample_size, sensitivity, epsilon)
fare_population, fare_weights = privacy.create_private_histo(df, 'fare', sample, sample_size, sensitivity, epsilon)
spd_value = choices(spd_population, spd_weights)
cp_value = choices(cp_population, cp_weights)
fare_value = choices(fare_population, fare_weights)

shift = privacy.col_decoder(num_dict, num_decode, col_decode, spd_value[0], 'shift_c')
pca = privacy.col_decoder(num_dict, num_decode, col_decode, spd_value[0], 'pca_c')
dca = privacy.col_decoder(num_dict, num_decode, col_decode, spd_value[0], 'dca_c')

company = privacy.col_decoder(num_dict, num_decode, col_decode, cp_value[0], 'company_c')
payment = privacy.col_decoder(num_dict, num_decode, col_decode, cp_value[0], 'payment_c')

fares = privacy.col_decoder(num_dict, num_decode, col_decode, fare_value[0], 'fare_n')
tips = privacy.col_decoder(num_dict, num_decode, col_decode, fare_value[0], 'tips_n')
seconds = privacy.col_decoder(num_dict, num_decode, col_decode, fare_value[0], 'seconds_n')
miles = privacy.col_decoder(num_dict, num_decode, col_decode, fare_value[0], 'miles_n')

print('spd_value', spd_value)
print('shift', shift)
print('pca', pca)
print('dca', dca)
print(' ')
print('cm_value', cp_value)
print('company', company)
print('payment', payment)
print(' ')
print('fare_value', fare_value)
print('fares', fares)
print('tips', tips)
print('seconds', seconds)
print('miles', miles)
