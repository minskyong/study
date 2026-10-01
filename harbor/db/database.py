from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "port.db"

engine = create_engine(
    f"sqlite:///{DB_PATH}"
)


def save_dataframe(df, table_name):
    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
    )


def load_dataframe(table_name):
    return pd.read_sql(
        f"SELECT * FROM {table_name}",
        engine
    )


def load_cargo_by_period(start_ym, end_ym):
    query = text(
        """
        SELECT *
        FROM cargo_statistics
        WHERE year_month BETWEEN :start_ym AND :end_ym
        ORDER BY year_month, cargo_code
        """
    )

    return pd.read_sql(
        query,
        engine,
        params={
            "start_ym": start_ym,
            "end_ym": end_ym,
        }
    )


def cargo_period_exists(start_ym, end_ym):
    query = text(
        """
        SELECT COUNT(DISTINCT year_month) AS month_count
        FROM cargo_statistics
        WHERE year_month BETWEEN :start_ym AND :end_ym
        """
    )

    try:
        result = pd.read_sql(
            query,
            engine,
            params={
                "start_ym": start_ym,
                "end_ym": end_ym,
            }
        )

        return result.iloc[0]["month_count"] > 0

    except Exception:
        return False


def delete_cargo_period(start_ym, end_ym):
    query = text(
        """
        DELETE FROM cargo_statistics
        WHERE year_month BETWEEN :start_ym AND :end_ym
        """
    )

    with engine.begin() as conn:
        conn.execute(
            query,
            {
                "start_ym": start_ym,
                "end_ym": end_ym,
            }
        )

def save_portmis_summary(df):

    df.to_sql(
        "portmis_monthly_summary",
        engine,
        if_exists="replace",
        index=False,
    )


def load_portmis_summary():

    return pd.read_sql(
        """
        SELECT *
        FROM portmis_monthly_summary
        ORDER BY year_month, port_area_display
        """,
        engine
    )