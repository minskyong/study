import pandas as pd
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

csv_PATH = BASE_DIR / 'data' / 'container.csv'
csv_PATH2 = BASE_DIR / 'data' / '월별물동량.csv'

# 각각 실제 인코딩에 맞게 읽기
df = pd.read_csv(csv_PATH, encoding='utf-8-sig')
df2 = pd.read_csv(csv_PATH2, encoding = 'utf-8')


def check_data():

    st.header('부산 컨테이너 물동량 중심지 확인')
    st.subheader('원본데이터')
    st.dataframe(df)

    st.header('월별 물동량 확인')
    st.subheader('원본')
    st.dataframe(df2)

    st.write(df2.columns.tolist())