# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """ Choose the fruits you want in your Custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=6
    )

if ingredients_list: 
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

   

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
                     values (?, ?)"""

    if st.button('Submit Order'):
       session.sql(my_insert_stmt, params=[ingredients_string, name_on_order]).collect()
       st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")


    
    
