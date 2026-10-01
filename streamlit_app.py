# Import python packages
import streamlit as st
import requests
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
session.sql("USE WAREHOUSE COMPUTE_WH").collect()

# Get fruit options
# Get fruit options - now include SEARCH_ON column
my_dataframe = session.table("smoothies.public.fruit_options") \
    .select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Multi-select ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe.select(col('FRUIT_NAME')),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # Get the SEARCH_ON value for this fruit
        search_on_value = session.table("smoothies.public.fruit_options") \
            .filter(col('FRUIT_NAME') == fruit_chosen) \
            .select(col('SEARCH_ON')) \
            .collect()[0]['SEARCH_ON']

        # Use SEARCH_ON in the API call
        smoothiefroot_response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on_value}"
        )
        st.subheader(f"{fruit_chosen} Nutrition Info:")
        st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )

    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                        VALUES ('{ingredients_string.strip()}', '{name_on_order}')"""

    if st.button('Submit Order'):
        try:
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
        except Exception as e:
            st.error(f"Error details: {e}")
    
