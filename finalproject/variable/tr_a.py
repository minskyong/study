import streamlit as st
import statsmodels.api as sm
import pandas as pd
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
csv_PATH = BASE_DIR / 'data' / '월별물동량.csv'

df = pd.read_csv(csv_PATH, encoding='utf-8')


def tr_analysis ():
    st.header('환적 분석')
    st.write('환적 물동량을 분석합니다.')


tr_con = df.copy()