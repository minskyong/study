import streamlit as st
import pandas as pd


data = pd.DataFrame({
        '월' : ['1월',
                '2월',
                '3월',
                '4월',
                '5월'],

         '매출': [12_500_000,  
                11_500_000,
                10_500_000,
                9_500_000,
                8_500_000,]
                
})

st.title('월별 매출')

st.line_chart(
    data = data,
    x= '월', 
    y = '매출',
    x_label = '기간',
    y_label = '매출액'

)

st.write('---')


reg_data = pd.DataFrame({
        '월' : ['1월',
                '2월',
                '3월',
                '4월',
                '5월'],

         '부산': [12_500_000,  
                11_500_000,
                10_500_000,
                9_500_000,
                8_500_000,],

        '대전': [12_000_000,  
                11_000_000,
                10_000_000,
                9_000_000,
                8_000_000,]
        
                
                
})

st.title('지역별 월 매출')

st.line_chart(
    data = reg_data,
    x = '월',
    y = ('부산','대전'),
    x_label = '기간',
    y_label = '월 매출액'


)
st.write('---')


st.bar_chart(data = data, x= '월', y = '매출'
                )

st.write('---')


product = pd.DataFrame({
        '상품' : ['모니터',
                '키보드',
                '마우스'],
        '실제매출' : [15_000_000,
                     8_500_000,
                    7_000_000,],
        '목표매출' : [14_000_000,
                    9_000_000,
                    8_000_000  ]


})

pr = product

st.bar_chart(data = pr, x= '상품', y = ['실제매출','목표매출'],
             

      stack = False,       
    horizontal = True            
             
             
)

# 영역 그래프  ( traffic)

traffic = pd.DataFrame({
        '월' : ['1월',
                '2월',
                '3월',
                '4월',
                '5월'],

        '사용량' :  [320,
                    380,
                    370,
                    450,
                    200,]
})


st.title('월별 서비스 사용량')

#선 그래프 영역 다 칠하기 
# #st.area_chart()
st.area_chart(             
data= traffic,
x = '월',
y = '사용량'

)

