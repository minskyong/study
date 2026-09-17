import pandas as pd
import streamlit as st
import plotly.express as px

csv_PATH = r'C:\work\finalproject\data\container.csv'
origin = pd.read_csv(csv_PATH, encoding='utf-8')
origin.dtypes

def check_data():

    
    df = pd.read_csv(csv_PATH, encoding='utf-8')

    st.header('컨테이너 물동량')
    

    # 데이터 선택
    data_menu = st.selectbox(
       label = '데이터',
       options = ['원본', '가공']
    )

    # 원본 / 가공 선택
    if data_menu == '원본':

        st.subheader('원본 데이터')
        st.dataframe(
            df,
            use_container_width=True
        )

    elif data_menu == '가공':

        # 원본을 복사해서 가공용 데이터프레임 생성
        df1 = df.copy()

        
       
       
        df1 = df1[df1['년도'] >=2012]
        df1 = df1[['년도','합계']]
        st.subheader('가공 데이터')
        st.dataframe(
            df1, hide_index = True,
            use_container_width=True
        )
        st.write('2012년 미만 자료 삭제')

      
    fig = px.line(
        df1,
        x='년도',
        y='합계',
     markers=True
)
    fig.update_xaxes(
    tickmode='linear',
    dtick=1
    )
    fig.update_yaxes(
        range=[
            df1['합계'].min(),
            df1['합계'].max()
    ]
)

    st.plotly_chart(
        fig,
        use_container_width=True
)