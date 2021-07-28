import pandas as pd
import numpy as np
from pathlib import Path
from privacy import convert_codes, convert_cat, convert_num, combine_cols, \
                    preprocess, col_decoder, laplaceMechanism, weight, \
                    create_private_histo, check_input

# Set data directories
ROOT_DIRECTORY = Path("/Users/JKMacBook/Documents/Lambda/Product1/PrivacyHistos")
DATA_DIRECTORY = ROOT_DIRECTORY / "data"
ground_truth_file = DATA_DIRECTORY / "ground_truth_test.csv"
df_test_file = DATA_DIRECTORY / "df_test.csv"

ground_truth = pd.read_csv(ground_truth_file)
df_test = pd.read_csv(df_test_file)
code_dict = {0.0: 10, 5.0: 11, 10.0: 12}
char_list = ['shift_c_char', 'company_c_char', 'pca_c_char', 'dca_c_char', 'payment_c_char']
num_list = ['fare_n_char', 'tips_n_char', 'seconds_n_char', 'miles_n_char']

combo_dict = {'spd': ['shift_c', 'pca_c', 'dca_c'],
              'cp': ['company_c', 'payment_c'],
              'fare': ['fare_n', 'tips_n', 'seconds_n', 'miles_n']
              }

num_dict = {'fare_n': [50, 5, 100],
            'tips_n': [20, 2, 50],
            'seconds_n': [5000, 100, 10000],
            'miles_n': [20, 2, 50]
            }

num_code = {'fare_n': {0.0: 10, 5.0: 11, 10.0: 12, 15.0: 13, 20.0: 14, 25.0: 15, 30.0: 16, 35.0: 17, 40.0: 18, 45.0: 19, 50.0: 20, np.inf: 21}, \
            'tips_n': {0.0: 10, 2.0: 11, 4.0: 12, 6.0: 13, 8.0: 14, 10.0: 15, 12.0: 16, 14.0: 17, 16.0: 18, 18.0: 19, 20.0: 20, np.inf: 21}, \
            'seconds_n': {0.0: 10, 100.0: 11, 200.0: 12, 300.0: 13, 400.0: 14, 500.0: 15, 600.0: 16, 700.0: 17, 800.0: 18, 900.0: 19, 1000.0: 20, \
                          1100.0: 21, 1200.0: 22, 1300.0: 23, 1400.0: 24, 1500.0: 25, 1600.0: 26, 1700.0: 27, 1800.0: 28, 1900.0: 29, 2000.0: 30, \
                          2100.0: 31, 2200.0: 32, 2300.0: 33, 2400.0: 34, 2500.0: 35, 2600.0: 36, 2700.0: 37, 2800.0: 38, 2900.0: 39, 3000.0: 40, \
                          3100.0: 41, 3200.0: 42, 3300.0: 43, 3400.0: 44, 3500.0: 45, 3600.0: 46, 3700.0: 47, 3800.0: 48, 3900.0: 49, 4000.0: 50, \
                          4100.0: 51, 4200.0: 52, 4300.0: 53, 4400.0: 54, 4500.0: 55, 4600.0: 56, 4700.0: 57, 4800.0: 58, 4900.0: 59, 5000.0: 60, np.inf: 61}, \
            'miles_n': {0.0: 10, 2.0: 11, 4.0: 12, 6.0: 13, 8.0: 14, 10.0: 15, 12.0: 16, 14.0: 17, 16.0: 18, 18.0: 19, 20.0: 20, np.inf: 21}}

num_decode = {'fare_n': {10: 0.0, 11: 5.0, 12: 10.0, 13: 15.0, 14: 20.0, 15: 25.0, 16: 30.0, 17: 35.0, 18: 40.0, 19: 45.0, 20: 50.0, 21: np.inf}, \
              'tips_n': {10: 0.0, 11: 2.0, 12: 4.0, 13: 6.0, 14: 8.0, 15: 10.0, 16: 12.0, 17: 14.0, 18: 16.0, 19: 18.0, 20: 20.0, 21: np.inf}, \
              'seconds_n': {10: 0.0, 11: 100.0, 12: 200.0, 13: 300.0, 14: 400.0, 15: 500.0, 16: 600.0, 17: 700.0, 18: 800.0, 19: 900.0, 20: 1000.0, \
                            21: 1100.0, 22: 1200.0, 23: 1300.0, 24: 1400.0, 25: 1500.0, 26: 1600.0, 27: 1700.0, 28: 1800.0, 29: 1900.0, 30: 2000.0, \
                            31: 2100.0, 32: 2200.0, 33: 2300.0, 34: 2400.0, 35: 2500.0, 36: 2600.0, 37: 2700.0, 38: 2800.0, 39: 2900.0, 40: 3000.0, \
                            41: 3100.0, 42: 3200.0, 43: 3300.0, 44: 3400.0, 45: 3500.0, 46: 3600.0, 47: 3700.0, 48: 3800.0, 49: 3900.0, 50: 4000.0, \
                            51: 4100.0, 52: 4200.0, 53: 4300.0, 54: 4400.0, 55: 4500.0, 56: 4600.0, 57: 4700.0, 58: 4800.0, 59: 4900.0, 60: 5000.0, 61: np.inf}, \
              'miles_n': {10: 0.0, 11: 2.0, 12: 4.0, 13: 6.0, 14: 8.0, 15: 10.0, 16: 12.0, 17: 14.0, 18: 16.0, 19: 18.0, 20: 20.0, 21: np.inf}}

col_decode = {'shift_c': ['spd', 1, 3], 'pca_c': ['spd', 3, 5], 'dca_c': ['spd', 5, 7], \
              'company_c': ['cp', 1, 3], 'payment_c': ['cp', 3, 4], \
              'fare_n': ['fare', 0, 2], 'tips_n': ['fare', 2, 4], 'seconds_n': ['fare', 4, 6], 'miles_n': ['fare', 6, 8]}

combo_list = ['taxi_id_i', 'spd', 'cp', 'fare']


def test_check_input():
    valid = check_input(ground_truth, combo_dict, num_dict)
    assert valid == 1


def test_convert_codes():
    assert convert_codes(0, code_dict) == 10
    assert convert_codes(5, code_dict) == 11
    assert convert_codes(10, code_dict) == 12


def test_convert_cat():
    df = convert_cat(ground_truth)
    all_list = list(df.columns)
    new_char_list = (x for x in all_list if x[-5:] == '_char')
    assert all(x in new_char_list for x in char_list)
    list_lengths = list(df['shift_c_char'])
    assert (len(x) == 2 for x in list_lengths)


def test_convert_num():
    df, num_code_test, num_decode_test = convert_num(ground_truth, num_dict)
    all_list = list(df.columns)
    new_num_list = (x for x in all_list if x[-5:] == '_char')
    assert all(x in new_num_list for x in num_list)
    list_lengths = list(df['seconds_n_char'])
    assert (len(x) == 4 for x in list_lengths)
    assert num_code_test == num_code
    assert num_decode_test == num_decode


def test_combine_cols():
    df = convert_cat(ground_truth)
    df, num_code, num_decode = convert_num(df, num_dict)
    df, col_decode_test = combine_cols(df, combo_dict)
    all_list = list(df.columns)
    assert all(x in all_list for x in combo_list)
    list_lengths = list(df['taxi_id_i'])
    assert (len(x) == 7 for x in list_lengths)
    list_lengths = list(df['spd'])
    assert (len(x) == 7 for x in list_lengths)
    list_lengths = list(df['cp'])
    assert (len(x) == 4 for x in list_lengths)
    list_lengths = list(df['fare'])
    assert (len(x) == 8 for x in list_lengths)
    assert col_decode_test == col_decode


def test_pre_process():
    df, num_decode_test, col_decode_test = preprocess(ground_truth, combo_dict, num_dict)
    all_list = list(df.columns)
    assert all(x in all_list for x in combo_list)
    assert num_decode_test == num_decode
    assert col_decode_test == col_decode


def test_laplaceMechanism():
    x = laplaceMechanism(0, 1, 1000)
    assert (x > -10) & (x < 10)


def test_weight():
    col = 'cp'
    bins = df_test[col].unique().tolist()
    bins.append(-np.inf)
    bins.sort()
    sample = 1
    sample_size = 30
    sensitivity = 92
    epsilon = 10.0
    wt = weight(df_test, col, bins, sample, sample_size, sensitivity, epsilon)
    assert len(wt) == 6
    assert wt[2] > wt[0]
    assert (sum(wt) > .99999) & (sum(wt) < 1.00001)


def test_histo_test():
    for key in combo_dict:
        bins = df_test[key].unique().tolist()
        if key == 'spd':
            assert len(bins) == 21
        if key == 'cp':
            assert len(bins) == 6
        if key == 'fare':
            assert len(bins) == 31


def test_create_private_histo():
    col = 'cp'
    bins = df_test[col].unique().tolist()
    bins.append(-np.inf)
    bins.sort()
    sample = 1
    sample_size = 30
    sensitivity = 92
    epsilon = 10.0
    cp_pop, cp_w = create_private_histo(df_test, col, sample, sample_size, sensitivity, epsilon)
    assert len(cp_w) == 6
    assert cp_w[2] > cp_w[0]
    assert (sum(cp_w) > .99999) & (sum(cp_w) < 1.00001)
    assert cp_pop == [1271, 1279, 1491, 1495, 1520, 1521]


def test_col_decoder():
    result = col_decoder(num_dict, num_decode, col_decode, '1130608', 'shift_c')
    assert result == 13
    result = col_decoder(num_dict, num_decode, col_decode, '1130608', 'pca_c')
    assert result == 6
    result = col_decoder(num_dict, num_decode, col_decode, '1130608', 'dca_c')
    assert result == 8
    result = col_decoder(num_dict, num_decode, col_decode, '1270', 'company_c')
    assert result == 27
    result = col_decoder(num_dict, num_decode, col_decode, '1270', 'payment_c')
    assert result == 0
    result = col_decoder(num_dict, num_decode, col_decode, '11101810', 'fare_n')
    assert result >= 0 & result < 5
    result = col_decoder(num_dict, num_decode, col_decode, '11101810', 'tips_n')
    assert result == 0
    result = col_decoder(num_dict, num_decode, col_decode, '11101810', 'seconds_n')
    assert result >= 700 & result < 800
    result = col_decoder(num_dict, num_decode, col_decode, '11101810', 'miles_n')
    assert result == 0
