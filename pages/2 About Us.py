# draw a line chart
""" Draw a line chart"""
import streamlit as st
import numpy as np
import pandas as pd

st.title(":blue[About this page]")
st.markdown("This is a Streamlit App that demonstrates how to use the OpenAI API to generate text completions.")

container = st.container(border=True)

container.write(
    """
    How to use this App \n
    1. Enter your prompt in the text area. \n
    2. Click the 'Submit' button. \n
    3. The app will generate a text completion based on your prompt.
                
    """)