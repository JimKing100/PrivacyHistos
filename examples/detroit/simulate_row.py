# Imports
import privacy


# The row simulator - builds one simulated row
#     returns a single simulated row
def simulate_row(incident,
                 type,
                 injury,
                 call,
                 result,
                 n_dict,
                 n_decode,
                 c_decode
                 ):

    row = {}
    row['incident_i'] = incident + 1
    row['engine_area_c'] = privacy.col_decoder(n_dict, n_decode, c_decode, type, 'engine_area_c')
    row['exposure_c'] = privacy.col_decoder(n_dict, n_decode, c_decode, type, 'exposure_c')
    row['incident_type_c'] = privacy.col_decoder(n_dict, n_decode, c_decode, type, 'incident_type_c')
    row['property_use_c'] = privacy.col_decoder(n_dict, n_decode, c_decode, type, 'property_use_c')
    row['detector_c'] = privacy.col_decoder(n_dict, n_decode, c_decode, type, 'detector_c')
    row['structure_stat_c'] = privacy.col_decoder(n_dict, n_decode, c_decode, type, 'structure_stat_c')
    row['cinjury_c'] = privacy.col_decoder(n_dict, n_decode, c_decode, injury, 'cinjury_c')
    row['cfatal_c'] = privacy.col_decoder(n_dict, n_decode, c_decode, injury, 'cfatal_c')
    row['finjury_c'] = privacy.col_decoder(n_dict, n_decode, c_decode, injury, 'finjury_c')
    row['ffatal_c'] = privacy.col_decoder(n_dict, n_decode, c_decode, injury, 'ffatal_c')
    row['call_month_c'] = privacy.col_decoder(n_dict, n_decode, c_decode, call, 'call_month_c')
    row['call_day_c'] = privacy.col_decoder(n_dict, n_decode, c_decode, call, 'call_day_c')
    row['call_hour_c'] = privacy.col_decoder(n_dict, n_decode, c_decode, call, 'call_hour_c')
    row['dispatch_n'] = privacy.col_decoder(n_dict, n_decode, c_decode, result, 'dispatch_n')
    row['arrival_n'] = privacy.col_decoder(n_dict, n_decode, c_decode, result, 'arrival_n')
    row['clear_n'] = privacy.col_decoder(n_dict, n_decode, c_decode, result, 'clear_n')

    return row
