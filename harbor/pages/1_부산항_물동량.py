import streamlit as st
import plotly.express as px

from db.database import load_portmis_summary
from api.portmis import update_portmis_summary


st.set_page_config(
    page_title="부산항 물동량",
    page_icon="⚓",
    layout="wide",
)


st.title("⚓ 부산항 물동량 분석")

st.write(
    """
    PORT-MIS 기반 부산항 시설별 실적 데이터를 활용하여
    부산항 전체, 신항, 북항, 감천항의 월별 처리실적과
    접안시간을 분석합니다.
    """
)


# ---------------------------------
# 사이드바
# ---------------------------------

st.sidebar.header("조회 조건")


# ---------------------------------
# 데이터 업데이트
# ---------------------------------

if st.sidebar.button("PORT-MIS 데이터 업데이트"):

    with st.spinner(
        "PORT-MIS 데이터를 불러와 DB에 저장하고 있습니다..."
    ):

        df = update_portmis_summary()

    st.sidebar.success(
        "데이터 업데이트 완료"
    )

else:

    try:
        df = load_portmis_summary()

    except Exception:

        with st.spinner(
            "저장된 데이터가 없어 PORT-MIS 데이터를 불러옵니다..."
        ):

            df = update_portmis_summary()


# ---------------------------------
# 데이터 확인
# ---------------------------------

if df.empty:

    st.warning(
        "조회된 데이터가 없습니다."
    )

    st.stop()


# ---------------------------------
# 항만 구역 선택
# ---------------------------------

area_order = [
    "부산항 전체",
    "신항",
    "북항",
    "감천항",
]


available_areas = [
    area
    for area in area_order
    if area in df["port_area_display"].unique()
]


selected_area = st.sidebar.selectbox(
    "항만 구역",
    available_areas,
)


# ---------------------------------
# 선택 항만 필터링
# ---------------------------------

area_df = df[
    df["port_area_display"] == selected_area
].copy()


# ---------------------------------
# 연월 정렬
# ---------------------------------

area_df = area_df.sort_values(
    "year_month"
)


# ---------------------------------
# KPI
# ---------------------------------

total_throughput = (
    area_df["throughput"].sum()
)

total_berthing_time = (
    area_df["berthing_time"].sum()
)

month_count = (
    area_df["year_month"]
    .nunique()
)

if month_count > 0:
    avg_throughput = (
        total_throughput / month_count
    )
else:
    avg_throughput = 0


col1, col2, col3 = st.columns(3)


col1.metric(
    "총 처리실적",
    f"{total_throughput:,.0f}",
)


col2.metric(
    "총 접안시간",
    f"{total_berthing_time:,.0f} 시간",
)


col3.metric(
    "월평균 처리실적",
    f"{avg_throughput:,.0f}",
)


# ---------------------------------
# 월별 처리실적 차트
# ---------------------------------

st.subheader(
    f"{selected_area} 월별 처리실적"
)


fig_throughput = px.line(
    area_df,
    x="year_month",
    y="throughput",
    markers=True,
    labels={
        "year_month": "연월",
        "throughput": "처리실적",
    },
)


st.plotly_chart(
    fig_throughput,
    use_container_width=True,
)


# ---------------------------------
# 월별 접안시간 차트
# ---------------------------------

st.subheader(
    f"{selected_area} 월별 접안시간"
)


fig_berthing = px.line(
    area_df,
    x="year_month",
    y="berthing_time",
    markers=True,
    labels={
        "year_month": "연월",
        "berthing_time": "접안시간",
    },
)


st.plotly_chart(
    fig_berthing,
    use_container_width=True,
)


# ---------------------------------
# 데이터 표
# ---------------------------------

st.subheader(
    "월별 데이터"
)


display_df = area_df[
    [
        "year_month",
        "port_area_display",
        "throughput",
        "berthing_time",
    ]
].copy()


display_df = display_df.rename(
    columns={
        "year_month": "연월",
        "port_area_display": "항만구역",
        "throughput": "처리실적",
        "berthing_time": "접안시간",
    }
)


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
)