import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Mom's Healthy Diner")
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("let's pick some fruits : ",list(my_fruit_list.index),['Cherries','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


def get_fruityvice_data(this_fruit_choice):
  fruityvice_responce = requests.get('https://fruityvice.com/api/fruit/'+ fruit_choice)
  fruityvice_normalised = pandas.json_normalize(fruityvice_responce.json())
  return fruityvice_normalised

streamlit.title("Fruityvice Fruit Advice !")

try:
  fruit_choice = streamlit.text_input('What kind of fruit would you like info about ?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get the information')
  else:
    fruityvice_normalised_from_func = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalised_from_func)
    
except URLError as e:
  streamlit.error()


streamlit.header("The fruit load list contains :")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return  my_cur.fetchall()
  
if streamlit.button('Get fruit load list !'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)



def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +"')")
    return "Thanks for addding " + new_fruit
  
add_my_fruit = streamlit.text_input('What would you like to add ?' , 'Jackfruit')
if streamlit.button('Add a fruit to the list!'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_func = insert_row_snowflake(add_my_fruit)
  my_cnx.close()
  streamlit.text(back_from_func)

streamlit.stop()
