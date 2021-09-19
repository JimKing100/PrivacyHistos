# Imports
import privacy
import random


'''
time_add - Adds 20 minutes to a military time values

t_value - an integer in military time (0-2359)

returns new_time - an integer in military time (0-2359)
'''
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


'''
simulate_row - The row simululator which builds one simulated simulate_row

epsilon - the epsilon value
puma - the puma value
year - the year value
hhwt - the hhwt code
demo - the demo code
ageeduc - the ageeduc code
health - the health code
work - the work code
income - the income code
departs - the depart code
n_dict - the number dictionary
n_decode - the number decode dictionary
c_decode - the category decode dictionary

returns row - a dictionary of a simulated row
'''
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

    # convert puma back to original string
    temp_puma = str(puma)
    puma_len = len(temp_puma)
    front_puma = temp_puma[0:2]
    end_puma = temp_puma[2:puma_len]
    final_puma = front_puma + '-' + end_puma
    row['PUMA'] = final_puma

    row['YEAR'] = year

    # Decode HHWT
    if hhwt == 0:
        hhwt_v = random.randrange(1, 20)
    elif hhwt == 480:
        hhwt_v = random.randrange(hhwt, 500)
    else:
        hhwt_v = random.randrange(hhwt, hhwt + 20)
    row['HHWT'] = hhwt_v

    row['GQ'] = privacy.col_decoder(n_dict, n_decode, c_decode, demo, 'GQ_c')

    # PERWT = HHWT
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

    # INCWELFR = INCWAGE when INCWAGE is less than $8000
    if incwage_v < 8000:
        row['INCWELFR'] = incwage_v
    else:
        row['INCWELFR'] = 0

    row['INCINVST'] = privacy.col_decoder(n_dict, n_decode, c_decode, income, 'INCINVST_n')

    # INCEARN = INCWAGE
    row['INCEARN'] = incwage_v

    poverty = privacy.col_decoder(n_dict, n_decode, c_decode, income, 'POVERTY_n')
    # POVERTY = 501 when code is > 500
    if poverty > 500:
        poverty = 501
    row['POVERTY'] = poverty

    # Decode DEPARTS
    if departs == 0:
        departs_v = 0
    else:
        departs_v = random.randrange(departs, departs + 30)
    row['DEPARTS'] = departs_v

    # ARRIVES = DEPARTS + 20 minutes
    row['ARRIVES'] = time_add(departs_v)

    return row
