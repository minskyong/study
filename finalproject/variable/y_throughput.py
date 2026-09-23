import statsmodels.api as sm
import pandas as pd
import streamlit as st
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
csv_PATH = BASE_DIR / 'data' / 'container.csv'

df = pd.read_csv(csv_PATH, encoding='utf-8')

def year_throughput():

    st.title('부산 컨테이너 물동량 중심지 확인')
    st.header('2012년 이후 데이터만 추출')
    st.subheader('12년도 이전 데이터에 표본이 부족한 부두가 다수 존재')
    st.write('  \n')
    
    # --------------------------------
    # 원본 데이터
    # --------------------------------
    
    st.subheader('부두별 물동량 데이터')
   
    st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )
    
    # --------------------------------
    # 가공 데이터
    # --------------------------------

    st.write('---')

   
        # 원본을 복사해서 가공용 데이터프레임 생성
    df1 = df.copy()

    # 2012년 미만 자료 삭제
    df1 = df1[df1['년도'] >= 2012]

    # 필요한 컬럼만 선택
    df1 = df1[['년도', '합계']]

    st.subheader('부산 물동량 연간 총합(12년~24년)')

    st.dataframe(
        df1,
        hide_index=True,
        use_container_width=True
    )
    st.write('---')
    
    st.subheader('연도별 전체 물동량')
    # --------------------------------
    # 전체 물동량 선그래프
    # --------------------------------
    col1, col2 = st.columns(2)


# ========================================
# 왼쪽 : 선그래프
# ========================================

    with col1:

        fig_line = px.line(
        df1,
        x='년도',
        y='합계',
        markers=True
    )

    # X축 : 2012 ~ 2024 모든 연도 표시
        fig_line.update_xaxes(
            tickmode='linear',
            tick0=2012,
            dtick=1
        )

        # Y축 : 실제 최소값 ~ 최대값
        fig_line.update_yaxes(
            range=[
                df1['합계'].min(),
                df1['합계'].max()
            ]
        )

        fig_line.update_layout(
            
            xaxis_title='년도',
            yaxis_title='물동량',
            height=350
        )

       

        st.plotly_chart(
            fig_line,
            use_container_width=True
        )


# ========================================
# 오른쪽 : 막대그래프
# ========================================

    with col2:

        fig_bar = px.bar(
        df1,
        x='년도',
        y='합계'
    )

    # X축 : 2012 ~ 2024 모든 연도 표시
        fig_bar.update_xaxes(
            tickmode='linear',
            tick0=2012,
            dtick=1
        )

        # Y축 : 0 ~ 최대값
        fig_bar.update_yaxes(
            range=[
                0,
                df1['합계'].max()
            ]
        )

        fig_bar.update_layout(
            xaxis_title='년도',
            yaxis_title='물동량',
            height=350
        )

        

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )
    
    # ========================================
    # 부두별 물동량 분석
    # ========================================

    
    st.write('---')
    # 원본 복사-
    new_port = df.copy()

    # 2012년 이후 자료만 사용
    new_port = new_port[
        new_port['년도'] >= 2012
    ]

    # --------------------------------
    # 신항 1~5부두 합치기
    # --------------------------------

    new_port['신항부두'] = new_port[
        [
            '신항1부두',
            '신항2부두',
            '신항3부두',
            '신항4부두',
            '신항5부두'
        ]
    ].sum(axis=1)

    # 기존 신항 1~5부두 컬럼 삭제
    new_port = new_port.drop(
        columns=[
            '신항1부두',
            '신항2부두',
            '신항3부두',
            '신항4부두',
            '신항5부두'
        ]
    )


    # 부두별 필요한 컬럼만 선택
    
    port_columns = [
        '년도',
        '합계',
        '자성대부두',
        '신선대부두',
        '감만부두',
        '우암부두',
        '감천한진',
        '신감만부두',
        '일반부두',
        '다목적부두등',
        '신항부두'
    ]

    new_port = new_port[port_columns]


   
    # 부두별 데이터 확인
    

   

   


   
    # 부두별 물동량 선그래프
    
    fig_port = px.line(
        new_port,
        x='년도',
        y=[
            '자성대부두',
            '신선대부두',
            '감만부두',
            '우암부두',
            '감천한진',
            '신감만부두',
            '일반부두',
            '다목적부두등',
            '신항부두'
        ],
        markers=True
    )

    # X축 : 2012 ~ 2024
    fig_port.update_xaxes(
        tickmode='linear',
        dtick=1
    )

    fig_port.update_layout(
        xaxis_title='년도',
        yaxis_title='물동량',
        legend_title='부두'
    )

    st.subheader('전체 부두별 물동량 추이')

    st.plotly_chart(
        fig_port,
        use_container_width=True
    )
    st.write('신항은 양이 많아 상승.하락 곡선이 잘 보임')
    st.write('신항 제외 다른 항구는 신항대비 양이 적어 상승.하락 곡선이 잘 보이지 않음')
    st.write('---')
    


    fig_port = px.line(
            new_port,
            x='년도',
            y=[
                '자성대부두',
                '신선대부두',
                '감만부두',
                '우암부두',
                '감천한진',
                '신감만부두',
                '일반부두',
                '다목적부두등',
                
            ],
            markers=True
        )
    
        # X축 : 2012 ~ 2024
    fig_port.update_xaxes(
        tickmode='linear',
        dtick=1
    )

    fig_port.update_layout(
        xaxis_title='년도',
        yaxis_title='물동량',
        legend_title='부두'
    )
    
    st.header('전체 부두별 물동량 추이')
    st.subheader('신항 제외')

    st.plotly_chart(
        fig_port,
        use_container_width=True
    )
    st.markdown('13년 기준 전년대비 증가추세를 보이는 부두는 **:blue[자성대]**,**:blue[일반부두]**')
    
    st.write('신선대 : 13년도 하락 후 18년도 까지 우상향/ 22~24 우상향')
    st.write('자성대: 17년도까지 우상향 후 하락세 ')
    st.write('감만 : 12년이후 급속 하락 후 15~21 우상향 ')
    st.write('우암부두 : 현재는 해양산업클러스터 및 북항 재개발 구역으로 개편되어 미래 신해양산업 거점으로 육성')
    st.write('감천부두 : 한진 전용 터미널로 사용하다 현재 한진이 빠짐 / 현재 잡화 및 철강벌크선만 입항')
    st.write('YK 스틸 철강 회사 이전 확정이라 벌크선도 안들어올듯 -> 감천부두 데이터 제외해도 될듯')
    st.write('부산 북항 : 신선대, 자성대, 감만, 우암')
    st.write('---')





    new_port_ratio = new_port.copy()

# 비율을 계산할 부두 목록
    port_columns = [
        '자성대부두',
        '신선대부두',
        '감만부두',
        '우암부두',
        '감천한진',
        '신감만부두',
        '일반부두',
        '다목적부두등',
        '신항부두'
    ]

    # 각 부두 물동량 / 전체 물동량 × 100
    for port in port_columns:
        new_port_ratio[port] = (
            new_port_ratio[port]
            / new_port_ratio['합계']
            * 100
        )

    # 비율 데이터 표시
    st.subheader('부두별 물동량 비율')

    st.dataframe(
    new_port_ratio.style.format({
    '자성대부두': '{:.2f}%',
    '신선대부두': '{:.2f}%',
    '감만부두': '{:.2f}%',
    '우암부두': '{:.2f}%',
    '감천한진': '{:.2f}%',
    '신감만부두': '{:.2f}%',
    '일반부두': '{:.2f}%',
    '다목적부두등': '{:.2f}%',
    '신항부두': '{:.2f}%'
    }),

        hide_index=True,
        use_container_width=True
    )

    fig_ratio = px.line(
    new_port_ratio,
    x='년도',
    y=port_columns,
    markers=True
)

    fig_ratio.update_xaxes(
        tickmode='linear',
        dtick=1
    )

    fig_ratio.update_layout(
        xaxis_title='년도',
        yaxis_title='물동량 점유율 (%)',
        legend_title='부두',
         yaxis=dict(
        ticksuffix='%'
     ))

    st.subheader('부두별 물동량 비율 추이')

    st.plotly_chart(
        fig_ratio,
        use_container_width=True
    )

    st.write('비율을 선형그래프로 표현해서 보기 힘들다. -> 신항 북항으로 나누기')
    st.write('---')

    north_port = new_port.copy()

    north_ports = [
        '자성대부두',
        '신선대부두',
        '감만부두',
        '우암부두',
        '신감만부두'
    ]

    # 북항 = 5개 부두 물동량 합계
    north_port['북항'] = north_port[north_ports].sum(axis=1)

    # 북항이 전체 물동량에서 차지하는 비율
    north_port['북항비율'] = (
        north_port['북항'] / north_port['합계'] * 100
    )
    st.subheader('북항 물동량 비율')

    st.dataframe(
        north_port[['년도', '북항', '북항비율']].style.format({
            '북항비율': '{:.2f}%'
        }),
        hide_index=True,
        use_container_width=True
    )
    fig_north = px.bar(
    north_port,
    x='년도',
    y='북항비율',
    
)

    fig_north.update_xaxes(
        tickmode='linear',
        dtick=1
    )

    fig_north.update_layout(
        xaxis_title='년도',
        yaxis_title='북항 물동량 비율 (%)',
        legend_title='구분',
        yaxis=dict(ticksuffix='%')
    )

    fig_north.update_traces(
        hovertemplate='%{y:.2f}%<extra></extra>'
    )

    st.subheader('북항 물동량 비율 추이')
    st.plotly_chart(fig_north, use_container_width=True)


    st.write('---')


      
    # 북항 · 신항 물동량 비율 분석
    

    
    north_ports = [
        '자성대부두',
        '신선대부두',
        '감만부두',
        '우암부두',
        '신감만부두'
    ]

    
    new_ports = [
        '신항부두'
    ]

   
    port_group = new_port.copy()

    
    # 북항 물동량 계산
  
    port_group['북항'] = port_group[north_ports].sum(axis=1)

    
    # 신항 물동량 계산
  
    # 앞에서 이미 신항1~5부두를 합쳐
    #'신항부두'로 만들었기 때문에 이것을 사용
    port_group['신항'] = port_group['신항부두']

   
    # 북항 · 신항 비율 계산
   
    port_group['북항비율'] = (
        port_group['북항'] / port_group['합계'] * 100
    )

    port_group['신항비율'] = (
        port_group['신항'] / port_group['합계'] * 100
    )


    
    # 북항 · 신항 비율 표
   

    st.subheader('북항 · 신항 물동량 비율')

    group_ratio = port_group[
        ['년도', '북항비율', '신항비율']
    ].copy()

    st.dataframe(
        group_ratio.style.format({
            '북항비율': '{:.2f}%',
            '신항비율': '{:.2f}%'
        }),
        hide_index=True,
        use_container_width=True
    )


    
    # 북항 · 신항 비율 비교
   
  

    fig_group_ratio = px.bar(
        group_ratio,
        x='년도',
        y=['북항비율', '신항비율'],
        barmode='group',
        text_auto='.2f'
    )

    fig_group_ratio.update_xaxes(
        tickmode='linear',
        dtick=1
    )

    fig_group_ratio.update_layout(
        xaxis_title='년도',
        yaxis_title='물동량 비율 (%)',
        legend_title='구분',
        yaxis=dict(
            ticksuffix='%'
        )
    )

    fig_group_ratio.update_traces(
        hovertemplate='%{y:.2f}%<extra></extra>'
    )

    st.subheader('북항 · 신항 물동량 비율 비교')
    st.plotly_chart(
        fig_group_ratio,
        use_container_width=True
    )


    st.write('---')
        
    # KPI 분석
    

    st.write('---')
    st.header('북항 · 신항 KPI 분석')

    # 연도 기준 정렬
    kpi_df = port_group.sort_values('년도').copy()

    # 시작 / 종료 데이터
    start_data = kpi_df[kpi_df['년도'] == 2012].iloc[0]
    end_data = kpi_df[kpi_df['년도'] == 2024].iloc[0]

    # 분석 기간
    years = 2024 - 2012

    # ==========================================
    # 1. CAGR
    # ==========================================

    new_port_cagr = (
        (end_data['신항'] / start_data['신항']) ** (1 / years) - 1
    ) * 100

    north_port_cagr = (
        (end_data['북항'] / start_data['북항']) ** (1 / years) - 1
    ) * 100


    
    #  2024년 신항 점유율
   

    new_port_share_2024 = end_data['신항비율']


    
    #  2012 → 2024 신항 점유율 변화폭
    
    share_change = (
        end_data['신항비율']
        - start_data['신항비율']
    )


  

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label='신항 CAGR',
            value=f'{new_port_cagr:.2f}%'
        )

    with col2:
        st.metric(
            label='북항 CAGR',
            value=f'{north_port_cagr:.2f}%'
        )

    with col3:
        st.metric(
            label='2024 신항 점유율',
            value=f'{new_port_share_2024:.2f}%'
        )

    with col4:
        st.metric(
            label='신항 점유율 변화',
            value=f'{share_change:+.2f}%p',
            delta='2012 → 2024'
        )


   
    # YoY 증감률
   

    kpi_df['신항_YoY'] = (
        kpi_df['신항']
        .pct_change()   #현재 행과 이전 행의 변화율을 계산하는 함수
        * 100
    )

    kpi_df['북항_YoY'] = (
        kpi_df['북항']
        .pct_change()
        * 100
    )

    st.subheader('북항 · 신항 전년 대비 증감률 (YoY)')

    fig_yoy = px.line(
        kpi_df,
        x='년도',
        y=['신항_YoY', '북항_YoY'],
        markers=True
    )

    fig_yoy.update_xaxes(
        tickmode='linear',
        dtick=1
    )

    fig_yoy.update_layout(
        xaxis_title='년도',
        yaxis_title='전년 대비 증감률 (%)',
        legend_title='구분',
        yaxis=dict(
            ticksuffix='%'
        )
    )

    fig_yoy.add_hline(
        y=0,
        line_dash='dash'
    )

    st.plotly_chart(
        fig_yoy,
        use_container_width=True
    )


    # ==========================================
    # 북항 → 신항 물동량 중심 이동
    # ==========================================

    st.subheader('부산항 컨테이너 물동량 중심 이동')

    shift_df = kpi_df[
        ['년도', '북항비율', '신항비율']
    ].copy()

    fig_shift = px.area(
        shift_df,
        x='년도',
        y=['북항비율', '신항비율']
    )

    fig_shift.update_xaxes(
        tickmode='linear',
        dtick=1
    )

    fig_shift.update_layout(
        xaxis_title='년도',
        yaxis_title='전체 물동량 대비 점유율 (%)',
        legend_title='구분',
        yaxis=dict(
            ticksuffix='%'
        )
    )

    st.plotly_chart(
        fig_shift,
        use_container_width=True
    )


   
    # 변동성
    # YoY 증감률의 표준편차
   

    new_port_volatility = (
        kpi_df['신항_YoY'].std()
    )

    north_port_volatility = (
        kpi_df['북항_YoY'].std()
    )


    st.subheader('물동량 증감률 변동성')

    vol_col1, vol_col2 = st.columns(2)

    with vol_col1:
        st.metric(
            label='신항 변동성',
            value=f'{new_port_volatility:.2f}%p'
        )

    with vol_col2:
        st.metric(
            label='북항 변동성',
            value=f'{north_port_volatility:.2f}%p'
        )


    
    # KPI 해석
   

    st.subheader('KPI 분석 결과')

    st.write(
        f'''
        - 신항의 2012~2024년 연평균 성장률(CAGR)은
          :red[{new_port_cagr:.2f}%]로 나타남.

        - 북항의 같은 기간 CAGR은
          :blue[{north_port_cagr:.2f}%]로 나타남.

        - 신항의 부산항 전체 물동량 점유율은
          2012년 :blue[{start_data['신항비율']:.2f}%]에서
          2024년 :red[{end_data['신항비율']:.2f}%]로 변화함.

        - 12년간 신항 점유율은
          :red[{share_change:+.2f}%p] 변화함.

        - 이를 통해 부산항 컨테이너 물동량의 중심이
          장기적으로 북항에서 신항 방향으로 이동한 것을 확인할 수 있음.
        '''
    )

    port_group['북항신항합계'] = (
    port_group['북항'] + port_group['신항']
)

    port_group['북항상대점유율'] = (
        port_group['북항']
        / port_group['북항신항합계']
        * 100
    )

    port_group['신항상대점유율'] = (
        port_group['신항']
        / port_group['북항신항합계']
        * 100
    )

    








    st.write('---')
    st.header('북항 · 신항 물동량 중심 이동 KPI')

    kpi_df = port_group.sort_values('년도').copy()

    start_data = kpi_df[
        kpi_df['년도'] == 2012
    ].iloc[0]

    end_data = kpi_df[
        kpi_df['년도'] == 2024
    ].iloc[0]

    period = 2024 - 2012


    
    # CAGR
   

    new_port_cagr = (
        (end_data['신항'] / start_data['신항'])
        ** (1 / period)
        - 1
    ) * 100


    north_port_cagr = (
        (end_data['북항'] / start_data['북항'])
        ** (1 / period)
        - 1
    ) * 100


    
    # 점유율
    

    new_share_2012 = start_data['신항상대점유율']
    new_share_2024 = end_data['신항상대점유율']

    share_change = (
        new_share_2024 - new_share_2012
    )


   
    # KPI 
   

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            '신항 CAGR',
            f'{new_port_cagr:.2f}%'
        )

    with col2:
        st.metric(
            '북항 CAGR',
            f'{north_port_cagr:.2f}%'
        )

    with col3:
        st.metric(
            '2024 신항 상대 점유율',
            f'{new_share_2024:.2f}%'
        )

    with col4:
        st.metric(
            '신항 점유율 변화',
            f'{share_change:+.2f}%p',
            delta='2012 → 2024'
        )
    

    st.write('---')


    st.subheader('북항·신항 연도별 물동량 추세 분석')

    

        
    # 신항 회귀분석
    
    fig_new_reg = px.scatter(
        kpi_df,
        x='년도',
        y='신항',
        trendline='ols',
        title='신항 물동량 회귀 추세'
    )

    fig_new_reg.update_xaxes(
        tickmode='linear',
        tick0=2012,
        dtick=1
    )

    # 신항 회귀분석 결과
    new_results = px.get_trendline_results(fig_new_reg)
    new_model = new_results.iloc[0]['px_fit_results']

    new_slope = new_model.params[1]
    new_r2 = new_model.rsquared

    st.plotly_chart(fig_new_reg, use_container_width=True)

    
    st.markdown(
    f"""
    

    - 연간 추세 변화량(기울기): **{new_slope:,.0f} TEU/년**
    - 결정계수(R²): **{new_r2:.3f}**
    """
)


   
    # 북항 회귀분석
    
    fig_north_reg = px.scatter(
        kpi_df,
        x='년도',
        y='북항',
        trendline='ols',
        title='북항 물동량 회귀 추세'
    )

    fig_north_reg.update_xaxes(
        tickmode='linear',
        tick0=2012,
        dtick=1
    )

    # 북항 회귀분석 결과
    north_results = px.get_trendline_results(fig_north_reg)
    north_model = north_results.iloc[0]['px_fit_results']

    north_slope = north_model.params[1]
    north_r2 = north_model.rsquared

    st.plotly_chart(fig_north_reg, use_container_width=True)

    
    st.markdown(
        f"""
        

        - 연간 추세 변화량(기울기): **{north_slope:,.0f} TEU/년**
        - 결정계수(R²): **{north_r2:.3f}**

        **북항 연간 물동량은 예측하기 좋은 데이터는 아니다.**
        """
    )

    st.write('신항 = 꾸준하게 커지는 패턴')
    st.write('북항 = 전체적인 방향은 감소 쪽이지만, 오르내림이 있어서 단순한 직선으로 설명하기 어려움')


    st.write('---')
    st.write('ARIMA 분석 통해 다시 해볼 것')
    st.write('---')
    st.write(
            
            'ARIMA 시계열 모델을 이용하여 과거 신항 물동량의 시간적 변화 패턴을 학습  \n '
            '향후 물동량을 예측하는 테스트를 수행  ' 
            '  \n 다만 미래 예측값은 아직 실제값과 비교할 수 없음' 
            '  \n 모델의 예측 성능을 확인하기 위해 백테스트를 추가로 진행 ' 
            '  \n 2012부터 2021년 데이터를 학습 데이터로 사용하고, 모델이 보지 못한 2022~2024년을 예측하도록 한 뒤 실제 물동량과 비교 ' 
            '  \n 이후 MAE, RMSE, MAPE를 이용해 실제값과 예측값의 차이를 평가')
    # ARIMA 테스트
    st.divider()
    st.subheader('ARIMA 연간 물동량 예측 테스트')

    # 신항 데이터
    arima_df = kpi_df[['년도', '신항']].copy()
    arima_df = arima_df.sort_values('년도')

    # ARIMA(1,1,1)
    arima_model = ARIMA(
        arima_df['신항'],
        order=(1, 1, 1)
    )

    arima_fit = arima_model.fit()

    # 향후 3년 예측
    forecast = arima_fit.forecast(steps=3)

    last_year = int(arima_df['년도'].max())

    forecast_df = pd.DataFrame({
        '년도': [
            last_year + 1,
            last_year + 2,
            last_year + 3
        ],
        '예측물동량': forecast.values
    })

    st.dataframe(forecast_df)

    st.write('벡테스트')

    # ==========================================
    # ARIMA 백테스트
    # 2012~2021 학습
    # 2022~2024 예측
    # ==========================================

    st.subheader('신항 ARIMA 백테스트')

    bt_df = kpi_df[
        ['년도', '신항']
    ].copy()

    bt_df = bt_df.sort_values('년도')


    # 학습 데이터
    train = bt_df[
        bt_df['년도'] <= 2021
    ].copy()


    # 테스트 데이터
    test = bt_df[
        bt_df['년도'] >= 2022
    ].copy()


    # ARIMA 모델 학습
    bt_model = ARIMA(
        train['신항'],
        order=(1, 1, 1)
    )

    bt_fit = bt_model.fit()


    # 테스트 기간만큼 예측
    bt_forecast = bt_fit.forecast(
        steps=len(test)
    )


    # 비교 데이터프레임
    backtest_result = pd.DataFrame({
        '년도': test['년도'].values,
        '실제물동량': test['신항'].values,
        '예측물동량': bt_forecast.values
    })


    # 오차
    backtest_result['오차'] = (
        backtest_result['실제물동량']
        - backtest_result['예측물동량']
    )

    backtest_result['절대오차'] = (
        backtest_result['오차'].abs()
    )


    st.dataframe(
        backtest_result.style.format({
            '실제물동량': '{:,.0f}',
            '예측물동량': '{:,.0f}',
            '오차': '{:,.0f}',
            '절대오차': '{:,.0f}'
        }),
        hide_index=True,
        use_container_width=True
    )
        # ==========================================
    # 평가 지표
    # ==========================================

    mae = mean_absolute_error(
        backtest_result['실제물동량'],
        backtest_result['예측물동량']
    )

    rmse = np.sqrt(
        mean_squared_error(
            backtest_result['실제물동량'],
            backtest_result['예측물동량']
        )
    )

    mape = (
        np.abs(
            (
                backtest_result['실제물동량']
                - backtest_result['예측물동량']
            )
            / backtest_result['실제물동량']
        ).mean()
        * 100
    )


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            'MAE',
            f'{mae:,.0f} TEU'
        )

    with col2:
        st.metric(
            'RMSE',
            f'{rmse:,.0f} TEU'
        )

    with col3:
        st.metric(
            'MAPE',
            f'{mape:.2f}%'
        )

    st.write('MAE : 평균적 몇 TEU 정도 틀렸는지')
    st.write('RMSE : 오차에 벌점 지표')
    st.write('MAPE: 평균적실제값 대비 오차 비율 ')

    fig_bt = px.line(
    backtest_result,
    x='년도',
    y=[
        '실제물동량',
        '예측물동량'
    ],
    markers=True,
    title='신항 ARIMA 백테스트: 실제값 vs 예측값'
)

    fig_bt.update_xaxes(
        tickmode='linear',
        dtick=1
    )

    fig_bt.update_layout(
        xaxis_title='년도',
        yaxis_title='물동량 (TEU)',
        legend_title='구분'
    )

    st.plotly_chart(
        fig_bt,
        use_container_width=True
    )
    st.write('예측이랑 실제 물동량이랑 오차율 2.35%')


    st.write('---')
    