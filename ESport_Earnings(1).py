import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


# type setting
def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")

# read dataset
df = pd.read_csv('ESport_Earnings.csv',encoding='gbk')

# seaborn style, which looks better than the default one
plt.style.use('seaborn')

st.title('ESport Earnings Data by Cheng Ma and Ziyi Zhao')

# import image
st.image(Image.open('dataset-cover.jpg'))

space(1)
# filter
price_filter = st.slider('Total Money Earnings from the game:', 0, 110000000, 80000000)
df_totalmoney = df[df.TotalMoney >= price_filter]

# pie graph
f,ax = plt.subplots(1,1,figsize=(18,8))
x = df_totalmoney['TotalMoney'].groupby(df_totalmoney['Genre']).sum()
ax.pie(df_totalmoney['TotalMoney'].groupby(df_totalmoney['Genre']).sum() , labels = x.index,autopct = '%1.1f%%',shadow = True)
st.pyplot(f)

space(1)

# game categories 
st.header('Here i s a look at the revenue performance of different game categories')

df1=df.drop(['Releaseyear','IdNo'], axis=1)
game_type =  df1.groupby('Genre').sum()
st.write(game_type)

space(2)

# search game (filter)
st.header('Querying Game Data')

form = st.sidebar.form("Game_Name")
name_filter = form.text_input('Game Name (enter ALL to reset)', 'ALL')
form.form_submit_button("Apply")

if name_filter!='ALL':
    df = df[df.GameName.str.lower() == name_filter.lower()]
    st.write(df)
    st.write('(if the form is blank please type "ALL" to reset and type correct name )')
elif name_filter =='ALL':
    st.write('please type name of game')

space(2)

# filter
genre_filter = st.sidebar.multiselect(
    'Genre Selector',    
    df.Genre.unique()
    )
df = df[df.Genre.isin(genre_filter)]

# line graph
st.header('The relationship between the number of players and the earnings of the game')

fig, ax = plt.subplots()
df.sort_values(by = 'PlayerNo', inplace=True)
df.reset_index(drop=True, inplace=True)
x = df.PlayerNo
y = df.TotalMoney
ax.plot(x, y)
ax.set_xlabel('Number of Players')
ax.set_ylabel('Total Money Earnings')

# add scatter and game name
z=df.GameName
plt.scatter(x,y)
for i in range(len(x)):
    plt.annotate(z[i],xy=(x[i],y[i]),xytext=(x[i]+0.1,y[i]+0.1))
plt.show()
st.pyplot(fig)

space(2)

# bar graph
st.header('The relationship between publication time and game earnings')

a=df.Releaseyear.unique()
b=df.groupby('Releaseyear')['TotalMoney'].sum()
f, ax=plt.subplots()
ax.bar(a,b,color='r')
ax.set_ylabel('Total Money Earnings')
ax.set_xlabel('Release year')
plt.show()
st.pyplot(f)

space(2)

# scatterplot
st.header('The relationship between the number of games created and the games earnings')

fig, ax = plt.subplots()
tournament_no=df.TournamentNo
total_money=df.TotalMoney
ax.scatter(tournament_no,total_money)
ax.set_ylabel('Total Money Earnings')
ax.set_xlabel('Number of Tournament')
st.pyplot(fig)

space(2)

# bar graph
st.header('The popularity of different genres in different countries')

df_country, ax=plt.subplots()
y=df.groupby('Top_Country')['Top_Country_Earnings'].sum()
x=df.Top_Country.unique()
ax.bar(x,y,color='m')
plt.xticks(rotation=60)
ax.set_ylabel('Top Country Eaenings')
st.pyplot(df_country)


