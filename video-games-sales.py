import streamlit as st 
import pandas as pd 
import chart_studio.plotly as py
import plotly.graph_objects as go
import plotly as plt 
import plotly.express as px

#Page name and Icon 
st.set_page_config(page_title='Video Games Sales ', page_icon="🎮")

st.title("Video Games Sales Analysis")
from PIL import Image 
st.image("https://cdn.arstechnica.net/wp-content/uploads/2018/01/consoles-800x491.jpg", width = 600)

df = pd.read_csv("https://raw.githubusercontent.com/ziadshehabb/video-games-sales/main/vgsales.csv")

gamer = st.radio(
     "ARE YOU A GAMER?",
     ('YES!', 'No.'))

if gamer == 'YES!':
     st.markdown("![Alt Text](https://media3.giphy.com/media/l0HUnQR733uhm48UM/200w.webp?cid=ecf05e474uu1m1io04ax3lzxfb4w3ljim5q54qr7u9mjyay2&rid=200w.webp&ct=g)")
else:
     st.markdown("![Alt Text](https://media4.giphy.com/media/14dXclYKbx2ONW/200.webp?cid=ecf05e47qpwwhpq06opy8se2lifdjik29z52mkiwkwm5f90x&rid=200.webp&ct=g)")


#Data set
data_load_state = st.text('Loading data...')
agree = st.checkbox('First 10 rows')

if agree:
     st.subheader('First ten rows')
     st.dataframe(df.head(10))
     data_load_state.text('Loading data...done!')

agree = st.checkbox('Full data set')

if agree:
     st.subheader('Full data set')
     st.write(df)
     data_load_state.text('Loading data...done!')
     

df.isnull().sum()
df = df.dropna()
df.Genre.unique()

#FIGURE ONE
st.subheader('How Popular Are Video Games?')
df1 =  df.groupby('Year')['Name'].count().reset_index()
data = [go.Bar(x=df1.Year,
            y=df1.Name)]
layout=go.Layout(title='Yearly Number of games released', xaxis=dict(title='Year'), yaxis= dict(title='Number of games released'))

figure1=go.Figure(data=data, layout=layout)
figure1.update_xaxes(
    range=[1980,2016], 
    constrain="domain", 
)
st.plotly_chart(figure1)
st.write("We can see a steady increase in the number of games released from 1980 until the high peak in 2009, and then a decrease since then. ")

#FIGURE TWO
st.subheader('Which Video Game Platform Is The Most Popular? ')
df2 =  df.groupby('Platform')['Global_Sales'].count().reset_index()
data = [go.Bar(x=df2.Platform,
            y=df2.Global_Sales)]
layout=go.Layout(title='Global Sales per Platform between 1980 and 2020', xaxis=dict(title='Platform'), yaxis= dict(title='Global Sales'))

figure2=go.Figure(data=data, layout=layout)
st.plotly_chart(figure2)
st.write("PS2 and Nintendo DS the highest selling platform in the period between 1980 and 2016. ")

#FIGURE THREE
st.subheader('Sales VS Genre VS Year')
df = df.sort_values("Year")
df3 = df[df.Genre != "Platform"]
figure3 = px.bar(df3, x="Genre", y="Global_Sales", animation_frame="Year", animation_group="Genre",
           color="Genre", hover_name="Genre", range_y=[0,3], range_x=[0,10], title = "Change of Global Sales per Genre by Year")
st.plotly_chart(figure3)
st.write("Increases in all Genres are observed up until 1991, were the following Genres remained major in the market : Shooter, Misc, Action, Sports, and Fighting ")

#FIGURE FOUR 
st.subheader('Which Video Game Genre Is The Most Popular? ')
figure4 = px.pie(df, names = df.Genre, values = df['Global_Sales'], hole = 0.2)
figure4.update_layout(
    title_text="Global Sales by Genre",
    annotations=[dict(text='Genre', x=0.5, y=0.5, font_size=20, showarrow=False)])
st.plotly_chart(figure4)

#FIGURE FIVE
st.subheader('Interactive Scatterplot Playaround')
selected_x_var = st.selectbox('What do you want the x variable to be?', ('Genre','Platform','Publisher','Year') )
selected_y_var = st.selectbox('What about the y?', ('NA_Sales','EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales'))
fig = px.bar(df, x = df[selected_x_var], y = df[selected_y_var], color="Genre")
st.plotly_chart(fig)

#FIGURE SIX
st.subheader("Genre Level Analysis")
glist = df['Genre'].unique()
st.sidebar.title("Genre Level Analysis Visualization Selector")
select_genre = st.sidebar.selectbox("Select a Genre:",glist)
fig = px.bar(df[df['Genre'] == select_genre], 
    x = 'Year', y = "Global_Sales")
st.markdown(" Overall Global Sales " +
    " in %s genre per platform between 1980 and 2016 " % (select_genre))
st.plotly_chart(fig)

#Download data set
def convert_df(df):
     return df.to_csv().encode('utf-8')

csv = convert_df(df)
st.download_button(
     label="Download video games sales data as CSV",
     data=csv,
     file_name='Video_games_sales.csv',
     mime='text/csv',)


 
 