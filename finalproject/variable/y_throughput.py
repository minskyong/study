import pandas as pd
import streamlit as st
import plotly.express as px


csv_PATH = r'C:\work\finalproject\data\container.csv'

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


    # --------------------------------
    # 부두별 필요한 컬럼만 선택
    # --------------------------------

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


    # --------------------------------
    # 부두별 데이터 확인
    # --------------------------------

   

   


    # ========================================
    # 부두별 물동량 선그래프
    # ========================================

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


        # ==========================================
    # 북항 · 신항 물동량 비율 분석
    # ==========================================

    # 북항에 포함되는 부두
    north_ports = [
        '자성대부두',
        '신선대부두',
        '감만부두',
        '우암부두',
        '신감만부두'
    ]

    # 신항에 포함되는 부두
    new_ports = [
        '신항부두'
    ]

    # 복사
    port_group = new_port.copy()

    # -----------------------------
    # 북항 물동량 계산
    # -----------------------------
    port_group['북항'] = port_group[north_ports].sum(axis=1)

    # -----------------------------
    # 신항 물동량 계산
    # -----------------------------
    # 앞에서 이미 신항1~5부두를 합쳐
    # '신항부두'로 만들었기 때문에 이것을 사용
    port_group['신항'] = port_group['신항부두']

    # -----------------------------
    # 북항 · 신항 비율 계산
    # -----------------------------
    port_group['북항비율'] = (
        port_group['북항'] / port_group['합계'] * 100
    )

    port_group['신항비율'] = (
        port_group['신항'] / port_group['합계'] * 100
    )


    # ==========================================
    # 북항 · 신항 비율 표
    # ==========================================

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


    # ==========================================
    # 북항 · 신항 비율 비교
    # ==========================================

  

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