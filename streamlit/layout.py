import streamlit as st
import pandas as pd 
import numpy as np


# 
st.set_page_config(          
  page_title = '부산항​​', 
  page_icon = ('🚢' ), 
  layout = 'centered',
  initial_sidebar_state = 'locked'
)
with st.sidebar:
    st.title('북항')
    st.write('북항 대시보드')
    st.title('신항')
    st.write('신항 대시보드')

#토글 형식 눌러서 들어가기 가능  st.selectbox()

    st.selectbox(label =' 부두 종류', options = ['신항1부두','신항2부두'])

   

st.title('스마트항만 대시보드')


data = pd.DataFrame(
    {
        '상품' : ['키보드',
                '모니터',
                '마우스'],
        '판매량' : [
                    10,
                    20,
                    30]
            }
)
#st.dataframe(data, hide_index = True)

#컬럼 위치 수정 방법 
#fig, ax
col1 , col2, col3 = st.columns(3)


with col1:
    st.write('a')

with col2:
    st.write('b')

with col3 :
    st.write('c')





sales_kpi , orders_kpi, customers_kpi = st.columns(3)

with sales_kpi:
    with st.container(border =True):
        st.subheader('매출')
        st.metric(label ='오늘매출',
              value = '35,000,000원')

with orders_kpi:
    with st.container(border = True):
        st.subheader('주문')
        st.metric(label ='오늘 주문 수', 
              value = '1,250건')


with customers_kpi:
    with st.container(border = True):
        st.subheader('고객 수')
        st.metric(label ='오늘 고객 수',
              value = '874명')


left, right = st.columns([2, 1])

with left : 
    st.subheader('넓은 영역')
    st.write('상대적으로 넓다.')

with right : 
    st.subheader('좁은영역')
    st.write('상대적으로 좁음')



left,center, right = st.columns([1, 2, 1])

with left : 
    st.subheader('왼')
    st.write('1.')

with center : 
    st.subheader('중간')
    st.write('2')
with right : 
    st.subheader('오')
    st.write('1')


st.write('---')

st.write('컨테이너 밖')
container1 = st.container(border = True)

with container1 :
    st.subheader('매출정보')
    st.write('총매출 : 35,000,000원')
    st.write('1,250건')

st.write('컨테이너 밖')


st.write('---')



sales_kpi , orders_kpi, customers_kpi = st.columns(3)

with sales_kpi:
    with st.container(border =True):
        st.subheader('매출')
        st.metric(label ='오늘매출',
              value = '35,000,000원')

with orders_kpi:
    with st.container(border = True):
        st.subheader('주문')
        st.metric(label ='오늘 주문 수', 
              value = '1,250건')


with customers_kpi:
    with st.container(border = True):
        st.subheader('고객 수')
        st.metric(label ='오늘 고객 수',
              value = '874명')


result_area = st.container(border = True)
result_area.subheader('분석결과')
result_area.metric(label = '분석 결괴', value = '오늘 고객수 874명')

with st.expander('자세히보기'):   #토글형식 expander
    st.write('배고프다')


df_area  = st.container(border = True)
with df_area:
    sales_df = pd.DataFrame({
        '지역' : ['서울', '서울','대전','대전','부산','부산'],
        '상품' : ['모니터','모니터','키보드','키보드','모니터','키보드'],
        '매출' : [4_500_000,4_500_000,1_500_000,1_500_000,4_500_500,1_500_000],
    })


