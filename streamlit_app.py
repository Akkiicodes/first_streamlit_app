import streamlit
streamlit.title("My Mom's Healthy Diner")
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("let's pick some fruits : ",list(my_fruit_list.index),['Cherries','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

import requests

streamlit.title("Fruityvice Fruit Advice !")
fruit_choice = streamlit.text_input('What kind of fruit would you like info about ?' , 'Kiwi')
streamlit.write('The user entered : ',fruit_choice) 

fruityvice_responce = requests.get('https://fruityvice.com/api/fruit/'+'Kiwi')
#streamlit.text(fruityvice_responce.json())
fruityvice_normalised = pandas.json_normalize(fruityvice_responce.json())
streamlit.dataframe(fruityvice_normalised)

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)
