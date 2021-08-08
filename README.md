# PrivacyHistos

Welcome to the PrivacyHistos repository.  This repo contains five differential privacy functions for combining features into privatized histograms.  The five functions are contained in the **privacy.py** file located in the **src** directory.

----

### [Setup](#0-getting-started)
 - [Environment](#environment)
 - [Data](#data)
### [Input](#1-input)
 - [Formatted Ground Truth Data](#formatted-ground-truth-data)
### [Functions](#2-functions)
### [Basic Example](#3-basic-example)

----

## (0) Setup

### Environment

There are two environments included in this repo, both require **Python 3.8.5+**:
- **Basic** - The **requirements1.txt** file contains the bare bones packages necessary to run private.py and the Basic example.
- **Advanced** - The **requirements2.txt** files contains the packages necessary for running all the examples and unit testing.

### Data

The data directory holds the necessary data files and only contains the data files for the Basic example.  In order to run the other eaxamples the data files will need to be downloaded into the data directory with the following names:
- **ground_truth_2.csv** - The ground truth file for the Sprint 2 example (about 111.9MB).
- **ground_truth_3.csv** - The ground truth file for the Sprint 3 example (about 623.5MB).

## (1) Input

In order to use the functions the following input is required:

1) **Formatted Ground Truth Data (ground_truth)**
    * All data must be encoded as positive integers with no Nans
    * The column names must be appended as follows:
        - _c – indicates a categorical feature
        - _n – indicates a numeric feature
        - _i – One, and only one, column must be the individual identifier
        - _x – indicates a feature to include but not used as a combination feature
2) **Sensitivity and Epsilon (sensitivity, epsilon)**
    * Sensitivity = (number of histograms * sample size) + population queries
        - Number of histograms – the total number of histograms which may include other histograms not using the combined column approach.
        - Sample size – the number of individual records to use for building the histograms (if smapling is used).
        - Population queries – the total number of population queries used in the overall approach.
    * Epsilon - The epslion value to use
3) **Combination Dictionary (combo_dict)**
    * Format - {combo_name: column_list}
    * combo_name – name of the the new combined feature
    * column_list – a list of columns to combine (categorical and/or numeric)
    * Example - {‘cp’: [‘company_c’, ‘payment_c’]}
    * Explanation – Create a column named ‘cp’ combining categorical fields
‘company_c’ and ‘payment_c’
4) **Number Dictionary (num_dict)**
    * Format - {column_name: [top_value, increment, max_range]}
    * column_name – the name of the numeric feature
    * top_value – the top value to use with the increment
    * increment – the amount in each bin
    * max_range – the maximum value of the numeric range
    * Example – {‘fare_n’: [50, 5, 100]}
    * Explanation – Create 11 numeric bins for numeric feature ‘fare_n’ with bins of 5 from 0-50 (10 bins of 5) with numbers over 50 in a bin of 50-100 (1 bin of 50).

## (2) Functions

There are five public functions:

1) **check_input(ground_truth, combo_dict, num_dict)** - Tests the formatted ground truth data, the combination dictionary and the number dictionary for proper formatting and values.
    * ground_truth – the formatted ground truth dataframe
    * combo_dict – the combination dictionary
    * num_dict – the numeric dictionary
    * returns 1 if True
2) **pre_process(ground_truth, combo_dict, num_dict)** - Preprocesses the ground truth data by combining the columns per the combination dictionary and number dictionary
    * ground_truth – the formatted ground truth dataframe
    * combo_dict – the combination dictionary
    * num_dict – the numeric dictionary
    * returns a new dataframe with combined columns (df)
    * returns a numeric decoder dictionary (num_decode)
    * returns a column decoder dictionary (col_decode)
3) **histo_test(df, combo_dict)** - Counts the number of bins created for each combined column in the pre-processed dataframe. A useful tool for determining the optimal feature combinations.
    * df – the pre-processed dataframe
    * combo_dict – the combination dictionary
    * prints a count of bins for each combined column
4) **create_private_histo(df, column, sample, sample_size, sensitivity, epsilon)** - Creates privatized histograms of the specified combined column using a specified sample size, sensitivity and epsilon.
    * df – the pre-processed dataframe
    * column – the combined column
    * sample - enter 1 to use sampling
    * sample_size – the size of the sample
    * sensitivity – the sensitivity
    * epsilon – the epsilon
    * returns population (bins) as a list
    * returns privatized weights as a list
5) **col_decoder(num_dict, num_decode, col_decode, value, column)** - Decodes the specified column into a its privatized value.
    * num_dict – the numeric dictionary
    * num_decode – the numeric decoder dictionary
    * col_decode – the column decoder dictionary
    * value – a value to decode
    * column – the column to decode
    * returns decoded privatized value

## (3) Basic Example

Basic example


