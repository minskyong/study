import pandas as pd
import streamlit as st
import plotly.express as px

csv_PATH = r'C:\work\finalproject\data\container.csv'

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