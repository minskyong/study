import pandas as pd 
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt 

from variable.o_status import overall_status
from variable.m_throughput import monthly_throughput
from variable.q_throughput import quarterly_throughput
from variable.io_a import io_analysis
from variable.tr_a import tr_analysis
from variable.s_a import season_analysis
from variable.c_data import check_data


st.set_page_config(
    page_title = 'project',
    page_icon = ('🫆'),
    layout = 'centered',
    initial_sidebar_state = 'locked'
)

# 사이드바 생성 후 목차 만들고 넣기 
menu =st.sidebar.selectbox(
    label =     '메뉴선택',

    options = [ '전체 현황',
                '월별 물동량 분석',
                '분기별 물동량 분석',
                '수출입 분석',
                '환적 분석',
                '계절성 분석',
                '데이터 확인'])

if menu == '전체 현황':
   overall_status()

elif menu == '월별 물동량 분석':
    monthly_throughput ()

elif menu == '분기별 물동량 분석':
    quarterly_throughput()

elif menu == '수출입 분석':
    io_analysis()

elif menu == '환적 분석':
    tr_analysis()

elif menu == '계절성 분석':
    season_analysis()

elif menu == '데이터 확인':
    check_data()
    
  
    

#토글 형식 눌러서 들어가기 가능  st.selectbox()


st.title('TEST')