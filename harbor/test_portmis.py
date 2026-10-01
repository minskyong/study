from api.portmis import (
    get_portmis_data,
    make_monthly_summary,
    add_total_busan_port,
    update_portmis_summary,
)


# 1. PORT-MIS 원본 데이터 가져오기
df = get_portmis_data()


# 2. 기본 확인
print("처음 5행")
print(df.head())

print()

print("컬럼 목록")
print(df.columns.tolist())

print()

print("데이터 개수")
print(len(df))

print()

print("항구 구분")
print(df["port_area"].unique())

print()

print("화면 표시용 항구 구분")
print(df["port_area_display"].unique())


# 3. 부산 구분 시설명 확인
print()
print("========== 부산 시설명 ==========")

busan_facilities = (
    df[df["port_area"] == "부산"]["facility_name"]
    .dropna()
    .drop_duplicates()
    .sort_values()
)

for name in busan_facilities:
    print(name)


# 4. 부산신항 시설명 확인
print()
print("========== 부산신항 시설명 ==========")

new_port_facilities = (
    df[df["port_area"] == "부산신항"]["facility_name"]
    .dropna()
    .drop_duplicates()
    .sort_values()
)

for name in new_port_facilities:
    print(name)


# 5. 감천 시설명 확인
print()
print("========== 감천 시설명 ==========")

gamcheon_facilities = (
    df[df["port_area"] == "감천"]["facility_name"]
    .dropna()
    .drop_duplicates()
    .sort_values()
)

for name in gamcheon_facilities:
    print(name)


# 6. 월별 집계
summary = make_monthly_summary(df)

print()
print("========== 월별 집계 ==========")
print(summary.head(30))


# 7. 부산항 전체 데이터 추가
summary_with_total = add_total_busan_port(summary)

print()
print("========== 부산항 전체 포함 ==========")
print(summary_with_total.head(40))

print()
print("========== DB 저장 테스트 ==========")

saved_df = update_portmis_summary()

print("DB 저장 완료")
print(saved_df.head())