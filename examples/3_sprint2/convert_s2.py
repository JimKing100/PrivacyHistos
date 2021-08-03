import pandas as pd
from pathlib import Path

# Set root and data directories
ROOT_DIRECTORY = Path("/Users/JKMacBook/Documents/Lambda/Product1/PrivacyHistos")
DATA_DIRECTORY = ROOT_DIRECTORY / "data"
ground_truth_file = DATA_DIRECTORY / "ground_truth_2.csv"
output_file = DATA_DIRECTORY / "ground_truth_s2.csv"

# Read in the raw ground truth
df = pd.read_csv(ground_truth_file)

# Encode strings as integers
df['PUMA'] = df['PUMA'].str.replace('-', '')
df['PUMA'] = df['PUMA'].astype(int)
df['HHWT'] = df['HHWT'].astype(int)
df[df < 0] = 0

# Drop unneeded columns
new_df = df.drop(['PERWT', 'ARRIVES', 'INCEARN', 'INCWELFR'], axis=1)

# Rename columns following the guidelines
col_dict = {'PUMA': 'PUMA_x',
            'YEAR': 'YEAR_x',
            'HHWT': 'HHWT_x',
            'GQ': 'GQ_c',
            'SEX': 'SEX_c',
            'AGE': 'AGE_c',
            'MARST': 'MARST_c',
            'RACE': 'RACE_c',
            'HISPAN': 'HISPAN_c',
            'CITIZEN': 'CITIZEN_c',
            'SPEAKENG': 'SPEAKENG_c',
            'HCOVANY': 'HCOVANY_c',
            'HCOVPRIV': 'HCOVPRIV_c',
            'HINSEMP': 'HINSEMP_c',
            'HINSCAID': 'HINSCAID_c',
            'HINSCARE': 'HINSCARE_c',
            'EDUC': 'EDUC_c',
            'EMPSTAT': 'EMPSTAT_c',
            'EMPSTATD': 'EMPSTATD_c',
            'LABFORCE': 'LABFORCE_c',
            'WRKLSTWK': 'WRKLSTWK_c',
            'ABSENT': 'ABSENT_c',
            'LOOKING': 'LOOKING_c',
            'AVAILBLE': 'AVAILBLE_c',
            'WRKRECAL': 'WRKRECAL_c',
            'WORKEDYR': 'WORKEDYR_c',
            'INCTOT': 'INCTOT_n',
            'INCWAGE': 'INCWAGE_n',
            'INCINVST': 'INCINVST_n',
            'POVERTY': 'POVERTY_n',
            'DEPARTS': 'DEPARTS_x',
            'sim_individual_id': 'sim_individual_id_i',
            }
new_df = new_df.rename(columns=col_dict)

# Write the results to the formatted ground truth file
new_df.to_csv(output_file, index=False)
