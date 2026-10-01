# 월간 물동량으로 계절성 확인하기 

import pandas as pd
import streamlit as st
from pathlib import Path
import plotly.express as px
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
BASE_DIR = Path(__file__).resolve().parent.parent
csv_PATH = BASE_DIR / 'data' / '월별물동량.csv'


def season_analysis():
    
    
    df = pd.read_csv(
        csv_PATH,
        encoding='utf-8',
        header=[0, 1]
    )

    
    st.header('분석 과정')
    st.markdown(""" 
        ### 1.월별 평균

        - 월별 차이가 있는지 탐색
    
        ### 2.성수기/비수기
            
        - 전체 평균 대비 높은/낮은 월 파악
    
        ### 3. 12개월 이동평균
            
        - 장기 추세 확인
    
        ### 4. 월별 편차
            
        - 월별 차이를 수치화
    
        ### 5. 시계열 분해
            
         - Trend와 Seasonal을 실제로 분리
        ---
        """)

   
    season_df = df[
    [
        ('Unnamed: 0_level_0', '조회년도'),
        ('Unnamed: 1_level_0', '조회월'),
        ('Unnamed: 2_level_0', '국적선구분'),
        ('TEU', '적'),
        ('Unnamed: 16_level_0', '공'),
        ('Unnamed: 17_level_0', '계')
    ]
        ].copy()
    
    season_df.columns = [
    '년도',
    '월',
    '국적선구분',
    '적컨테이너',
    '공컨테이너',
    '총합'
]
    season_df['년도'] = season_df['년도'].ffill()

    season_df['년도'] = pd.to_numeric(
    season_df['년도'],
    errors='coerce'
)

    season_df['월'] = pd.to_numeric(
        season_df['월'],
        errors='coerce'
    )
    season_df = season_df[
    season_df['국적선구분'] == '계'
    ].copy()
    season_df = season_df.dropna(
    subset=['년도', '월']
)
    season_df['년도'] = season_df['년도'].astype(int)
    season_df['월'] = season_df['월'].astype(int)

    for col in ['적컨테이너', '공컨테이너', '총합']:
        season_df[col] = (
            season_df[col]
            .astype(str)
            .str.replace(',', '', regex=False)
            .str.strip()
        )

        season_df[col] = pd.to_numeric(
            season_df[col],
            errors='coerce'
        )

    season_df['date'] = pd.to_datetime(
    dict(
        year=season_df['년도'],
        month=season_df['월'],
        day=1
    )
)

    season_df = season_df.sort_values('date')    

    st.subheader('계절성 분석용 데이터 가공 확인')

    st.write('전체 행 개수:', len(season_df))

  

    st.dataframe(
        season_df[
            [
                '년도',
                '월',
                '적컨테이너',
                '공컨테이너',
                '총합',
                'date'
            ]
        ]
    )


  
    st.write('---')
    
    st.header("월별 평균 물동량 확인")
    st.write('---')
    st.markdown(
                
        """
          ### 월들을 비교해서 계절성 확인
           
        """
    )

    # 월별 평균 계산
    monthly_avg = (
        season_df
        .groupby('월')['총합']
        .mean()
        .reset_index()
    )

    monthly_avg.columns = ['월', '평균물동량']

    st.subheader('1. 월별 평균 물동량')

    st.dataframe(monthly_avg)

    fig_monthly_avg = px.bar(
        monthly_avg,
        x='월',
        y='평균물동량',
        title='2012~2024 월별 평균 컨테이너 물동량',
        labels={
            '월': '월',
            '평균물동량': '평균 물동량(TEU)'
        }
    )

    fig_monthly_avg.update_xaxes(
        tickmode='linear',
        dtick=1
    )

    st.plotly_chart(
        fig_monthly_avg,
        use_container_width=True
    )

    st.write("각 월마다 왜 차이가 나는지 알아볼것")
    st.write('---')

    st.header('성수기 / 비수기 분석')
    st.markdown(
        """
        단순히 이름 붙이기 x 
        
        :red[무엇을 기준]으로 **성수기/비수기 정했는지 설명가능하게 만드는것 중요**
        
        성수기 / 비수기가 년도별로 일정하다면 이걸 계절성으로 봐도 되는지? 
        """
)   


    st.subheader('2. 성수기 / 비수기 분석')

    overall_avg = monthly_avg['평균물동량'].mean()

    st.metric(
        '전체 월 평균 물동량',
        f'{overall_avg:,.0f} TEU'
    )

    st.markdown(
        """
        ### '쉬운 성수기/비수기 기준'

        '월 평균 > 전체 평균 → 성수기' 

        '월 평균 < 전체 평균 → 비수기'

        '평균을 잡은 것과 같은 수치인 월이 나올 수 있음'
        '보통이라는 기준을 하나 잡아놓기'
        """
)

    monthly_avg['구분'] = monthly_avg['평균물동량'].apply(
    lambda x:
        '성수기' if x > overall_avg
        else '비수기' if x < overall_avg
        else '보통'
)


    monthly_avg['평균대비차이'] = (
    monthly_avg['평균물동량'] - overall_avg
)

    st.dataframe(
        monthly_avg[
            [
                '월',
                '평균물동량',
                '평균대비차이',
                '구분'
            ]
        ],
        use_container_width=True
    )
    st.write('기준점')
    st.write(overall_avg)

    fig_peak = px.line(
    monthly_avg,
    x='월',
    y='평균물동량',
    title='월별 평균 물동량과 전체 평균 비교',
    labels={
        '월': '월',
        '평균물동량': '평균 물동량(TEU)'
    },
    markers=True)

    


    # 전체 평균 기준선
    fig_peak.add_hline(
        y=overall_avg,
        line_dash='dash',
        annotation_text=f'전체 평균 {overall_avg:,.0f} TEU',
        annotation_position='top left'
    )

    # X축 1월 ~ 12월 고정
    fig_peak.update_xaxes(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=[f'{i}월' for i in range(1, 13)]
    )

    # Y축 숫자 표시
    fig_peak.update_yaxes(
        tickformat=','
    )

    st.plotly_chart(
        fig_peak,
        use_container_width=True
    )
    
    st.markdown(
        """
        그래프로 보면 :blue[2월, 9월]이 다른 월들에 비해 감소폭이 큼
        
        중국 춘절,중추절이 우리나라 설날,추석과 겹침 
        
        연휴의 연파가 큰것을 추론 가능
    
        why? : 부산항이 환적 비중이 점점 늘어났음을 환적 분석에서 파악

        환적 비중이 제일 높은 나라가 중국

        그래서 연휴의 영향을 보인다 생각
    
    
        """)

    
    st.write('---')
    st.subheader('전월대비/전년동월대비 증감률')
    

    total = season_df.set_index('date')['총합']

    growth = pd.DataFrame({
        '물동량': total,
        '전월대비':total.pct_change() * 100,
        '전년동월대비': total.pct_change(12) * 100
    })

    growth = growth.round(2)
    st.write(growth.loc['2013-01':].round(2))
    # 2012년은 비교할 전년도 데이터가 없으므로 제외
    recent = growth.dropna(subset=['전년동월대비'])

    
    # ==========================================
    # 그래프
    # ==========================================

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = [
        'green' if v >= 0 else 'red'
        for v in recent['전년동월대비']
    ]

    ax.bar(
        recent.index,
        recent['전년동월대비'],
        color=colors,
        width=20
    )

    # 0% 기준선
    ax.axhline(
        0,
        color='black',
        linewidth=0.8
    )

    ax.set_ylabel('전년 동월 대비 (%)')

    ax.set_title(
        '부산항 전체 물동량 전년 동월 대비 증감률 (2013~2024)'
    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)
    st.markdown(
        """
        전년 동월대비 증감률(Year over Year, YoY)
        월별 물동량을 바로 앞달과 비교하면 계절의 영향이 포함될 수 있다. 연별로 같은 달끼리 비교하는 방법을 사용할 수도 있다. 올해 2월이랑 작년 2월을 비교하면 날짜 수랑 계절도 같기 때문에 계절 효과같은 내용들이 상당히 소거될 수 있다.

        이렇게 전년도의 같은달처럼 같은 달끼리 비교하는 방식을 전년 동월대비 증감률이라고 일컫는다. pct_change(12), shift(12)로 확인 가능하다.

        전년 동월대비비교도 문제가 있을 수 있는데, 음력에따라 양력의 쉬는날(명절)이 변경될 수 있다. 작년에 설 2월이었는데 올해는 설이 1월이면, 같은 1월끼리 비교해도 연휴가 있어서 불리하고 유리하고가 바뀌게 된다. 1~2월값 합쳐서보면 어느정도는 해소 가능합니다. 처음 12개월은 비교할 작년이 없음.

        전년동월대비증감률 = (올해 이번달 값 - 작년 같은달 값) / 작년 같은 달 값 * 100


        """



    )

    st.write('---')
    st.header('12개월 이동평균')

    # ==========================================
   # 12개월 이동평균
    # ==========================================

    

    season_df['12개월이동평균'] = (
        season_df['총합']
        .rolling(window=12)
        .mean()
    )

    fig_ma = px.line(
        season_df,
        x='date',
        y=['총합', '12개월이동평균'],
        title='월별 물동량과 12개월 이동평균',
        labels={
            'date': '날짜',
            'value': '물동량(TEU)',
            'variable': '구분'
        }
    )
    fig_ma.update_xaxes(
    tickmode='array',
    tickvals=pd.date_range(
        start='2012-01-01',
        end='2024-01-01',
        freq='YS'
    ),
    ticktext=[str(year) for year in range(2012, 2025)],
    title='연도'
)

    fig_ma.update_yaxes(
        tickformat=','
    )

   
    
    st.plotly_chart(
        fig_ma,
        use_container_width=True
    )
    st.write('---')

    # 12개월 이동평균
    season_df['12개월이동평균'] = (
        season_df['총합']
        .rolling(12)
        .mean()
    )

    # 그래프
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        season_df['date'],
        season_df['총합'],
        label='월별 물동량',
        linewidth=1
    )

    ax.plot(
        season_df['date'],
        season_df['12개월이동평균'],
        label='12개월 이동평균',
        linewidth=2.5
    )

    ax.set_title('부산항 전체 월별 물동량 및 12개월 이동평균')
    ax.set_ylabel('물동량 (TEU)')
    ax.set_xlabel('연도')
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)
    

    st.write('---')
    st.subheader('시계열 분석')

   
    # ==========================================
    # 5. 시계열 분해
    # ==========================================

    

    # 날짜를 인덱스로 설정
    ts = (
        season_df
        .set_index('date')['총합']
        .sort_index()
    )

    # 시계열 분해
    decomposition = seasonal_decompose(
        ts,
        model='additive',
        period=12
    )
   
    # 결과를 DataFrame으로 변환
    decomp_df = pd.DataFrame({
        'date': ts.index,
        '실제 물동량': ts.values,
        '장기추세': decomposition.trend.values,
        '계절성': decomposition.seasonal.values,
        '잔차': decomposition.resid.values
    })
    st.dataframe(decomp_df[['date','계절성']].head(36))
    #장기 추세 
    fig_trend = px.line(
        decomp_df,
        x='date',
        y='장기추세',
        title='2012~2024 컨테이너 물동량 장기 추세',
        labels={
            'date': '연도',
            '장기추세': '물동량 (TEU)'
        }
    )

    fig_trend.update_xaxes(
        tickmode='array',
        tickvals=pd.date_range(
            start='2012-01-01',
            end='2024-01-01',
            freq='YS'
        ),
        ticktext=[str(year) for year in range(2012, 2025)]
    )

    fig_trend.update_yaxes(
        tickformat=','
    )

    fig_trend.update_layout(
        hovermode='x unified'
    )

    st.plotly_chart(
        fig_trend,
        use_container_width=True,
        key='trend_chart'
    )
     #계절성 Seasonal
    fig_seasonal = px.line(
    decomp_df,
    x='date',
    y='계절성',
    title='2012~2024 월별 계절성 패턴',
    labels={
        'date': '연도',
        '계절성': '계절 효과 (TEU)'
    }
)

    fig_seasonal.update_xaxes(
        tickmode='array',
        tickvals=pd.date_range(
            start='2012-01-01',
            end='2024-01-01',
            freq='YS'
        ),
        ticktext=[str(year) for year in range(2012, 2025)]
    )

    fig_seasonal.add_hline(
        y=0,
        line_dash='dash'
    )

    fig_seasonal.update_yaxes(
        tickformat=','
    )

    st.plotly_chart(
        fig_seasonal,
        use_container_width=True,
        key='seasonal_chart'
    )
    st.markdown("""        
        
            seasonal_decompose()는 13년 전체에
    
            대표적인 12개월 계절 패턴 하나를 추출해서 반복해서 보여줌
            
            그래서 12~24년도 13년의 평균만 보여주는 거라 연도별 차이를 보여주지 않음
            """)
    
    
    # 잔차 Residual
    fig_residual = px.line(
    decomp_df,
    x='date',
    y='잔차',
    title='추세와 계절성으로 설명되지 않는 변동',
    labels={
        'date': '연도',
        '잔차': '잔차 (TEU)'
    }
)

    fig_residual.add_hline(
        y=0,
        line_dash='dash'
    )

    fig_residual.update_xaxes(
        tickmode='array',
        tickvals=pd.date_range(
            start='2012-01-01',
            end='2024-01-01',
            freq='YS'
        ),
        ticktext=[str(year) for year in range(2012, 2025)]
    )

    fig_residual.update_yaxes(
        tickformat=','
    )

    st.plotly_chart(
        fig_residual,
        use_container_width=True,
        key='residual_chart'
    )
    

    fig_year_pattern = px.line(
    season_df,
    x='월',
    y='총합',
    color='년도',
    markers=True,
    title='2012~2024 연도별 월별 물동량 패턴 비교',
    labels={
        '월': '월',
        '총합': '물동량(TEU)',
        '년도': '연도'
    }
)

    fig_year_pattern.update_xaxes(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=[f'{i}월' for i in range(1, 13)]
    )

    fig_year_pattern.update_yaxes(
        tickformat=','
    )

    st.plotly_chart(
        fig_year_pattern,
        use_container_width=True,
        key='year_pattern_chart'
    )

    st.markdown("""
            1월 -> 2월 전체 감소

            2월 -> 3월 전체 증가


                """)

    st.write('---')

    
    
    st.markdown(


        """
        # 분석 결과 
        계절성 및 장기 추세 분석 결과
    2012~2024년 부산항 월별 컨테이너 물동량을 대상으로 월별 특성, 장기 추세 및 계절성을 분석하였다.
    1. 월별 평균 물동량
    13년간 동일 월의 평균 물동량을 비교하여 월별 물동량 수준의 차이를 확인하였다. 이를 통해 특정 월에 물동량이 상대적으로 높거나 낮아지는 경향을 파악하였다.
   
     2. 성수기·비수기 분석
    월별 평균을 전체 월 평균과 비교하여 평균 이상인 월과 평균 이하인 월을 구분하였다. 이는 공식적인 성수기·비수기 분류가 아닌, 분석 기간의 평균을 기준으로 한 상대적 물동량 수준을 의미한다.
   
     3. 12개월 이동평균
    월별 단기 변동과 계절적 영향을 완화하고 장기적인 물동량 흐름을 확인하기 위해 12개월 이동평균을 적용하였다. 이를 통해 개별 월의 증감보다 중장기적인 물동량 변화 추세를 확인할 수 있다.
   
    4. 월별 편차 분석
    각 월의 평균 물동량이 전체 평균에서 얼마나 차이가 나는지 TEU 및 비율로 산출하였다. 이를 통해 단순한 평균 이상·이하 구분뿐만 아니라 월별 물동량 차이의 크기를 정량적으로 비교하였다.
    
    5. 시계열 분해
    월별 물동량을 Trend(장기추세), Seasonal(계절성), Residual(불규칙 변동)로 분해하였다. 또한 연도별 실제 월 패턴을 비교한 결과, 모든 월이 동일한 형태로 반복되지는 않았으나 일부 월 구간에서 반복적인 상승·하락 패턴이 관찰되었다.
    종합 결과
    부산항 월별 컨테이너 물동량은 장기적인 물동량 변화와 함께 월별로 서로 다른 변동 특성을 보였다. 특히 일부 월에서는 여러 연도에 걸쳐 유사한 증감 패턴이 반복되어 계절적 특징이 관찰되었다. 다만 계절성의 정도는 월별로 차이가 있으므로, 향후 월별 반복률과 전년 동월 대비 증감률 등을 추가 분석하여 반복성과 변화 수준을 정량적으로 검증할 필요가 있다.        
            
        
        



    """
    )


# 전처리 코드

##  월별 평균 계산 
    monthly_avg = (
        season_df
        .groupby('월')['총합']
        .mean()
        .reset_index()
    )


## 2단 헤더에서 필요한 컬럼만 추출 
 
    season_df = df[
        [
            ('Unnamed: 0_level_0', '조회년도'),
            ('Unnamed: 1_level_0', '조회월'),
            ('Unnamed: 2_level_0', '국적선구분'),
            ('TEU', '적'),
            ('Unnamed: 16_level_0', '공'),
            ('Unnamed: 17_level_0', '계')
        ]
            ].copy()
        
    season_df.columns = [
    '년도',
    '월',
    '국적선구분',
    '적컨테이너',
    '공컨테이너',
    '총합'
]
    season_df['년도'] = season_df['년도'].ffill()

    season_df['년도'] = pd.to_numeric(
    season_df['년도'],
    errors='coerce'
)

    season_df['월'] = pd.to_numeric(
        season_df['월'],
        errors='coerce'
    )


    season_df = season_df[
    season_df['국적선구분'] == '계'
    ].copy()


    season_df = season_df.dropna(
    subset=['년도', '월']
)
    season_df['년도'] = season_df['년도'].astype(int)
    season_df['월'] = season_df['월'].astype(int)

    for col in ['적컨테이너', '공컨테이너', '총합']:
        season_df[col] = (
            season_df[col]
            .astype(str)
            .str.replace(',', '', regex=False)
            .str.strip()
        )

        season_df[col] = pd.to_numeric(
            season_df[col],
            errors='coerce'
        )

    season_df['date'] = pd.to_datetime(
        dict(
            year=season_df['년도'],
            month=season_df['월'],
            day=1
              ))
    
    season_df = season_df.sort_values('date')   
 
## 날짜를 인덱스로 설정
    ts = (
        season_df
        .set_index('date')['총합']
        .sort_index()
    )

## 시계열 분해
    decomposition = seasonal_decompose(
        ts,
        model='additive',
        period=12
    )
## 결과를 DataFrame으로 변환
    decomp_df = pd.DataFrame({
        'date': ts.index,
        '실제 물동량': ts.values,
        '장기추세': decomposition.trend.values,
        '계절성': decomposition.seasonal.values,
        '잔차': decomposition.resid.values
    })