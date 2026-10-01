import streamlit as st
import plotly.express as px

from api.cargo import (
    get_cargo_statistics,
    get_cargo_from_db,
)


st.set_page_config(
    page_title="Harbor",
    page_icon="⚓",
    layout="wide"
)

st.title("⚓ Harbor")
st.subheader("항만물류 데이터 분석 플랫폼")


# # -------------------------
# # 조회 조건
# # -------------------------

# st.sidebar.header("조회 조건")

# start_year = st.sidebar.selectbox(
#     "시작 연도",
#     range(2020, 2027),
#     index=5
# )

# end_year = st.sidebar.selectbox(
#     "종료 연도",
#     range(2020, 2027),
#     index=5
# )

# start_month = st.sidebar.selectbox(
#     "시작 월",
#     range(1, 13),
#     index=0
# )

# end_month = st.sidebar.selectbox(
#     "종료 월",
#     range(1, 13),
#     index=11
# )

# start_ym = f"{start_year}{start_month:02d}"
# end_ym = f"{end_year}{end_month:02d}"


# # -------------------------
# # 데이터 업데이트
# # -------------------------

# update_button = st.sidebar.button(
#     "최신 데이터 업데이트"
# )

# if update_button:

#     with st.spinner(
#         "해양수산부 API에서 데이터를 가져오는 중..."
#     ):
#         df = get_cargo_statistics(
#             start_ym,
#             end_ym
#         )

#     st.sidebar.success(
#         "데이터 업데이트 완료"
#     )

# else:

#     try:
#         df = get_cargo_from_db(
#             start_ym,
#             end_ym
#         )

#     except Exception:
#         df = get_cargo_statistics(
#             start_ym,
#             end_ym
#         )


# # -------------------------
# # 데이터 확인
# # -------------------------

# if df.empty:

#     st.warning(
#         "조회된 데이터가 없습니다."
#     )

#     st.stop()


# # -------------------------
# # KPI
# # -------------------------

# total = df["total"].sum()
# arrival = df["arrival"].sum()
# departure = df["departure"].sum()


# col1, col2, col3 = st.columns(3)

# col1.metric(
#     "총 처리량",
#     f"{total:,.0f}"
# )

# col2.metric(
#     "입항",
#     f"{arrival:,.0f}"
# )

# col3.metric(
#     "출항",
#     f"{departure:,.0f}"
# )


# # -------------------------
# # 품목별 집계
# # -------------------------

# cargo_summary = (
#     df.groupby(
#         "cargo_name",
#         as_index=False
#     )
#     [
#         [
#             "total",
#             "arrival",
#             "departure"
#         ]
#     ]
#     .sum()
# )


# cargo_top10 = (
#     cargo_summary
#     .sort_values(
#         "total",
#         ascending=False
#     )
#     .head(10)
# )


# # -------------------------
# # 차트
# # -------------------------

# st.subheader(
#     "품목별 화물 처리량 TOP 10"
# )

# fig = px.bar(
#     cargo_top10,
#     x="cargo_name",
#     y="total",
#     title="품목별 총 처리량 TOP 10"
# )

# st.plotly_chart(
#     fig,
#     use_container_width=True
# )


# # -------------------------
# # 원본 데이터
# # -------------------------

# st.subheader(
#     "조회 데이터"
# )

# st.dataframe(
#     df,
#     use_container_width=True
# )



selected_area = st.sidebar.selectbox(
    "항만 구분",
    [
        "부산항 전체",
        "신항",
        "북항",
        "감천"
    ]
)