#전체 코드
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

   
    # 데이터 전처리
    
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


    
    # 계절성 분석 탭
    

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        '1. 월별 평균',
        '2. 성수기 / 비수기',
        '3. 12개월 이동평균',
        '4. 월별 편차',
        '5. 시계열 분해'
    ])


    with tab1:

        st.header('1. 월별 물동량 수준에 차이가 있는가?')

        st.markdown("""
        2012~2024년의 동일한 월끼리 묶어 평균 물동량을 계산한다.

        이를 통해 1월부터 12월까지
        **월에 따라 물동량 수준에 차이가 존재하는지** 확인한다.
        """)

    # 월별 평균 계산
        monthly_avg = (
            season_df
            .groupby('월')['총합']
            .mean()
            .reset_index()
        )

        monthly_avg.columns = [
            '월',
            '평균물동량'
        ]
        monthly_avg['평균물동량_1000TEU'] = (monthly_avg['평균물동량']/1000)
       
        # 표 확인
        st.dataframe(
            monthly_avg,
            use_container_width=True
        )

        # 그래프
        fig_monthly_avg = px.bar(
            monthly_avg,
            x='월',
            y='평균물동량_1000TEU',
            title='2012~2024 월별 평균 컨테이너 물동량',
            labels={
                '월': '월',
                '평균물동량_1000TEU': '평균 물동량(TEU)'
            }
        )

        fig_monthly_avg.update_xaxes(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=[f'{i}월' for i in range(1, 13)]
        )

        fig_monthly_avg.update_yaxes(
            tickformat=',.0f'
        )
        #plotly 
        fig_monthly_avg.add_annotation(
        text='단위: 1,000 TEU',
        x=1,
        y=1.08,
        xref='paper',
        yref='paper',
        showarrow=False,
        xanchor='right'
    )


        st.plotly_chart(
            fig_monthly_avg,
            use_container_width=True,
            key='monthly_avg_chart'
        )

        st.markdown("""
        **분석 결과**

        월별 평균 물동량에 차이가 나타난다면,
        특정 월에 물동량이 상대적으로 높거나 낮아지는
        경향이 존재할 가능성이 있다.

        **→ 그렇다면 전체 평균보다 물동량이 많은 달과 적은 달은 언제인가?**
        """)

    with tab2:

        st.header('2. 상대적으로 물동량이 많은 시기는 언제인가?')

        st.markdown("""
        월별 평균 물동량을 전체 월 평균과 비교한다.

        이를 통해 전체 평균보다 높은 달과 낮은 달을 구분하여
        **상대적으로 물동량이 많은 시기와 적은 시기**를 확인한다.
        """)

        # 월별 평균 계산
        monthly_avg = (
            season_df
            .groupby('월')['총합']
            .mean()
            .reset_index()
        )

        monthly_avg.columns = [
            '월',
            '평균물동량'
        ]

        # 전체 월 평균
        overall_avg = monthly_avg['평균물동량'].mean()

        # 성수기 / 비수기 구분
        monthly_avg['구분'] = monthly_avg['평균물동량'].apply(
            lambda x:
                '성수기' if x > overall_avg
                else '비수기' if x < overall_avg
                else '보통'
        )

        # 전체 평균과의 차이
        monthly_avg['평균대비차이'] = (
            monthly_avg['평균물동량'] - overall_avg
        )

        # 그래프 표시용 1,000 TEU 단위
        monthly_avg['평균물동량_천TEU'] = (
            monthly_avg['평균물동량'] / 1000
        )

        overall_avg_천TEU = overall_avg / 1000


        # 전체 평균 표시
        st.metric(
            '전체 월 평균 물동량 (1,000 TEU)',
                 f'{overall_avg_천TEU:,.1f}'
        )
        

        # 표
        
         # 표 출력용
        display_df = monthly_avg[
            [
                '월',
                '평균물동량',
                '평균대비차이',
                '구분'
            ]
        ].copy()

        # 화면 표시만 1,000 TEU 단위로 변환
        display_df['평균물동량'] = (
            display_df['평균물동량'] / 1000
        )

        display_df['평균대비차이'] = (
            display_df['평균대비차이'] / 1000
        )

        # 소수점 1자리
        display_df['평균물동량'] = display_df['평균물동량'].round(1)
        display_df['평균대비차이'] = display_df['평균대비차이'].round(1)

        # 표 컬럼명에 단위 표시
        display_df = display_df.rename(
            columns={
                '평균물동량': '평균물동량 (1,000 TEU)',
                '평균대비차이': '평균대비차이 (1,000 TEU)'
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


        # 그래프
        fig_peak = px.line(
            monthly_avg,
            x='월',
            y='평균물동량_천TEU',
            markers=True,
            title='월별 평균 물동량과 전체 평균 비교',
            labels={
                '월': '월',
                '평균물동량_천TEU': '평균 물동량'
            }
        )


        # 전체 평균 기준선
        fig_peak.add_hline(
            y=overall_avg_천TEU,
            line_dash='dash',
            annotation_text=f'<b>전체 평균 : {overall_avg_천TEU:,.1f}</b>',
            annotation_position='top left',
            annotation_font_size=13
        )


        # X축
        fig_peak.update_xaxes(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=[f'{i}월' for i in range(1, 13)]
        )


        # Y축
        fig_peak.update_yaxes(
            tickformat=',.0f'
        )


        # 그래프 우측 상단 단위 표시
        fig_peak.add_annotation(
            text='단위: 1,000 TEU',
            x=1,
            y=1.08,
            xref='paper',
            yref='paper',
            showarrow=False,
            xanchor='right'
        )


        st.plotly_chart(
            fig_peak,
            use_container_width=True,
            key='peak_chart'
        )


        st.markdown("""
        **분석 결과**

        전체 월 평균보다 높은 달은 상대적으로 물동량이 많은 달,
        낮은 달은 상대적으로 물동량이 적은 달로 볼 수 있다.

        이 분류는 공식적인 성수기·비수기 기준이 아니라,
        **2012~2024년 월별 평균을 기준으로 한 상대적 분류**이다.

        **→ 그런데 이 차이가 장기적인 물동량 증가나 감소 때문에 나타난 것은 아닐까?**
        """)
        with tab3:

            

            st.markdown("""
            ## 3. 장기적으로 물동량은 어떻게 변화했는가?


            월별 컨테이너 물동량은 계절적 요인, 연휴, 선박 운항 일정,

            일시적인 물류 변화 등에 따라 매월 크게 상승하거나 하락할 수 있다.

            이러한 월별 변동만으로는 부산항 물동량이 장기적으로
            증가하고 있는지, 감소하고 있는지 판단하기 어렵다.

            따라서 본 분석에서는 **12개월 이동평균**을 사용하였다.

            12개월 이동평균은 현재 월을 기준으로 최근 12개월의
            물동량 평균을 연속적으로 계산하는 방법으로

            월별 데이터의 단기적인 급등·급락을 완화하여
            **전체 물동량의 중장기적인 흐름을 보다 쉽게 확인할 수 있다.**

            월별 자료에서 12개월을 사용하는 이유는
            **1년 전체의 계절 변동을 하나의 구간에 포함할 수 있기 때문**이다.

            그래프에서는 다음 내용을 중심으로 확인한다.

            - 월별 실제 물동량이 얼마나 크게 변동하는지
            - 12개월 이동평균이 장기적으로 상승 또는 하락하는지
            - 물동량의 장기적인 방향이 바뀌는 시점이 존재하는지
            - 특정 월의 급등·급락이 일시적인 현상인지 장기적인 변화인지
            - 월별 변동과 장기 추세가 서로 어떻게 다른지

            즉, 이 분석의 목적은 단순히 물동량의 증가·감소를 보는 것이 아니라
            
            **단기적인 월별 변동과 장기적인 물동량 변화 추세를 구분하는 것**이다.
            """)

            # 12개월 이동평균 계산
            season_df['12개월이동평균'] = (
                season_df['총합']
                .rolling(12)
                .mean()
            )

            # 그래프 표시용 1,000 TEU 단위
            season_df['총합_천TEU'] = (
                season_df['총합'] / 1000
            )

            season_df['12개월이동평균_천TEU'] = (
                season_df['12개월이동평균'] / 1000
            )


            # 그래프
            fig_moving = px.line(
                season_df,
                x='date',
                y=[
                    '총합_천TEU',
                    '12개월이동평균_천TEU'
                ],
                title='부산항 월별 물동량과 12개월 이동평균',
                labels={
                    'date': '연도',
                    'value': '물동량',
                    'variable': ''
                }
            )


            # 범례 이름 변경
            fig_moving.for_each_trace(
                lambda trace: trace.update(
                    name={
                        '총합_천TEU': '월별 물동량',
                        '12개월이동평균_천TEU': '12개월 이동평균'
                    }.get(trace.name, trace.name)
                )
            )


            # Y축 숫자 형식
            fig_moving.update_yaxes(
                tickformat=',.0f'
            )


            # 우측 상단 단위
            fig_moving.add_annotation(
                text='<b>단위: 1,000 TEU</b>',
                x=1,
                y=1.08,
                xref='paper',
                yref='paper',
                showarrow=False,
                xanchor='right',
                font=dict(size=14)
            )


            # 범례
            fig_moving.update_layout(
                legend=dict(
                    orientation='h',
                    x=0,
                    y=1.08
                )
            )


            st.plotly_chart(
                fig_moving,
                use_container_width=True,
                key='moving_average_chart'
            )


            st.markdown("""
            ### **단순 그래프로만 파악 가능한 점**
            
            


            월별 물동량 선은 실제 월별 변화를 나타내기 때문에
            상승과 하락이 비교적 크게 나타난다.

            반면 12개월 이동평균선은 최근 1년의 평균을 이용하므로
            월별 변동보다 부드러운 형태로 나타나며,
            부산항 물동량의 장기적인 방향을 파악하는 데 활용할 수 있다.

            - 월별 물동량만 급등하거나 급락하고 이동평균의 변화가 크지 않다면
            일시적인 변동일 가능성이 있다.
            - 월별 물동량과 이동평균이 함께 지속적으로 상승한다면
            전체적인 물동량 수준이 증가하는 흐름으로 볼 수 있다.
            - 이동평균이 상승하다 하락하거나, 하락하다 상승하는 구간은
            장기적인 물동량 흐름이 변화하는 시점으로 볼 수 있다.
            """
            )
            st.markdown("""
            ### 분석 결과

            12개월 이동평균을 통해 월별 물동량의 단기적인 변동을 완화하여 살펴본 결과,
            **2013년부터 2024년까지 부산항 컨테이너 물동량은 전체적으로 상승하는 장기 흐름**을 보인다.

            #### ① 2013~2016년 : 완만한 증가

            분석 초기에는 12개월 이동평균이 약 **1,400~1,500 수준에서 시작하여
            1,600 수준까지 점진적으로 상승**하는 모습이 나타난다.

            월별 실제 물동량은 일부 시점에서 크게 감소하기도 하지만,
            이동평균은 비교적 안정적으로 상승하고 있다.

            따라서 개별 월의 일시적인 변동과 별개로
            이 기간에는 **물동량의 전반적인 수준이 점차 높아지는 흐름**이 나타났다고 볼 수 있다.


            #### ② 2017~2019년 : 물동량 수준의 한 단계 상승

            2017년 이후 이동평균선의 상승이 이전보다 뚜렷하게 나타나며,
            2018~2019년에는 약 **1,800 수준까지 상승**한다.

            특히 월별 실제 물동량은 지속적으로 등락하지만
            이동평균 자체가 이전 기간보다 높은 수준에서 형성되고 있다.

            이는 단순히 특정 월의 물동량만 증가한 것이 아니라
            **연간 평균적인 물동량 수준 자체가 이전보다 높아졌음을 보여준다.**


            #### ③ 2020~2022년 : 높은 수준을 유지하면서 정체와 변동 발생

            2020년 이후에는 월별 실제 물동량의 변동 폭이 이전보다 크게 나타나는 구간이 확인된다.

            반면 12개월 이동평균은 대체로 **1,800 수준 이상을 유지하면서
            상승과 정체를 반복**한다.

            따라서 일부 월에서 큰 증가 또는 감소가 발생하더라도
            장기적인 물동량 수준 전체가 동일한 폭으로 움직인 것은 아니라는 것을 확인할 수 있다.

            특히 이러한 차이는 **월별 실제값만으로 장기 추세를 판단하기 어려운 이유**를 보여준다.


            #### ④ 2023~2024년 : 조정 이후 다시 상승

            2023년 전후에는 월별 물동량이 크게 감소하는 시점이 나타나고
            12개월 이동평균 역시 일시적으로 낮아지는 모습이 확인된다.

            그러나 이후 이동평균이 다시 상승하여
            2024년에는 분석기간 중 비교적 높은 수준에 도달한다.

            따라서 최근 구간에서는 단기적인 감소 이후
            **물동량의 장기적인 수준이 다시 상승하는 흐름**이 나타난다.


            ### 종합 해석

            전체 분석기간을 보면 월별 물동량은 지속적으로 상승과 하락을 반복하지만,
            12개월 이동평균은 장기적으로 우상향하는 모습을 보인다.

            즉, 부산항 물동량은 매월 일정하게 증가한 것이 아니라
            **단기적인 급등·급락과 일정 기간의 정체를 반복하면서도
            전체적인 물동량 수준은 장기적으로 높아진 것**으로 해석할 수 있다.

            또한 월별 실제값의 큰 변동이 항상 장기적인 추세 변화로 이어지는 것은 아니었다.
            따라서 월별 물동량만 보는 것보다 12개월 이동평균을 함께 확인하는 것이
            장기적인 물동량의 방향을 파악하는 데 유용하다.

            **→ 그렇다면 이러한 장기적인 증가 추세를 제외하고 보았을 때도
            특정 월이 반복적으로 높거나 낮게 나타나는가?**
            """)



        with tab4:

            st.header('4. 월별 물동량은 전체 평균에서 얼마나 차이가 나는가?')

            st.markdown("""
            앞선 분석에서는 월별 평균을 이용하여 상대적으로 물동량이 높은 달과
            낮은 달을 확인하고, 12개월 이동평균을 통해 장기적인 물동량 변화도 살펴보았다.

            이번에는 각 월의 평균 물동량이 **전체 월 평균에서 실제로 얼마나 차이가 나는지**
            편차를 계산한다.

            월별 편차는 다음과 같이 계산한다.

            **월별 편차 = 해당 월의 평균 물동량 - 전체 월 평균 물동량**

            편차가 **양수(+)**이면 전체 평균보다 물동량이 많은 달이고,
            **음수(-)**이면 전체 평균보다 물동량이 적은 달이다.

            또한 편차의 절댓값이 클수록 해당 월의 물동량이
            전체 평균에서 더 크게 벗어나 있다는 의미이다.

            따라서 단순히 평균보다 높은 달과 낮은 달을 구분하는 것을 넘어,
            **월별 물동량 차이가 어느 정도의 크기로 나타나는지** 확인할 수 있다.
            """)

            # 월별 평균 계산
            monthly_avg = (
                season_df
                .groupby('월')['총합']
                .mean()
                .reset_index()
            )

            monthly_avg.columns = [
                '월',
                '평균물동량'
            ]

            # 전체 월 평균
            overall_avg = monthly_avg['평균물동량'].mean()

            # 월별 편차
            monthly_avg['평균대비차이'] = (
                monthly_avg['평균물동량'] - overall_avg
            )

            # 화면 표시용 1,000 TEU
            monthly_avg['평균대비차이_천TEU'] = (
                monthly_avg['평균대비차이'] / 1000
            )

            # 표 출력용
            display_deviation = monthly_avg[
                [
                    '월',
                    '평균물동량',
                    '평균대비차이'
                ]
            ].copy()

            display_deviation['평균물동량'] = (
                display_deviation['평균물동량'] / 1000
            ).round(1)

            display_deviation['평균대비차이'] = (
                display_deviation['평균대비차이'] / 1000
            ).round(1)

            display_deviation = display_deviation.rename(
                columns={
                    '평균물동량': '평균물동량 (1,000 TEU)',
                    '평균대비차이': '평균대비차이 (1,000 TEU)'
                }
            )

            st.dataframe(
                display_deviation,
                use_container_width=True,
                hide_index=True
            )

            # 월별 편차 그래프
            fig_deviation = px.bar(
                monthly_avg,
                x='월',
                y='평균대비차이_천TEU',
                title='월별 평균 물동량의 전체 평균 대비 편차',
                labels={
                    '월': '월',
                    '평균대비차이_천TEU': '전체 평균 대비 편차'
                }
            )

            # 편차 0 기준선
            fig_deviation.add_hline(
                y=0,
                line_dash='dash',
                annotation_text='<b>전체 평균 기준</b>',
                annotation_position='top left',
                annotation_font_size=16
            )

            fig_deviation.update_xaxes(
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=[f'{i}월' for i in range(1, 13)]
            )

            fig_deviation.update_yaxes(
                tickformat=',.0f'
            )

            # 우측 상단 단위
            fig_deviation.add_annotation(
                text='<b>단위: 1,000 TEU</b>',
                x=1,
                y=1.08,
                xref='paper',
                yref='paper',
                showarrow=False,
                xanchor='right',
                font=dict(size=14)
            )

            st.plotly_chart(
                fig_deviation,
                use_container_width=True,
                key='deviation_chart'
            )

            st.markdown("""
            ### 그래프 해석 방법

            그래프의 **0선은 2012~2024년 전체 월 평균 물동량**을 의미한다.

            - 막대가 0보다 위에 있으면 해당 월의 평균 물동량이 전체 평균보다 높다.
            - 막대가 0보다 아래에 있으면 해당 월의 평균 물동량이 전체 평균보다 낮다.
            - 막대의 길이가 길수록 전체 평균과의 차이가 큰 월이다.
            - 0에 가까운 월은 전체 평균과 비교적 비슷한 물동량 수준을 가진다.

            이를 통해 어떤 월이 단순히 평균보다 높거나 낮은지를 넘어,
            **월별 차이가 실제로 어느 정도의 규모로 나타나는지** 비교할 수 있다.

            **→ 그렇다면 이러한 월별 차이는 단순한 우연한 변동일까,
            아니면 장기 추세를 제거한 뒤에도 반복적으로 나타나는 계절적 패턴일까?**
            """)


        with tab5:

            st.header('5. 장기추세와 계절성을 분리하면 어떤 패턴이 나타나는가?')

            st.markdown("""
            앞선 분석에서는 월별 평균 물동량에 차이가 있다는 것을 확인하였다.

            하지만 실제 월별 물동량에는 단순한 월별 특성뿐만 아니라
            시간이 지나면서 전체 물동량 수준이 증가하거나 감소하는
            **장기적인 변화도 함께 포함되어 있다.**

            따라서 월별 평균만 비교하면 특정 월의 물동량이 높은 이유가
            실제로 반복되는 계절적 특성 때문인지,
            전체 물동량 수준이 장기적으로 증가했기 때문인지 구분하기 어렵다.

            이를 구분하기 위해 **시계열 분해(Time Series Decomposition)**를 사용한다.

            시계열 분해는 실제 물동량의 움직임을 다음 세 가지 요소로 나누어 살펴보는 방법이다.

            - **Trend(장기추세)** : 시간이 지나면서 물동량의 기본적인 수준이 어떻게 변화하는가
            - **Seasonal(계절성)** : 특정 월에 반복적으로 나타나는 상승·하락 패턴이 있는가
            - **Residual(잔차)** : 장기추세와 계절성으로 설명되지 않는 일시적·불규칙한 변동

            즉 이번 분석의 핵심은 단순히 어느 달의 물동량이 높고 낮은지를 보는 것이 아니라,

            **장기적인 물동량 변화와 분리한 뒤에도 특정 월의 상승·하락이 반복되는지를 확인하는 것**이다.
            """)

            # 날짜를 인덱스로 설정하여 시계열 데이터 생성
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

            # 분해 결과 데이터프레임
            decomp_df = pd.DataFrame({
                'date': ts.index,
                '실제 물동량': ts.values,
                '장기추세': decomposition.trend.values,
                '계절성': decomposition.seasonal.values,
                '잔차': decomposition.resid.values
            })

        
                # ==========================================
            # 5-1. Trend(장기추세)
            # ==========================================

            # 그래프 표시용 1,000 TEU
            decomp_df['장기추세_천TEU'] = (
                decomp_df['장기추세'] / 1000
            )

            fig_trend = px.line(
                decomp_df,
                x='date',
                y='장기추세_천TEU',
                title='부산항 컨테이너 물동량의 장기추세(Trend)',
                labels={
                    'date': '연도',
                    '장기추세_천TEU': '장기추세'
                }
            )

            fig_trend.update_yaxes(
                tickformat=',.0f'
            )

            # 우측 상단 단위
            fig_trend.add_annotation(
                text='<b>단위: 1,000 TEU</b>',
                x=1,
                y=1.08,
                xref='paper',
                yref='paper',
                showarrow=False,
                xanchor='right',
                font=dict(size=14)
            )

            st.plotly_chart(
                fig_trend,
                use_container_width=True,
                key='trend_chart'
            )


              # 그래프 표시용 1,000 TEU
            decomp_df['계절성_천TEU'] = (
                decomp_df['계절성'] / 1000
            )

            fig_seasonal = px.line(
                decomp_df,
                x='date',
                y='계절성_천TEU',
                title='부산항 컨테이너 물동량의 계절성(Seasonal)',
                labels={
                    'date': '연도',
                    '계절성_천TEU': '계절적 효과'
                }
            )

            # 계절성 0 기준선
            fig_seasonal.add_hline(
                y=0,
                line_dash='dash',
                annotation_text='<b>계절적 효과 0</b>',
                annotation_position='top left',
                annotation_font_size=16
            )

            fig_seasonal.update_yaxes(
                tickformat=',.0f'
            )

            # 우측 상단 단위
            fig_seasonal.add_annotation(
                text='<b>단위: 1,000 TEU</b>',
                x=1,
                y=1.08,
                xref='paper',
                yref='paper',
                showarrow=False,
                xanchor='right',
                font=dict(size=14)
            )

            st.plotly_chart(
                fig_seasonal,
                use_container_width=True,
                key='seasonal_chart'
            )
                    # 5-2-1. 월별 대표 계절 효과
            # ==========================================

            # 계절성 값에서 대표 12개월 추출
            seasonal_pattern = pd.DataFrame({
                '월': list(range(1, 13)),
                '계절효과': decomposition.seasonal.iloc[:12].values
            })

            # 1,000 TEU 단위
            seasonal_pattern['계절효과_천TEU'] = (
                seasonal_pattern['계절효과'] / 1000
            )

            st.markdown("""
            ### 월별 대표 계절 효과

            시계열 분해에서 추정된 12개월 계절 패턴을
            1월부터 12월까지 한 번만 추출하여 비교한다.

            이 그래프를 통해 특정 월이 장기 추세와 분리된 이후에도
            상대적으로 물동량을 증가시키는 방향인지,
            감소시키는 방향인지 확인할 수 있다.
            """)

            fig_seasonal_month = px.bar(
                seasonal_pattern,
                x='월',
                y='계절효과_천TEU',
                title='월별 대표 계절 효과',
                labels={
                    '월': '월',
                    '계절효과_천TEU': '계절적 효과'
                }
            )

            # 0 기준선
            fig_seasonal_month.add_hline(
                y=0,
                line_dash='dash',
                annotation_text='<b>계절 효과 0</b>',
                annotation_position='top left',
                annotation_font_size=16
            )

            # X축 1월~12월
            fig_seasonal_month.update_xaxes(
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=[f'{i}월' for i in range(1, 13)]
            )

            # Y축
            fig_seasonal_month.update_yaxes(
                tickformat=',.0f'
            )

            # 우측 상단 단위
            fig_seasonal_month.add_annotation(
                text='<b>단위: 1,000 TEU</b>',
                x=1,
                y=1.08,
                xref='paper',
                yref='paper',
                showarrow=False,
                xanchor='right',
                font=dict(size=14)
            )

            st.plotly_chart(
                fig_seasonal_month,
                use_container_width=True,
                key='seasonal_month_chart'
            )

            st.markdown("""
                ### 월별 평균 편차와 계절 효과 비교

                월별 평균 편차와 시계열 분해를 통해 추정한 계절 효과를 비교한 결과,
                두 분석의 월별 패턴이 완전히 동일하지는 않았다.

                월별 평균 편차는 분석기간 전체에서 같은 월의 물동량을 평균하여
                전체 평균과 비교한 값이므로, 장기간에 걸친 물동량 수준의 변화가
                함께 포함되어 있다.

                반면 Seasonal은 시계열의 장기적인 추세를 분리한 뒤
                12개월을 주기로 반복되는 월별 효과를 추정한 결과이다.

                따라서 특정 월의 평균 물동량이 전체 평균보다 높더라도,
                장기추세를 고려한 계절 효과는 음(-)으로 나타날 수 있으며
                반대의 경우도 가능하다.

                실제 분석에서도 일부 월은 두 분석의 방향이 다르게 나타났다.

                이는 **단순히 특정 월의 평균 물동량이 높거나 낮다는 사실만으로
                계절성을 판단하기 어렵다는 것을 보여준다.**

                따라서 부산항 물동량의 계절적 특성을 해석할 때는
                월별 평균뿐 아니라 장기추세를 분리한 계절 효과를 함께 고려할 필요가 있다.
                """)



                            # ==========================================
            # 5-3. Residual(잔차)
            # ==========================================

            st.markdown("""
            ### 5-3. 잔차(Residual)

            마지막으로 장기추세(Trend)와 계절성(Seasonal)을 제거한 뒤에도
            남아 있는 **불규칙한 물동량 변동**을 확인한다.

            잔차는 장기적인 증가·감소 흐름이나 매년 반복되는 월별 패턴으로
            설명되지 않는 부분을 의미한다.

            - **0에 가까운 값** : 추세와 계절성으로 비교적 잘 설명되는 시점
            - **큰 양수(+)** : 예상되는 수준보다 물동량이 크게 증가한 시점
            - **큰 음수(-)** : 예상되는 수준보다 물동량이 크게 감소한 시점

            따라서 잔차가 크게 나타나는 시점을 확인하면
            일반적인 장기추세와 계절적 패턴만으로 설명하기 어려운
            **비정상적으로 큰 증가 또는 감소 시점**을 찾을 수 있다.
            """)

            # 그래프 표시용 1,000 TEU
            decomp_df['잔차_천TEU'] = (
                decomp_df['잔차'] / 1000
            )

            fig_residual = px.bar(
                decomp_df,
                x='date',
                y='잔차_천TEU',
                title='부산항 컨테이너 물동량의 잔차(Residual)',
                labels={
                    'date': '연도',
                    '잔차_천TEU': '잔차'
                }
            )

            # 잔차 0 기준선
            fig_residual.add_hline(
                y=0,
                line_dash='dash',
                annotation_text='<b>잔차 0</b>',
                annotation_position='top left',
                annotation_font_size=16
            )

            fig_residual.update_yaxes(
                tickformat=',.0f'
            )

            # 우측 상단 단위
            fig_residual.add_annotation(
                text='<b>단위: 1,000 TEU</b>',
                x=1,
                y=1.08,
                xref='paper',
                yref='paper',
                showarrow=False,
                xanchor='right',
                font=dict(size=14)
            )

            st.plotly_chart(
                fig_residual,
                use_container_width=True,
                key='residual_chart'
            )