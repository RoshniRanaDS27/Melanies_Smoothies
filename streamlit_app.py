# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your Custom Smoothie!")

# Get customer name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Multi-select ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# if ingredients_list:
#     ingredients_string = ''
    
#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen + ' '

#     my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order)
#                         VALUES ('{ingredients_string.strip()}', '{name_on_order}')"""

#   #  Uncomment to debug - shows the exact SQL being run
#     st.write(my_insert_stmt)

#     if st.button('Submit Order'):
#         session.sql(my_insert_stmt).collect()
#         st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                        VALUES ('{ingredients_string.strip()}', '{name_on_order}')"""

    st.write("SQL Statement:")
    st.code(my_insert_stmt)

# import requests  
# smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
# st.text(smoothiefroot_response.jason())
# sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    if st.button('Submit Order'):
        try:
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
        except Exception as e:
            st.error(f"Error details: {e}")

import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response.jason())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
