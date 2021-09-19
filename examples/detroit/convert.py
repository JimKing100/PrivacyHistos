import pandas as pd
from datetime import datetime
from pathlib import Path

ROOT_DIRECTORY = Path("/Users/JKMacBook/Documents/Lambda/Product1/PrivacyHistos")
DATA_DIRECTORY = ROOT_DIRECTORY / "data"
raw_data_file = DATA_DIRECTORY / "2015_fire_data.csv"
output_file = DATA_DIRECTORY / "ground_truth_detroit.csv"

# Read the raw data
raw_data = pd.read_csv(raw_data_file)

# Columns for the converted data
new_columns = ['incident_i',
               'engine_area_c',
               'exposure_c',
               'incident_type_c',
               'property_use_c',
               'detector_c',
               'structure_stat_c',
               'cinjury_c',
               'cfatal_c',
               'finjury_c',
               'ffatal_c',
               'call_month_c',
               'call_day_c',
               'call_hour_c',
               'dispatch_n',
               'arrival_n',
               'clear_n'
               ]

# Create and sort the new dataframe
df = pd.DataFrame(columns=new_columns)

# Create the synthetic incident_i columns
raw_data = raw_data.sort_values(by=['DATE OF CALL', 'TIME OF CALL'])
raw_data = raw_data.reset_index(drop=True)
df['incident_i'] = range(1, 1+len(raw_data))

# Clean up and create the engine_area_c column
raw_data['ENGINE AREA'] = raw_data['ENGINE AREA'].fillna('E00')
df['engine_area_c'] = raw_data['ENGINE AREA'].str.slice(1, 3).astype(int)

# Create the exposure_c column
df['exposure_c'] = raw_data['EXPOSURE'].apply(lambda x: 0 if x == 'No' else 1)

# Clean up and create the incident_type_c column
raw_data['INCIDENT TYPE'] = raw_data['INCIDENT TYPE'].fillna('000 - none')
df['incident_type_c'] = raw_data['INCIDENT TYPE'].str.slice(0, 3).astype(int)

# Create the property_use_c column
temp_dict = dict(enumerate(raw_data['PROPERTY USE'].unique()))
property_dict = dict((v, k) for k, v in temp_dict.items())
df['property_use_c'] = raw_data['PROPERTY USE'].map(property_dict)

# Create the detector_c column
raw_data['DETECTOR'] = raw_data['DETECTOR'].fillna('None')
temp_dict = dict(enumerate(raw_data['DETECTOR'].unique()))
detector_dict = dict((v, k) for k, v in temp_dict.items())
df['detector_c'] = raw_data['DETECTOR'].map(detector_dict)

# Create the structure_stat_c column
raw_data['STRUCTURE STATUS'] = raw_data['STRUCTURE STATUS'].fillna('None')
temp_dict = dict(enumerate(raw_data['STRUCTURE STATUS'].unique()))
structure_dict = dict((v, k) for k, v in temp_dict.items())
df['structure_stat_c'] = raw_data['STRUCTURE STATUS'].map(structure_dict)

# Create the cinjury_c, cfatal_c, finjury_c and ffatal_c columns
df['cinjury_c'] = raw_data['CIVILIAN INJURY']
df['cfatal_c'] = raw_data['CIVILIAN FATALITY']
df['finjury_c'] = raw_data['FIRE PERSONNEL INJURY']
df['ffatal_c'] = raw_data['FIRE PERSONNEL FATALITY']

# Convert DATE and TIME OF CALL to datetime dt_call
format = '%m/%d/%Y %I:%M:%S %p'
raw_data['call_time'] = raw_data.apply(lambda row: row['TIME OF CALL']
                                       if len(row['TIME OF CALL']) == 11
                                       else '0' + row['TIME OF CALL'], axis=1)
raw_data['dt'] = raw_data['DATE OF CALL'] + ' ' + raw_data['call_time']
raw_data['dt_call'] = raw_data['dt'].apply(lambda x: datetime.strptime(x, format))

# Clean up DATE AND TIME columns
raw_data['DATE OF DISPATCH'] = raw_data['DATE OF DISPATCH'].fillna(raw_data['DATE OF CALL'])
raw_data['TIME OF DISPATCH'] = raw_data['TIME OF DISPATCH'].fillna(raw_data['TIME OF CALL'])
raw_data['DATE OF ARRIVAL'] = raw_data['DATE OF ARRIVAL'].fillna(raw_data['DATE OF CALL'])
raw_data['TIME OF ARRIVAL'] = raw_data['TIME OF ARRIVAL'].fillna(raw_data['TIME OF CALL'])
raw_data['DATE UNIT CLEARED'] = raw_data['DATE UNIT CLEARED'].fillna(raw_data['DATE OF CALL'])
raw_data['TIME UNIT CLEARED'] = raw_data['TIME UNIT CLEARED'].fillna(raw_data['TIME OF CALL'])

# Convert DATE and TIME OF DISPATCH to datetime dt_disp
raw_data['disp_time'] = raw_data.apply(lambda row: row['TIME OF DISPATCH']
                                       if len(row['TIME OF DISPATCH']) == 11
                                       else '0' + row['TIME OF DISPATCH'], axis=1)
raw_data['dt_d'] = raw_data['DATE OF DISPATCH'] + ' ' + raw_data['disp_time']
raw_data['dt_disp'] = raw_data['dt_d'].apply(lambda x: datetime.strptime(x, format))

# Convert DATE and TIME OF ARRIVAL to datetime dt_arr
raw_data['arr_time'] = raw_data.apply(lambda row: row['TIME OF ARRIVAL']
                                      if len(row['TIME OF ARRIVAL']) == 11
                                      else '0' + row['TIME OF ARRIVAL'], axis=1)
raw_data['dt_a'] = raw_data['DATE OF ARRIVAL'] + ' ' + raw_data['arr_time']
raw_data['dt_arr'] = raw_data['dt_a'].apply(lambda x: datetime.strptime(x, format))

# Convert DATE and TIME UNIT CLEARED to datetime dt_clr
raw_data['clr_time'] = raw_data.apply(lambda row: row['TIME UNIT CLEARED']
                                      if len(row['TIME UNIT CLEARED']) == 11
                                      else '0' + row['TIME UNIT CLEARED'], axis=1)
raw_data['dt_c'] = raw_data['DATE UNIT CLEARED'] + ' ' + raw_data['clr_time']
raw_data['dt_clr'] = raw_data['dt_c'].apply(lambda x: datetime.strptime(x, format))

# Create call_month_c, call_day_c, call_hour_c, call_minute_c
df['call_month_c'] = raw_data['dt_call'].apply(lambda x: x.month)
df['call_day_c'] = raw_data['dt_call'].apply(lambda x: x.day)
df['call_hour_c'] = raw_data['dt_call'].apply(lambda x: x.hour)

# Create dispatch_n
raw_data['call_disp'] = raw_data['dt_disp'] - raw_data['dt_call']
df['dispatch_n'] = raw_data['call_disp'].apply(lambda x: int(x.total_seconds()))
df['dispatch_n'] = df['dispatch_n'].mask(df['dispatch_n'] < 0, 0)
df['dispatch_n'] = df['dispatch_n'].mask(df['dispatch_n'] > 10000, 10000)

# Create arrival_n
raw_data['call_arr'] = raw_data['dt_arr'] - raw_data['dt_call']
df['arrival_n'] = raw_data['call_arr'].apply(lambda x: int(x.total_seconds()))
df['arrival_n'] = df['arrival_n'].mask(df['arrival_n'] < 0, 0)
df['arrival_n'] = df['arrival_n'].mask(df['arrival_n'] > 10000, 10000)

# Create clear_n
raw_data['call_clr'] = raw_data['dt_clr'] - raw_data['dt_call']
df['clear_n'] = raw_data['call_clr'].apply(lambda x: int(x.total_seconds()))
df['clear_n'] = df['clear_n'].mask(df['clear_n'] < 0, 0)
df['clear_n'] = df['clear_n'].mask(df['clear_n'] > 20000, 20000)

# Create the synthetic incident_i columns
df = df.sort_values(by=['call_month_c', 'call_day_c', 'call_hour_c'])
df = df.reset_index(drop=True)
df['incident_i'] = range(1, 1+len(df))

df.to_csv(output_file, index=False)
