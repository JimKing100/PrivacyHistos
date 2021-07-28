import privacy


# Create two concurrent lists representing a split row
#   - row is the front end of the row with sec_estimate faredecode_dict
#   - row1 is the back end of the row
def simulate_row(epsilon, taxi_id, spd, cp, fr, pd, n_dict, n_decode, c_decode):
    row = {}
    row1 = {}

    # Create row = epsilon, taxi_id, shift, company_id, pcs, dca, payment_type, sec_estimate
    row['epsilon'] = epsilon
    row['taxi_id'] = taxi_id
    row['shift'] = privacy.col_decoder(n_dict, n_decode, c_decode, spd, 'shift_c')
    row['company_id'] = privacy.col_decoder(n_dict, n_decode, c_decode, cp, 'company_c')

    pca = privacy.col_decoder(n_dict, n_decode, c_decode, spd, 'pca_c')
    tpca = pca
    if pca == 0:
        pca = -1
    row['pickup_community_area'] = pca

    dca = privacy.col_decoder(n_dict, n_decode, c_decode, spd, 'dca_c')
    tdca = dca
    if dca == 0:
        dca = -1
    row['dropoff_community_area'] = dca

    pay = privacy.col_decoder(n_dict, n_decode, c_decode, cp, 'payment_c')
    if pay == 9:
        pay = -1
    row['payment_type'] = pay

    pca_dca = str(tpca).zfill(2) + str(tdca).zfill(2)
    sec_estimate = pd[pca_dca]
    row['sec_estimate'] = sec_estimate

    # Create row1 = fare, tips, trip_total, trip_seconds, trip_miles
    fare = privacy.col_decoder(n_dict, n_decode, c_decode, fr, 'fare_n')
    row1['fare'] = fare
    tips = privacy.col_decoder(n_dict, n_decode, c_decode, fr, 'tips_n')
    row1['tips'] = tips
    row1['trip_total'] = fare + tips
    row1['trip_seconds'] = privacy.col_decoder(n_dict, n_decode, c_decode, fr, 'seconds_n')
    row1['trip_miles'] = privacy.col_decoder(n_dict, n_decode, c_decode, fr, 'miles_n')

    return row, row1
