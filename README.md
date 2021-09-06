# PrivacyHistos

Welcome to the PrivacyHistos repository.  This repo contains five differential privacy functions for combining features into privatized histograms.  The five functions are contained in the **privacy.py** file located in the **src** directory.

----

### [Setup](#0-setup)
 - [Environment](#environment)
 - [Data](#data)
### [Input](#1-input)
 - [Formatted Ground Truth Data](#formatted-ground-truth-data)
 - [Sensitivity and Epsilon](#sensitivity-and-epsilon)
 - [Combination Dictionary](#combination-dictionary)
 - [Numeric Dictionary](#numeric-dictionary)
### [Functions](#2-functions)
 - [check_input](#check_input)
 - [pre_process](#pre_process)
 - [histo_test](#histo_test)
 - [create_private_histo](#create_private_histo)
 - [col_decoder](#col_decoder)
### [Basic Example](#3-basic-example)
 - [Basic Formatted Ground Truth](#basic-formatted-ground-truth)
 - [Basic Sensitivity and Epsilon](#basic-sensitivity-and-epsilon)
 - [Basic Combination Dictionary](#basic-combination-dictionary)
 - [Basic Numeric Dictionary](#basic-numeric-dictionary)
 - [1 check_input](#1-check_input)
 - [2 preprocess](#2-preprocess)
 - [3 histo_test](#3-histo_test)
 - [4 create_private_histos](#4-create_private_histos)
 - [5 col_decoder](#5-col_decoder)
 ### [Sprint 3 Example](#4-sprint-3-example)
 ### [Sprint 2 Example](#5-sprint-2-example)

----

## (0) Setup

### Environment

There are two environments included in this repo, both require **Python 3.8.5+**:
- **Basic** - The **requirements1.txt** file contains the bare bones packages necessary to run private.py and the Basic example.
- **Advanced** - The **requirements2.txt** files contains the packages necessary for running all the examples and unit testing.

### Data

The data directory holds the necessary data files and only contains the data files for the Basic example.  In order to run the other examples the data files below will need to be downloaded from Kaggle into the data directory with the following names:
- **ground_truth_2.csv** - The ground truth file for the Sprint 2 example (about 111.9MB). [download](https://www.kaggle.com/jimking100/differential-privacy-challenge-sprint-2)
- **ground_truth_3.csv** - The ground truth file for the Sprint 3 example (about 623.5MB). [download](https://www.kaggle.com/jimking100/differential-privacy-challenge-sprint-3)

## (1) Input

In order to use the functions the following input is required:

#### Formatted Ground Truth Data

  * The ground_truth data file
  * All data must be encoded as positive integers with no Nans
  * The column names must be appended as follows:
      - _c – indicates a categorical feature
      - _n – indicates a numeric feature
      - _i – One, and only one, column must be the individual identifier
      - _x – indicates a feature to include but not used as a combination feature

#### Sensitivity and Epsilon

   * Sensitivity = (number of histograms * sample size) + population queries
      - Number of histograms – the total number of histograms which may include other histograms not using the combined column approach.
      - Sample size – the number of individual records to use for building the histograms (if sampling is used).
      - Population queries – the total number of population queries used in the overall approach.
   * Epsilon - The epslion value to use

#### Combination Dictionary

   * The combo_dict with the key = combo name and the value = list of columns
   * Format - {combo_name: column_list}
   * combo_name – name of the the new combined feature
   * column_list – a list of columns to combine (categorical and/or numeric)
   * Example - {‘cp’: [‘company_c’, ‘payment_c’]}
   * Explanation – Create a column named ‘cp’ combining categorical fields ‘company_c’ and ‘payment_c’

#### Numeric Dictionary

   * The num_dict with the key = column name and the value = list of top value, increment and maximum range
   * Format - {column_name: [top_value, increment, max_range]}
   * column_name – the name of the numeric feature
   * top_value – the top value to use with the increment
   * increment – the amount in each bin
   * max_range – the maximum value of the numeric range
   * Example – {‘fare_n’: [50, 5, 100]}
   * Explanation – Create 11 numeric bins for numeric feature ‘fare_n’ with bins of 5 from 0-50 (10 bins of 5) with numbers over 50 in a bin of 50-100 (1 bin of 50).

## (2) Functions

There are five public functions located in **private.py**:

#### check_input

Tests the formatted ground truth data, the combination dictionary and the number dictionary for proper formatting and values.

1) **check_input(ground_truth, combo_dict, num_dict)**
    * ground_truth – the formatted ground truth dataframe
    * combo_dict – the combination dictionary
    * num_dict – the numeric dictionary
    * returns 1 if True

#### pre_process

Preprocesses the ground truth data by combining the columns per the combination dictionary and number dictionary

2) **pre_process(ground_truth, combo_dict, num_dict)**
    * ground_truth – the formatted ground truth dataframe
    * combo_dict – the combination dictionary
    * num_dict – the numeric dictionary
    * returns a new dataframe with combined columns (df)
    * returns a numeric decoder dictionary (num_decode)
    * returns a column decoder dictionary (col_decode)

#### histo_test

Counts the number of bins created for each combined column in the pre-processed dataframe. A useful tool for determining the optimal feature combinations.

3) **histo_test(df, combo_dict)**
    * df – the pre-processed dataframe
    * combo_dict – the combination dictionary
    * prints a count of bins for each combined column

#### create_private_histo

Creates privatized histograms of the specified combined column using a specified sample size, sensitivity and epsilon.

4) **create_private_histo(df, column, sample, sample_size, sensitivity, epsilon)**
    * df – the pre-processed dataframe
    * column – the combined column
    * sample - enter 1 to use sampling
    * sample_size – the size of the sample
    * sensitivity – the sensitivity
    * epsilon – the epsilon
    * returns population (bins) as a list
    * returns privatized weights as a list

#### col_decoder

Decodes the specified column into a its privatized value.

5) **col_decoder(num_dict, num_decode, col_decode, value, column)**
    * num_dict – the numeric dictionary
    * num_decode – the numeric decoder dictionary
    * col_decode – the column decoder dictionary
    * value – a value to decode
    * column – the column to decode
    * returns decoded privatized value

## (3) Basic Example

The Basic example is located in the **examples** directory in the **1_basic** directory.  The python file is **main.py**.  It uses a small sample of data to demonstrate the use of the five functions.

#### Basic Formatted Ground Truth

The first five rows of the **ground_truth_test.csv** are shown below:

```
taxi_id_i,shift_c,company_c,pca_c,dca_c,payment_c,fare_n,tips_n,seconds_n,miles_n
1004636,0,27,76,0,1,44,14,1440,0
1004636,0,27,8,8,0,10,0,720,0
1004636,0,27,8,8,0,5,0,240,0
1004636,0,27,8,6,1,10,2,660,0
```
- taxi_id_i = a unique taxi driver id 
- shift_c = a taxi shift number from 0-20 (categorical) 
- company_c = a company id from 0-99 (categorical) 
- pca_c = a pickup community area from 0-77 (categorical) 
- dca_c = a dropoff community area from 0-77 (catgorical) 
- payment_c = payment type from 0-9(categorical) 
- fare_n = fare paid (numeric) 
- tips_n = tips paid (numeric) 
- seconds_n = trip seconds (numeric) 
- miles_n = trip miles (numeric)

Notice the data is properly formatted.

#### Basic Sensitivity and Epsilon

The Basic sensitivity and epsilon are calculated in **main.py**:

```
number_histos = 3       # Create 3 histograms
sample = 1              # Use sampling
sample_size = 3         # Sample size equals 3
population_queries = 2  # Use 2 population queries
epsilon = 10.0          # Use an epsilon value of 10

# Calculate the sensitivity
sensitivity = (number_histos * sample_size) + population_queries
```

In this example the sensitivity is 11 and epsilon is 10.

#### Basic Combination Dictionary

The Basic combination dictionary in **main.py** is:

```
# Define the combined columns for the 3 histograms
combo_dict = {'spd': ['shift_c', 'pca_c', 'dca_c'],
              'cp': ['company_c', 'payment_c'],
              'fare': ['fare_n', 'tips_n', 'seconds_n', 'miles_n']
              }
```

For example, the **shift_c, pca_c and dca_c** columns are combined into the **spd** column.

#### Basic Numeric Dictionary

The Basic numeric dictionary in **main.py** is:

```
# Define the number dictionary for each numeric column
num_dict = {'fare_n': [50, 5, 100],
            'tips_n': [20, 2, 50],
            'seconds_n': [5000, 100, 10000],
            'miles_n': [20, 2, 50]
            }
```
For example, the fare_n column data is divided into 11 numeric bins with bins of **5** from 0-**50** (10 bins of 5) with numbers over 50 in a bin of 50-**100** (1 bin of 50).

#### 1 check_input

```
# Check if the ground truth file is properly formatted
valid = privacy.check_input(ground_truth, combo_dict, num_dict)
```
The **privacy.check_input** function checks to see if the ground truth file is properly formatted and returns 1 if True.

#### 2 preprocess

```
# Preprocess the ground truth by combining the columns and creating decodings
df, num_decode, col_decode = privacy.preprocess(ground_truth, combo_dict, num_dict)
```

The returned preprocessed data frame is:

```
     taxi_id_i      spd    cp      fare
0      1004636  1007600  1271  19172510
1      1004636  1000808  1270  12101810
2      1004636  1000808  1270  11101310
3      1004636  1000806  1271  12111710
4      1004636  1000824  1271  12111510
..         ...      ...   ...       ...
211    1004638  1192843  1270  11102810
212    1004638  1194346  1270  11101310
213    1004638  1195000  1270  11104110
214    1004638  1194250  1270  11102310
215    1004638  1195028  1270  11104010

[216 rows x 4 columns]

```

The returned numeric decoder dictionary is:

```
{'fare_n': {10: 0.0, 11: 5.0, 12: 10.0, 13: 15.0, 14: 20.0, 15: 25.0, 16: 30.0, 17: 35.0, 18: 40.0, 19: 45.0, 20: 50.0, 21: inf}, 'tips_n': {10: 0.0, 11: 2.0, 12: 4.0, 13: 6.0, 14: 8.0, 15: 10.0, 16: 12.0, 17: 14.0, 18: 16.0, 19: 18.0, 20: 20.0, 21: inf}, 'seconds_n': {10: 0.0, 11: 100.0, 12: 200.0, 13: 300.0, 14: 400.0, 15: 500.0, 16: 600.0, 17: 700.0, 18: 800.0, 19: 900.0, 20: 1000.0, 21: 1100.0, 22: 1200.0, 23: 1300.0, 24: 1400.0, 25: 1500.0, 26: 1600.0, 27: 1700.0, 28: 1800.0, 29: 1900.0, 30: 2000.0, 31: 2100.0, 32: 2200.0, 33: 2300.0, 34: 2400.0, 35: 2500.0, 36: 2600.0, 37: 2700.0, 38: 2800.0, 39: 2900.0, 40: 3000.0, 41: 3100.0, 42: 3200.0, 43: 3300.0, 44: 3400.0, 45: 3500.0, 46: 3600.0, 47: 3700.0, 48: 3800.0, 49: 3900.0, 50: 4000.0, 51: 4100.0, 52: 4200.0, 53: 4300.0, 54: 4400.0, 55: 4500.0, 56: 4600.0, 57: 4700.0, 58: 4800.0, 59: 4900.0, 60: 5000.0, 61: inf}, 'miles_n': {10: 0.0, 11: 2.0, 12: 4.0, 13: 6.0, 14: 8.0, 15: 10.0, 16: 12.0, 17: 14.0, 18: 16.0, 19: 18.0, 20: 20.0, 21: inf}}
```

The returned column decoder dictionary is:

```
{'shift_c': ['spd', 1, 3], 'pca_c': ['spd', 3, 5], 'dca_c': ['spd', 5, 7], 'company_c': ['cp', 1, 3], 'payment_c': ['cp', 3, 4], 'fare_n': ['fare', 0, 2], 'tips_n': ['fare', 2, 4], 'seconds_n': ['fare', 4, 6], 'miles_n': ['fare', 6, 8]}
```

#### 3 histo_test

```
# Print a count of the number of bins for each histogram
privacy.histo_test(df, combo_dict)
```

The histo test prints the following:

```
2021-08-10 09:51:16.368 | INFO     | privacy:histo_test:294 - number of bins in spd 198
2021-08-10 09:51:16.368 | INFO     | privacy:histo_test:294 - number of bins in cp 3
2021-08-10 09:51:16.369 | INFO     | privacy:histo_test:294 - number of bins in fare 90

```


#### 4 create_private_histo

The create_private_histo function create the privatized histograms as lists of populations and weights.

```
# Create privatized histograms for the specified column using the sample size, sensitivity and epsilon
spd_population, spd_weights = privacy.create_private_histo(df, 'spd', sample, sample_size, sensitivity, epsilon)
cp_population, cp_weights = privacy.create_private_histo(df, 'cp', sample, sample_size, sensitivity, epsilon)
fare_population, fare_weights = privacy.create_private_histo(df, 'fare', sample, sample_size, sensitivity, epsilon)
```

#### 5 col_decoder

Using the histogtams (populations and weights), a random value for a combined column is selected and decoded.

```
# Select a random combined column value from the histogram
spd_value = choices(spd_population, spd_weights)

# Decode the column values from the combined column values
shift = privacy.col_decoder(num_dict, num_decode, col_decode, spd_value[0], 'shift_c')
pca = privacy.col_decoder(num_dict, num_decode, col_decode, spd_value[0], 'pca_c')
dca = privacy.col_decoder(num_dict, num_decode, col_decode, spd_value[0], 'dca_c')
```

The values of the combined column and decoded values are:

```
spd_value [1130808]
shift 13
pca 8
dca 8
```

## (4) Sprint 3 Example

The Sprint 3 example is located in the **examples** directory in the **2_sprint3** directory.  This example demonstrates the use of the privacy functions in Sprint 3 of the [Differential Privacy Temporal Map Challenge](https://www.drivendata.co/blog/differential-privacy-winners-sprint3/)

## (5) Sprint 2 Example

The Sprint 2 example is located in the **examples** directory in the **3_sprint2** directory.  This example demonstrates the use of the privacy functions in Sprint 2 of the [Differential Privacy Temporal Map Challenge](https://www.drivendata.co/blog/differential-privacy-winners-sprint2/)

