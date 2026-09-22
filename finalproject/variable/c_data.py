import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
csv_PATH = BASE_DIR / 'data' / 'container.csv'

df = pd.read_csv(csv_PATH, encoding='utf-8')

def check_data():

    st.header('부산 컨테이너 물동량 중심지 확인')
    st.subheader('원본데이터')
    st.dataframe(df)



