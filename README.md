# PrivacyHistos

Welcome to the PrivacyHistos repository.  This repo contains five differential privacy functions for combining features into privatized histograms.  The five functions are contained in the **privacy.py** file located in the **src directory**.  In order to use the functions the following input is required:

### Input

1) Formatted Ground Truth Data (ground_truth)
    * All data must be encoded as positive integers with no Nans
    * The column names must be appended as follows:
        - _c – indicates a categorical feature
        - _n – indicates a numeric feature
        - _i – One, and only one, column must be the individual identifier
        - _x – indicates a feature to include but not used as a combination feature
2) Sensitivity and Epsilon (sensitivity, epsilon)
    * Sensitivity = (number of histograms * sample size) + population queries
        - Number of histograms – the total number of histograms which may include other histograms not using the combined column approach.
        - Sample size – the number of individual records to use for building the histograms (if smapling is used).
        - Population queries – the total number of population queries used in the overall approach.
    * Epsilon - The epslion value to use
3) Combination Dictionary (combo_dict)
    * Format - {combo_name: column_list}
    * combo_name – name of the the new combined feature
    * column_list – a list of columns to combine (categorical and/or numeric)
    * Example - {‘cp’: [‘company_c’, ‘payment_c’]}
    * Explanation – Create a column named ‘cp’ combining categorical fields
‘company_c’ and ‘payment_c’
4) Number Dictionary (num_dict)
    * Format - {column_name: [top_value, increment, max_range]}
    * column_name – the name of the numeric feature
    * top_value – the top value to use with the increment
    * increment – the amount in each bin
    * max_range – the maximum value of the numeric range
    * Example – {‘fare_n’: [50, 5, 100]}
    * Explanation – Create 11 numeric bins for numeric feature ‘fare_n’ with bins of 5 from 0-50 (10 bins of 5) with numbers over 50 in a bin of 50-100 (1 bin of 50).

### Functions

1) check_input(ground_truth, combo_dict, num_dict)
2) pre_process(ground_truth, combo_dict, num_dict)
3) histo_test(df, combo_dict)
4) create_private_histo(df, column, sample, sample_size, sensitivity, epsilon)
5) col_decoder(num_dict, num_decode, col_decode, value, column)



