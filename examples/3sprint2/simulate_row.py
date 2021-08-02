# Imports
import privacy
import random


def time_conv(n):
    t = str(n)

    # Determine hour
    if len(t) < 3:
        hour = 0
    elif len(t) == 3:
        hour = int(t[0])
    else:
        hour = int(t[0:2])

    # Determine minute
    end = int(t[-2:])
    if end > 59:
        hour = hour + 1
        minute = int(end % 60)
    else:
        minute = end

    # Concatenate and test bounds
    h = str(hour).zfill(2)
    m = str(minute).zfill(2)
    result = h+m
    final = int(result)
    if final < 0:
        final = 0
    elif final > 2359:
        final = 2359
    return final


def time_add(t_value):
    n = 20
    if t_value == 0:
        new_time = 0
    else:
        s_value = str(t_value)
        if len(s_value) == 4:
            h = int(s_value[0:2])
        else:
            h = int(s_value[0:1])
        m = int(s_value[-2:])
        t = (h * 60) + m + n
        new_h = t // 60
        new_m = t % 60
        if new_m < 10:
            final_min = '0' + str(new_m)
        else:
            final_min = str(new_m)
        final_hour = str(new_h)
        new_time = int(final_hour + final_min)

    return new_time


# The row simulator - builds one simulated row
#     returns a single simulated row
def simulate_row(epsilon,
                 puma,
                 year,
                 hhwt,
                 demo,
                 ageeduc,
                 health,
                 work,
                 income,
                 departs,
                 n_dict,
                 n_decode,
                 c_decode
                 ):

    row = {}
    row['epsilon'] = epsilon
    temp_puma = str(puma)
    puma_len = len(temp_puma)
    front_puma = temp_puma[0:2]
    end_puma = temp_puma[2:puma_len]
    final_puma = front_puma + '-' + end_puma
    row['PUMA'] = final_puma
    row['YEAR'] = year
    if hhwt == 0:
        hhwt_v = random.randrange(1, 20)
    elif hhwt == 480:
        hhwt_v = random.randrange(hhwt, 500)
    else:
        hhwt_v = random.randrange(hhwt, hhwt + 20)
    # hhwt_v = utilities.col_decoder(n_dict, n_decode, c_decode, hhwt, 'HHWT_n')
    # if hhwt_v == 0:
        # hhwt_v = 1
    row['HHWT'] = hhwt_v
    row['GQ'] = privacy.col_decoder(n_dict, n_decode, c_decode, demo, 'GQ_c')
    row['PERWT'] = hhwt_v
    row['SEX'] = privacy.col_decoder(n_dict, n_decode, c_decode, demo, 'SEX_c')
    row['AGE'] = privacy.col_decoder(n_dict, n_decode, c_decode, ageeduc, 'AGE_c')
    row['MARST'] = privacy.col_decoder(n_dict, n_decode, c_decode, demo, 'MARST_c')
    row['RACE'] = privacy.col_decoder(n_dict, n_decode, c_decode, demo, 'RACE_c')
    row['HISPAN'] = privacy.col_decoder(n_dict, n_decode, c_decode, demo, 'RACE_c')
    row['CITIZEN'] = privacy.col_decoder(n_dict, n_decode, c_decode, demo, 'CITIZEN_c')
    row['SPEAKENG'] = privacy.col_decoder(n_dict, n_decode, c_decode, demo, 'SPEAKENG_c')
    row['HCOVANY'] = privacy.col_decoder(n_dict, n_decode, c_decode, health, 'HCOVANY_c')
    row['HCOVPRIV'] = privacy.col_decoder(n_dict, n_decode, c_decode, health, 'HCOVPRIV_c')
    row['HINSEMP'] = privacy.col_decoder(n_dict, n_decode, c_decode, health, 'HINSEMP_c')
    row['HINSCAID'] = privacy.col_decoder(n_dict, n_decode, c_decode, health, 'HINSCAID_c')
    row['HINSCARE'] = privacy.col_decoder(n_dict, n_decode, c_decode, health, 'HINSCARE_c')
    row['EDUC'] = privacy.col_decoder(n_dict, n_decode, c_decode, ageeduc, 'EDUC_c')
    row['EMPSTAT'] = privacy.col_decoder(n_dict, n_decode, c_decode, work, 'EMPSTAT_c')
    row['EMPSTATD'] = privacy.col_decoder(n_dict, n_decode, c_decode, work, 'EMPSTATD_c')
    row['LABFORCE'] = privacy.col_decoder(n_dict, n_decode, c_decode, work, 'LABFORCE_c')
    row['WRKLSTWK'] = privacy.col_decoder(n_dict, n_decode, c_decode, work, 'WRKLSTWK_c')
    row['ABSENT'] = privacy.col_decoder(n_dict, n_decode, c_decode, work, 'ABSENT_c')
    row['LOOKING'] = privacy.col_decoder(n_dict, n_decode, c_decode, work, 'LOOKING_c')
    row['AVAILBLE'] = privacy.col_decoder(n_dict, n_decode, c_decode, work, 'AVAILBLE_c')
    row['WRKRECAL'] = privacy.col_decoder(n_dict, n_decode, c_decode, work, 'WRKRECAL_c')
    row['WORKEDYR'] = privacy.col_decoder(n_dict, n_decode, c_decode, work, 'WORKEDYR_c')
    row['INCTOT'] = privacy.col_decoder(n_dict, n_decode, c_decode, income, 'INCTOT_n')
    incwage_v = privacy.col_decoder(n_dict, n_decode, c_decode, income, 'INCWAGE_n')
    row['INCWAGE'] = incwage_v
    if incwage_v < 8000:
        row['INCWELFR'] = incwage_v
    else:
        row['INCWELFR'] = 0
    row['INCINVST'] = privacy.col_decoder(n_dict, n_decode, c_decode, income, 'INCINVST_n')
    row['INCEARN'] = incwage_v
    poverty = privacy.col_decoder(n_dict, n_decode, c_decode, income, 'POVERTY_n')
    if poverty > 500:
        poverty = 501
    row['POVERTY'] = poverty
    # time_v = utilities.col_decoder(n_dict, n_decode, c_decode, departs, 'DEPARTS_n')
    # departs_v = time_conv(time_v)
    if departs == 0:
        departs_v = 0
    else:
        departs_v = random.randrange(departs, departs + 30)
    row['DEPARTS'] = departs_v
    row['ARRIVES'] = time_add(departs_v)

    return row
