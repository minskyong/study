import streamlit as st
import pandas as pd 
import numpy as np

#

"""
streamlit에서 텍스트를 사용하는 방법

title()
subtitle()
header()
write()
text()
code()
markdown()

"""


# streamlit run <실행하고자 하는 파이썬 파일>

# 가장 큰 제목
# st.title('온라인 쇼핑몰 매출 분석')
# # 주요 영역 제목
# st.header('2026년 매출 현황')
# # 세부 영역 제목
# st.subheader('8월 매출')
# # 일반적인 내용
# st.write('8월 매출 데이터를 분석합니다.')

price = 1000
amount = 5

st.write(f'총 가격은 {price * amount}원입니다')

st.title('쇼핑몰 운영 대시보드')
st.header('매출 현황')
st.subheader('금일 매출 현황')
st.write('오늘 발생한 주문의 매출을 확인합니다.')
st.subheader('월간 매출')
st.write('이번달 누적 매출을 확인합니다.')
st.header('고객 현황')
st.subheader('신규 가입자')
st.write('오늘 가입한 신규 고객을 확인합니다.')

st.title('이것은 title이구요')
st.write('**판매량** : 120개')
st.text('**매출액** : 3500000')

st.caption('매출 데이터는 매일 오전 9시에 갱신됩니다.')
st.caption('기준일: 2026-09-15')
st.caption('단위: 1TEU')


st.markdown(
    "이번달 매출은 **무려** **35000000** 이며"
    "*전월보다 많이 증가했습니다 :)*"
)

st.markdown("""
### 매출 분석 결과

이번 달 주요 지표입니다.

- 총 주문수: 30건
- 총 매출: 10만원
- 평균 주문 금액: 3만원

매출은 지난달보다 32.5%증가했습니다.
""")

st.code(
    """
    """
)




st.markdown('---')

scores = [50,60,70,80,90]

st.subheader('학생평균')

score_avg = sum(scores) / len(scores)

st.markdown(f'현재 학생의 평균점수 **{score_avg: .2f}**')


# sehll 
# streamlit run

st.markdown('---')

example_sql ="""
select 
    category, product_name, unit_price
from
    orders
GROUP BY
    catergory
"""

st.code(

    example_sql,
    language = 'sql'
)

st.markdown('---')


sales = pd.DataFrame(
    {'월' : [
            '1월',
            '2월',
            '3월',
            '4월'],
     '매출': [
            1200,
            1400,
            1500,
            1600],
    '판매량': [
            3,
            4,
            6,
            8]
    }
)

sales['가격'] =sales['매출']*sales['판매량']

st.title('월별매출')

st.dataframe(sales, hide_index = True)

st.write('---')

image = np.zeros((200,400,3), dtype = np.uint8)
image[:, 200:] = [1,200,150]

st.image(image)

st.write('---')

st.image('1234.png', width = 200, caption = '뭐고이건.png')

st.write('---')

st.title('수식')
#raw r'값'
st.latex(r'pi = 3.141592\2')

st.latex(r"""
\bar{x} = 
\frac{1}{n} \sum_{i=1}^{n} x_i""")

st.write('---')

st.title('코드실행과정확인')

with st.echo():
    numbers = [10,20,30,40]
    total = sum(numbers)
    st.write(f'합계: {total}')

    st.write('---')

st.info('데이터는 매일 오전 9시에 갱신됨')
st.success('1234')  # 초록색  성공
st.warning('1234')  # 노란색 경고 
st.error('1234')    # 빨간색 에러 

st.write('---')

st.title ('학생 성적 확인')
scores = 85
st.write(f'점수 :{scores} ')

if scores > 90:
    st.success('good')
elif scores >80:
    st.warning ('soso')
else :
    st.error('bad')