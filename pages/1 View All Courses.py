
import streamlit as st
import json
import pandas as pd

# Open the file in read mode ('r')
with open('./data/courses-full.json', 'r') as file:
    # Read the contents of the file
    json_string = file.read()
    print(json_string)

course_data = json.loads(json_string)

# Convert a list of dictionary into a Pandas DataFrame
df_courses = pd.json_normalize(course_data.values())

df_courses


