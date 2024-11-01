import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie! ðŸ¥¤")
st.write("Choose the fruits you want in your custom Smoothie")
name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your smoothie will be:", name_on_order)

# Establish session and fetch data
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()

# Display multiselect widget
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe['FRUIT_NAME'])

# Display selected ingredients
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    st.write("You selected:", ingredients_string)
else:
    st.write("No ingredients selected.")

# Submit order button
time_to_insert = st.button('Submit Order')
if time_to_insert:
    if ingredients_list:
        # Correctly format the SQL statement with the correct column names
        my_insert_stmt = f"INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES ('{ingredients_string}', '{name_on_order}')"
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="âœ…")
    else:
        st.error('Please select at least one ingredient.')
