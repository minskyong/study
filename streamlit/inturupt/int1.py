import streamlit as st
#버튼 불린 확인



st.title ('버튼')

cl = st.button('확인')
if cl == True:
     st.write('누름')
else :
     st.write('안누름')

st.write(cl)


if st.button('분석시작'):
     st.success('성공')