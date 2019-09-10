import pandas as pd
import numpy as np


# 시뮬레이션 데이터프레임 추출
def extract_sim_data(df_sim_table, df_input, i):

    temp = []

    start_idx = df_sim_table['Start'].iat[i]
    end_idx = df_sim_table['Start'].iat[i] + df_sim_table['Inv_time'].iat[i]
        
    df_trade = df_input.loc[start_idx : end_idx]

    return df_trade


# 결과 DataFrame 생성
def get_df_result(df_trade):
    
    df_result = pd.DataFrame()

    ## 성과 계산용 지표 저장
    df_result['Date'] = df_trade['Date']
    df_result['일일수익률'] = df_trade['일일수익률']
    df_result['누적수익률'] = df_result['일일수익률'].div(100).add(1).cumprod().astype(float)
    df_result['최고누적'] = df_result['누적수익률'].rolling(min_periods=1, window=100).max()
    df_result['DD'] = df_result['누적수익률'] / df_result['최고누적'] -1
    df_result['MDD'] = df_result['DD'].rolling(min_periods=1, window=len(df_trade.index)).min()

    df_result['cummax'] = df_result['누적수익률'].cummax()
    df_result['underwater'] = df_result['누적수익률'] < df_result['cummax']
    df_result['win'] = df_result['일일수익률'] > 0
    
    ## 셋째자리에서 반올림
    return df_result.round(4)


# 결과값 Array 산출
def get_array_result(df_result):
    
    df = pd.DataFrame()
    start_date = df_result['Date'].iat[0]
    end_date = df_result['Date'].iat[-1]

    result_return = (df_result['누적수익률'].iat[-1] - 1) * 100
    avg_day_profit = round(df_result['일일수익률'].mean(), 2)
    max_underwater = count_max_underwater(df_result)

    HL_ratio = round(df_result.win.sum() / len(df_result.index) * 100, 2)
    
    return [start_date, end_date, result_return, avg_day_profit, max_underwater, HL_ratio]
    

## Underwater Period 산출
def count_max_underwater(df):
    temp = []

    for i in range(len(df.index)):
        if df["underwater"].iat[i] == np.bool_(True):
            if(i == 0):
                temp.append(1)

            else:
                temp.append(temp[i-1] + 1)
        else:
            temp.append(0)

    return max(temp)


def draw_graph(df_result_table):
    print('Average Day Profit : %.2f%%' %result_table['day_profit_AVG'].mean())
    print('Average Total Profit : %.2f%%' %result_table['total_profit'].mean())
    print('Average Hit Ratio : %.2f%%' %result_table['HL_ratio'].mean())
    print('Average Underwater : %.2f Days' %result_table['Underwater'].mean())
    
    plt.scatter(result_table['day_profit_AVG'], result_table['HL_ratio'], label='%s' %array_pf[0])
    plt.xlabel('Day_profit')
    plt.ylabel('Hit_ratio')
    plt.legend(loc='upper left')

    plt.show()

    return True