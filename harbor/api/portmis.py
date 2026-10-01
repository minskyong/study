import os

import pandas as pd
import requests

from dotenv import load_dotenv
from db.database import save_portmis_summary

load_dotenv()


BASE_URL = (
    "https://api.odcloud.kr/api/"
    "15133155/v1/"
    "uddi:84ee5009-d0dc-4ddf-94d6-fdbac8b683f1"
)


def clean_portmis_data(df):

    df = df.copy()

    # 한글 컬럼명을 영어 컬럼명으로 변경
    df = df.rename(
        columns={
            "사용년월": "year",
            "사용월": "month",
            "시설명": "facility_name",
            "시설서브코드": "facility_sub_code",
            "시설코드": "facility_code",
            "접안시간": "berthing_time",
            "처리실적": "throughput",
            "항구청명": "port_area",
        }
    )

    # 숫자형으로 변환
    numeric_columns = [
        "year",
        "month",
        "berthing_time",
        "throughput",
    ]

    for col in numeric_columns:
        df[col] = (
            pd.to_numeric(
                df[col],
                errors="coerce"
            )
            .fillna(0)
            .astype(int)
        )

    # YYYYMM 형태의 연월 컬럼 생성
    # 예: 2025년 8월 -> 202508
    df["year_month"] = (
        df["year"].astype(str)
        + df["month"].astype(str).str.zfill(2)
    )

    # PORT-MIS 원본 구역명을
    # 화면에서 보기 쉬운 분석용 구역명으로 변환
    area_map = {
        "부산": "북항",
        "부산신항": "신항",
        "감천": "감천항",
    }

    df["port_area_display"] = (
        df["port_area"]
        .map(area_map)
        .fillna(df["port_area"])
    )

    return df


def get_portmis_data(page=1, per_page=1000):

    service_key = os.getenv("PORTMIS_API_KEY")

    if not service_key:
        raise ValueError(
            "PORTMIS_API_KEY가 없습니다. .env 파일을 확인해주세요."
        )

    params = {
        "page": page,
        "perPage": per_page,
        "returnType": "JSON",
        "serviceKey": service_key,
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()

    df = pd.DataFrame(
        result["data"]
    )

    # API 원본 데이터를 분석하기 좋은 형태로 정리
    df = clean_portmis_data(df)

    return df


def make_monthly_summary(df):

    summary = (
        df.groupby(
            [
                "year_month",
                "port_area_display",
            ],
            as_index=False
        )
        .agg(
            throughput=("throughput", "sum"),
            berthing_time=("berthing_time", "sum"),
        )
        .sort_values(
            [
                "year_month",
                "port_area_display",
            ]
        )
        .reset_index(drop=True)
    )

    return summary


def add_total_busan_port(summary_df):

    # 신항 + 북항 + 감천항을 합해서
    # 부산항 전체 데이터 생성
    total_df = (
        summary_df.groupby(
            "year_month",
            as_index=False
        )
        .agg(
            throughput=("throughput", "sum"),
            berthing_time=("berthing_time", "sum"),
        )
    )

    total_df["port_area_display"] = "부산항 전체"

    result = pd.concat(
        [
            summary_df,
            total_df,
        ],
        ignore_index=True
    )

    result = (
        result.sort_values(
            [
                "year_month",
                "port_area_display",
            ]
        )
        .reset_index(drop=True)
    )

    return result


def update_portmis_summary():

    # PORT-MIS 데이터 가져오기
    df = get_portmis_data()

    # 신항 / 북항 / 감천항 월별 집계
    summary = make_monthly_summary(df)

    # 부산항 전체 합계 추가
    summary = add_total_busan_port(summary)

    # SQLite 저장
    save_portmis_summary(summary)

    return summary