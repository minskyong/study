import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt 


#matplotlib로 그래프 그리기 
st.title('matplotlib')

sales = pd.DataFrame({
    'month' : ['jan',
               'feb',
               'mar',
               'apr',
               'may',
               'jun'],

    'sales' : [12.5,
               13.8,
               11.5,
               14.6,
               16.9,
               19.2]
})

fig,ax = plt.subplots( figsize = (10,6) )

ax.plot(
     sales['month'],
     sales['sales'],
    marker = 'o'
)

ax.set_title ('monthly sales')
ax.set_xlabel('month')
ax.set_ylabel('sales')

st.pyplot(fig)
plt.close(fig)


st.write('---')

#seaborn 사용 
st.title('seaborn')

fig , ax= plt.subplots(figsize =(10,6))

sns.barplot(
    data = sales,
    x = 'month',
    y = 'sales',
    ax = ax,
)

ax.set_title('Monthly sales')
ax.set_xlabel('month')
ax.set_ylabel('sales')

st.pyplot(fig)
plt.close(fig)