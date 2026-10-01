from api.client import PortAPIClient
from db.database import save_dataframe

client = PortAPIClient()

xml_data = client.get_xml(
    endpoint="SsopCargFrghtPrdlst2/YM",
    params={
        "pageNo": 1,
        "numOfRows": 100,
        "sym": "202501",
        "eym": "202501",
    }
)

df = client.xml_to_dataframe(xml_data)

# 컬럼명 변경
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

# 숫자형 변환
numeric_columns = [
    "total",
    "arrival",
    "departure",
]

for col in numeric_columns:
    df[col] = df[col].astype(int)

print(df)
print()
print(df.dtypes)

save_dataframe(
    df,
    "cargo_statistics"
)

print("\nDB 저장 완료")