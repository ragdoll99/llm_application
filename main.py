# Set up and run this Streamlit App
import streamlit as st
from logics.customer_query_handler import process_user_message
from utility import check_password

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

# endregion <--------- Streamlit App Configuration --------->

st.title("Streamlit App")

form = st.form(key="form")
form.subheader("Prompt")

user_prompt = form.text_area("Enter your prompt here", height=200)

if form.form_submit_button("Submit"):
    st.toast("User Input Submitted - {user_prompt}")
    response = process_user_message(user_prompt) #<--- This calls the `process_user_message` function that we have created 🆕
    st.write(response[0])
    response[1]
    print(f"User Input is {user_prompt}")