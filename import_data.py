'''
시뮬레이션 데이터 전처리 모듈
'''

#-*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import sqlite3
import os

# 포트폴리오 읽어들인 후 리스트로 변환
# In : 포트폴리오 No.(str)
# Out : 포트폴리오 리스트(list)
def read_pf_list(*pf_number):      
    pf_list = list(pf_number)[0].split()
    return pf_list


# 엑셀 데이터 엑세스
# in : 포트폴리오 번호 (int)
# out : 포트폴리오 전체 데이터 (Dataframe)
def excess_csv_data(pf_num):

    ## CSV 파일로 접근
    filepath = "trade_history_daily_" + pf_num + '.csv'    
    trade_data = pd.read_csv(filepath, header=0)
    
    return trade_data


# 시뮬레이션용 데이터 생성
# in : 포트폴리오 리스트
# out : 포트폴리오 수익률 데이터(Dataframe) 
def import_simulation_data(pf_list):
    
    # DB 파일 연결
    con_input = sqlite3.connect("input_data.db")
    
    # 전처리 데이터 저장용 데이터프레임 제작
    df = pd.DataFrame()

    # 날짜, 년월 데이터 적재
    df = pd.concat([df, pd.read_sql("SELECT Date FROM Raw_%s" %pf_list[0], con_input, index_col=None)])
    df['YearMonth'] = df['Date'].astype(str).str.slice(stop=6)
        
    ## import profit_data and log data
    for pf_num in pf_list:
        df['Profit_day_%s' %pf_num] = pd.read_sql("SELECT 일일수익률 FROM Raw_%s" %pf_num, con_input, index_col=None).astype(float)
        df['Profit_tot_%s' %pf_num] = pd.read_sql("SELECT 누적수익률 FROM Raw_%s" %pf_num, con_input, index_col=None).astype(float)
        
        ### 로그수익률 구하는 방법 : log(전날 누적수익률 / 오늘 누적수익률) 
        temp = df['Profit_tot_%s' %pf_num]
        df['Log_%s' %pf_num] = np.log(temp/temp.shift(1)).astype(float)   
    
    ## 전처리 데이터 리턴
    return df


# SQLite3 Database 데이터로 저장
# in : pf_list
# out : X (Database 파일 저장)
def store_data(pf_list):

    # 기존 파일 삭제
    try:
        print("< Delete Previous data... >")
        os.remove("input_data.db") 
        os.remove("result_data.db") 

    except:
        pass

    con = sqlite3.connect("input_data.db")

    # 데이터 적재
    for pf_num in pf_list:
        data_raw = excess_csv_data(pf_num).rename(columns = {'날짜': 'Date'})
        data_raw.to_sql('Raw_%s' %pf_num, con)

    # 전처리 데이터 저장
    data_preprocess = import_simulation_data(pf_list)
    data_preprocess.to_sql('Preprocess' , con)

    # End
    print("< Store >")   
    return True


# SQLite3 Database 데이터로 저장
# in : pf_num
# out : 주가 데이터 (DataFrame)
def extract_data(pf_num):

    ## DB 연결
    con_input = sqlite3.connect("input_data.db")
    
    ## 데이터 호출
    df = pd.read_sql("SELECT Date, 일일수익률 FROM Raw_%s" %pf_num, con_input, index_col=None)

    ## 리턴
    return df


# 모듈 테스트용
# 최근 테스트일 : 2019.08.25 (정상)
if __name__ == "__main__":
    print("Preprocess Modeule Test")
    pf_str = input("포트 번호 :")

    pf_list = read_pf_list(pf_str)
    store_data(pf_list)
