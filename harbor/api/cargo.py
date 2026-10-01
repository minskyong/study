from api.client import PortAPIClient
from db.database import (
    save_dataframe,
    load_cargo_by_period,
    delete_cargo_period,
)


def get_cargo_statistics(start_ym, end_ym):
    client = PortAPIClient()

    xml_data = client.get_xml(
        endpoint="SsopCargFrghtPrdlst2/YM",
        params={
            "pageNo": 1,
            "numOfRows": 1000,
            "sym": start_ym,
            "eym": end_ym,
        }
    )

    df = client.xml_to_dataframe(xml_data)

    df = df.rename(
        columns={
            "useYm": "year_month",
            "frghtPrdlstNm": "cargo_name",
            "frghtPrdlstCd": "cargo_code",
            "total": "total",
            "etrypt": "arrival",
            "tkoff": "departure",
        }
    )

    numeric_columns = [
        "total",
        "arrival",
        "departure",
    ]

    for col in numeric_columns:
        df[col] = (
            df[col]
            .fillna(0)
            .astype(int)
        )

    delete_cargo_period(
        start_ym,
        end_ym
    )

    save_dataframe(
        df,
        "cargo_statistics"
    )

    return df


def get_cargo_from_db(start_ym, end_ym):
    return load_cargo_by_period(
        start_ym,
        end_ym
    )