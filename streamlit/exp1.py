import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(
    layout = 'wide'
)
sales_df = pd.DataFrame({
            '상품' : ['모니터',
                    '키보드',
                    '모니터',],
            '판매량' : [3,8,10],

            '매출' : [4_500_000,
                     500_000,
                     1_500_000,
                    ]
} )

st.dataframe(sales_df,hide_index = True)


total_sales = sales_df['매출'].sum()
total_quantity = sales_df['판매량'].sum()
average_sales = sales_df['매출'].mean()


max_product = sales_df.loc[
                sales_df['매출'].idxmax(),
                '상품']


col1,col2,col3,col4 = st.columns(4)

col1.metric(
    label = '총매출',
    value = f'{total_sales:}원',
    border = True 
)

col2.metric(
    label = '총판매량',
    value = f'{total_quantity:}개',
    border = True 
)

col3.metric(
    label = '평균매출',
    value = f'{average_sales:.0f}원',
    border = True 
)

col4.metric(
    label = '최고매출 상품',
    value = max_product,
    border = True 
)