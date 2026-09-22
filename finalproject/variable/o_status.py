import pandas as pd
import streamlit as st
import plotly.express as px

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
csv_PATH = BASE_DIR / 'data' / 'container.csv'

df = pd.read_csv(csv_PATH, encoding='utf-8')

def port_ratio():

    port_data = df.copy()
    port_data = port_data[port_data['년도'] >= 2012]

    port_data['신항부두'] = port_data[
        ['신항1부두', '신항2부두', '신항3부두', '신항4부두', '신항5부두']
    ].sum(axis=1)

    north_ports = [
        '자성대부두',
        '신선대부두',
        '감만부두',
        '우암부두',
        '신감만부두'
    ]

    port_data['북항'] = port_data[north_ports].sum(axis=1)

    port_data['북항비율'] = (
        port_data['북항'] / port_data['합계'] * 100
    )

    port_data['신항비율'] = (
        port_data['신항부두'] / port_data['합계'] * 100
    )

    ratio_data = port_data[
        ['년도', '북항', '신항부두', '북항비율', '신항비율']
    ]

    st.subheader('북항 · 신항 물동량 비율')

    st.dataframe(
        ratio_data.style.format({
            '북항': '{:,.0f}',
            '신항부두': '{:,.0f}',
            '북항비율': '{:.2f}%',
            '신항비율': '{:.2f}%'
        }),
        hide_index=True,
        use_container_width=True
    )

    fig = px.bar(
        ratio_data,
        x='년도',
        y=['북항비율', '신항비율'],
        barmode='group'
    )

    fig.update_xaxes(
        tickmode='linear',
        dtick=1
    )

    fig.update_layout(
        xaxis_title='년도',
        yaxis_title='물동량 비율 (%)',
        legend_title='구분',
        yaxis=dict(ticksuffix='%')
    )

    fig.update_traces(
        texttemplate='%{y:.2f}%',
        textposition='outside',
        hovertemplate='%{y:.2f}%<extra></extra>'
    )

    st.subheader('북항 · 신항 물동량 비율 비교')

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ==========================================
    # 부산항 전체 대비 비율
    # 기존 분석용
    # ==========================================

    port_data['북항비율'] = (
        port_data['북항']
        / port_data['합계']
        * 100
    )

    port_data['신항비율'] = (
        port_data['신항부두']
        / port_data['합계']
        * 100
    )


    # ==========================================
    # 북항 + 신항 기준 상대점유율
    # KPI용
    # ==========================================

    port_data['북항신항합계'] = (
        port_data['북항']
        + port_data['신항부두']
    )

    port_data['북항상대점유율'] = (
        port_data['북항']
        / port_data['북항신항합계']
        * 100
    )

    port_data['신항상대점유율'] = (
        port_data['신항부두']
        / port_data['북항신항합계']
        * 100
    )


    # ==========================================
    # KPI 계산
    # ==========================================

    start_data = (
        port_data[
            port_data['년도'] == 2012
        ]
        .iloc[0]
    )

    end_data = (
        port_data[
            port_data['년도'] == 2024
        ]
        .iloc[0]
    )


    # CAGR 기간
    period = 2024 - 2012


    # 신항 CAGR
    new_port_cagr = (
        (
            end_data['신항부두']
            / start_data['신항부두']
        ) ** (1 / period)
        - 1
    ) * 100


    # 북항 CAGR
    north_port_cagr = (
        (
            end_data['북항']
            / start_data['북항']
        ) ** (1 / period)
        - 1
    ) * 100


    # 2024년 신항 상대점유율
    new_share_2024 = (
        end_data['신항상대점유율']
    )


    # 2012년 신항 상대점유율
    new_share_2012 = (
        start_data['신항상대점유율']
    )


    # 신항 점유율 변화폭
    share_change = (
        new_share_2024
        - new_share_2012
    )


    # ==========================================
    # 화면 제목
    # ==========================================

    st.title(
        '부산항 컨테이너 물동량 전체 현황'
    )

    st.caption(
        '2012 ~ 2024년 북항 · 신항 컨테이너 물동량 비교'
    )


    # ==========================================
    # 핵심 KPI
    # ==========================================

    st.subheader(
        '부산항 컨테이너 물동량 핵심 KPI'
    )

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            label='신항 CAGR',
            value=f'{new_port_cagr:.2f}%'
        )

        st.caption(
            '2012~2024 연평균 성장률'
        )


    with col2:

        st.metric(
            label='북항 CAGR',
            value=f'{north_port_cagr:.2f}%'
        )

        st.caption(
            '2012~2024 연평균 성장률'
        )


    with col3:

        st.metric(
            label='2024 신항 상대점유율',
            value=f'{new_share_2024:.2f}%', 
        )

        st.caption(
            '북항 + 신항 기준'
        )


    with col4:

        st.metric(
            label='신항 점유율 변화',
            value=f'{share_change:+.2f}%p'
        )

        st.caption(
            '2012 → 2024'
        )


    # ==========================================
    # KPI 간단 설명
    # ==========================================

    st.markdown(
    f'''
    ### KPI 해석

    2012년 북항·신항 물동량 중 신항의 비중은
    :yellow[{new_share_2012:.2f}%] \n
    2024년에는 :red[{new_share_2024:.2f}%]로 증가

    따라서 신항의 상대점유율은
    2012년 대비 :red[{share_change:+.2f}%p] 확대됨을 보임

    같은 기간 신항 물동량은 연평균
    :red[{new_port_cagr:.2f}%] 성장률을 보이는 반면 \n
    북항은 연평균 :blue[{north_port_cagr:.2f}%] 감소율을 보임
    '''
)
   