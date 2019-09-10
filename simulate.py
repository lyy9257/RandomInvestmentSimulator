import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

import import_data as im
import result

# 시뮬레이션용 테스트 테이블 생성
def make_simulation_df(df_input, min_inv_time, max_inv_time, sim_count):
    
    temp = []

    ## 시뮬레이션 카운트만큼 랜덤 비중 생성
    for i in range(sim_count):
        start_index = random.randrange(0, len(df_input.index) - max_inv_time)
        inv_time = random.randrange(min_inv_time, max_inv_time)
        temp.append([start_index, inv_time])

    df_sim_table = pd.DataFrame(temp, columns = ['Start', 'Inv_time'])

    return df_sim_table


# 시뮬레이션
def simulate(df_sim_table, df_input):
    
    print('< Simulate >')

    temp = []
    
    for i in range(len(df_sim_table.index)):
        ## print("(%d / %d)" %(i+1, len(df_sim_table.index)))

        df_trade = result.extract_sim_data(df_sim_table, df_input, i) 
        df_result = result.get_df_result(df_trade)
        array_result = result.get_array_result(df_result)

        temp.append(array_result)
    
    column_array = ['Start', 'End', 'total_profit','day_profit_AVG', 'Underwater', 'HL_ratio']
    df_res_table = pd.DataFrame(temp, columns = column_array)

    print(df_res_table)

    return df_res_table


if __name__ == '__main__':
    str_pf = input("포트 번호 입력 :")

    array_pf = im.read_pf_list(str_pf)
    im.store_data(array_pf)

    df_input = im.extract_data(array_pf[0])

    sim_table = make_simulation_df(df_input, 20, 60, 500)
    result_table = simulate(sim_table, df_input)

    print('Average Day Profit : %.2f%%' %result_table['day_profit_AVG'].mean())
    print('Average Total Profit : %.2f%%' %result_table['total_profit'].mean())
    print('Average Hit Ratio : %.2f%%' %result_table['HL_ratio'].mean())
    print('Average Underwater : %.2f Days' %result_table['Underwater'].mean())
    
    plt.scatter(result_table['day_profit_AVG'], result_table['HL_ratio'], label='%s' %array_pf[0])
    plt.xlabel('Day_profit')
    plt.ylabel('Hit_ratio')
    plt.legend(loc='upper left')

    plt.show()