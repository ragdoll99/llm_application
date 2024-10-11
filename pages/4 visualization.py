import streamlit as st 
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import os
# from matplotlib.backends.backend_agg import RendererAgg
import numpy as np
# import plotly.express as px

#Loading the data
@st.cache_data
#  read csv
path ='./data'
extension = '.csv'

files = [file for file in os.listdire(path) if file.endswith(extension)]
dfs_raw = []
for file in files:
   df_raw = pd.read_csv(os.path.join(path, file), low_memory=False)
   dfs_raw.append()

# combine raw table
df_hdb_resale = pd.concat(dfs_raw, ignore_index=True)

# def get_data_hdb_resale():
#      return pd.read_csv("./data/hdb_resale_full_with_mall_hawker.csv")

#configuration of the page
st.set_page_config(layout="wide")
#load dataframes
# df_hdb_resale = get_data_hdb_resale()

st.title('HDB Resale transaction explorer')
st.markdown("""
This app performs visualization from the open data from the SG HDB Resale transaction
""")
st.write(df_hdb_resale)

# create selection
st.sidebar.header('Select what to display')
pol_parties = df_hdb_resale['town'].unique().tolist()
pol_party_selected = st.sidebar.multiselect('Town', pol_parties, pol_parties)
nb_deputies = df_hdb_resale['year']
nb_mbrs = st.sidebar.slider("Number of members", int(nb_deputies.min()), int(nb_deputies.max()), (int(nb_deputies.min()), int(nb_deputies.max())), 1)

# creates masks from the sidebar selection widgets
mask_pol_par = df_hdb_resale['town'].isin(pol_party_selected)

# creates masks for years slicer
mask_mbrs = df_hdb_resale['year'].between(nb_mbrs[0], nb_mbrs[1])

# apply mask to the data
df_hdb_resale_filtered = df_hdb_resale[mask_pol_par & mask_mbrs]
st.write(df_hdb_resale_filtered)

# Create a Bar chart
df_count = (
    df_hdb_resale_filtered.groupby("year")
    .count()
    .reset_index()
    .rename(columns={"town": "Count"})
)
st.bar_chart(df_count, x = "year", y="Count")

# Create a Scatter Chart
st.scatter_chart(
    df_hdb_resale_filtered,
    x="floor_area_sqm",
    y="resale_price",
    color="flat_type",
)


## not working
# matplotlib.use("agg")
# _lock = RendererAgg.lock

# # setting color
# pol_par = df_hdb_resale_filtered['town'].value_counts()
# #merge the two dataframe to get a column with the color
# df = pd.merge(pd.DataFrame(pol_par), df_hdb_resale, left_index=True, right_on='abreviated_name')
# colors = df['color'].tolist()

# # chart
# row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.beta_columns((0.2, 1, .2, 1, .2))
# with row0_1, _lock:
#     st.header("HDB")
#     fig, ax = plt.subplots(figsize=(5, 5))
#     ax.pie(pol_par, labels=(pol_par.index + ' (' + pol_par.map(str)
#     + ')'), wedgeprops = { 'linewidth' : 7, 'edgecolor' : 'white'
#     }, colors=colors)
#     #display a white circle in the middle of the pie chart
#     p = plt.gcf()
#     p.gca().add_artist(plt.Circle( (0,0), 0.7, color='white'))
#     st.pyplot(fig)