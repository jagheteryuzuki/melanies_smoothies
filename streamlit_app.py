# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col  #function to import the columns that you want to import only

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)


name_on_order = st.text_input('Name on Smoothie:')
st.write('The Name on your Smoothie will be:', name_on_order)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

#add a multiselect
ingredients_list = st.multiselect(
    'Choose Up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
)

#to check by taling a closer look at what is contained in our ingredients list
if ingredients_list: # that makes a blank space if the ingredients_list is null
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list: #each fruit_chosen in ingredients_list multiselect box: do everthing below this line that is indented
        ingredients_string += fruit_chosen + ' ' #+= means that add this to what is already in the variable, so each time the FOR loop is repeated
    
    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""


    #st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered!', icon="✅")
