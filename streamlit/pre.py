import streamlit as st
import pandas as pd

data = pd.DataFrame({
        '번호' : range(1,51),
        '점수' : range(1,51),
        '단가' : range(1,51),
        '입출항횟수' : range(1,51),
        '수출횟수' : range(1,51),
        '수입횟수' : range(1,51),
        '번호' : range(1,51),

}
)

display_df = data[ 
    ['입출항횟수','수출횟수','수입횟수']
]

st.dataframe(
   
   display_df,
   height = 300,
)

product = pd.DataFrame({
    '상품' : ['노트북','키보드','모니터'],
    '단가' : [1_500_000,350_000,1_200_000]

})
#보기 어려운 수 원화로 적어놓기 column_config = 
                        # {'컬럼명' : st.column_config.NumberColumn('변경할 이름')}}
                        #   format = (숫자)
st.dataframe(           
    product ,
    column_config = {'단가' : st.column_config.NumberColumn('단가(원)', format = '%,d원')}
)


achievements_data = pd.DataFrame({
                    '부서': ['영업팀','개발팀','마케팅팀'],
                    '달성률' : [82,92,68]})



st.dataframe(achievements_data,
             column_config = {
                 '달성률': st.column_config.NumberColumn('목표 달성률', format = '%d%%')
             })


st.write('---')



progress_data = pd.DataFrame({
                    '기술명': ['python','pandas','streamlit'],
                    '진행률' : [82,92,68]})



st.dataframe(progress_data,
             column_config = {
                 '진행률': st.column_config.NumberColumn('학습진행률', 
                                                        min_value = 0,
                                                        max_value = 100,
                                                        format = '%d%%')
             },
        hide_index =True )


st.metric(
    '총매출', 
    value = '3,000,0000원',
    delta = '20,000원'


)
#성장률 보기
current_sales = 35_000_000
previous_sales = 32_500_000

#성장률 보기
growth_rate = (current_sales-previous_sales) /previous_sales * 100

st.metric(
    label = '이번달 매출',
    value = f'{current_sales : }원',
    delta = f'{growth_rate : .2f}%'
)

st.metric(
        label = '일일 환적 처리 시간',
        value = '8.2시간',
        delta = '-0.8시간',
        delta_color =  'inverse'     # 감소가 긍정일 경우 inverse 사용해서  delta 색변경 
)