import pandas as pd
from loguru import logger

import privacy


# Create the proximity dictionary
def proximity(df):
    lookup_df = pd.crosstab(df['pca_c'],
                            df['dca_c'],
                            values=df['seconds_n'],
                            aggfunc='mean')
    lookup_df = lookup_df.fillna(0)
    lookup_df = lookup_df.reset_index(drop=True)
    lookup_df = lookup_df.rename(columns={-1: 0})
    prox_dict = {}
    for i in range(78):
        for j in range(78):
            p_key = str(i).zfill(2)
            d_key = str(j).zfill(2)
            key = p_key + d_key
            value = int(lookup_df[j][i])
            prox_dict[key] = value
    return prox_dict


# Create the raw weights for trips
def raw_weight_trips(df, c, m):

    ilist = []
    for i in range(1, (m + 1)):
        ilist.append(i)
    new_df = pd.Series(0, index=ilist)

    taxis = df[c].unique().tolist()
    taxi_counts = df[c].value_counts()
    t_counter = 0
    for taxi in taxis:
        trip_count = taxi_counts[taxi]

        t_counter += 1
        if t_counter % 10000 == 0:
            logger.info(f"processing {t_counter} drivers for trips")
        new_df[trip_count] += 1

    return new_df


# Privatize the weights for trips
def privatize_trips(df, sensitivity, m, epsilon):

    for i in range(1, (m + 1)):
        df[i] = privacy.laplaceMechanism(df[i], sensitivity, epsilon)

    for i in range(1, (m + 1)):
        if df[i] < 0:
            df[i] = 0

    final_df = df / df.sum()
    w = []
    for i in range(1, (m + 1)):
        w.append(final_df[i])

    return w


# Create the weights for the trips
def create_trips_histo(df, col, sensitivity, epsilon, mr, ec):
    global taxi_rw

    taxi_pop = [x + 1 for x in range(mr)]
    taxi_pop.sort()

    if ec == 1:
        taxi_rw = raw_weight_trips(df, col, mr)

    taxi_w = privatize_trips(taxi_rw, sensitivity, mr, epsilon)

    return taxi_pop, taxi_w
