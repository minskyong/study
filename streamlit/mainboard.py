import streamlit as st

from view.port1 import port_1
from view.port2 import port_2
from view.port3 import port_3
st.set_page_config(
    page_title = '운영 대시보드' ,  
    layout = 'wide',
    initial_sidebar_state = 'expanded'


)

with st.sidebar:
    st.title('메뉴')

    menu = st.radio(
        label = '대시보드선택',
        options = [ '북항','신항','신항2']
        )



if menu == '북항' :
   
            st.title('북항')
            st.write('북항입니다.')
elif menu == '신항' :
   
            st.title('신항')
            st.write('신항이다.')

elif menu == '신항2' :
       
            st.title('신항2')   
            st.write('신항2')

#with st.container():
       # st.write(f'선택된 메뉴 : {menu}')   

# 아래처럼도 가능 

st.write('---')






if menu == '북항' :
   port_1()

elif menu == '신항' :
    port_2()

elif menu == '신항2' :
    port_3()