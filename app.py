# load libraries 
import time 
import numpy as np 
import pandas as pd 
import streamlit as st
import plotly.express as px 

# read dataset
data = pd.read_excel("data/Final Data.xlsx")

# setup dashboard
st.set_page_config(page_title = "Confusion", page_icon = "🥴", layout = "wide")

# set title
st.title("Confusion: EEG analysis based on student confusion")

# input subject ID
subject_id = st.selectbox("Select Subject ID", pd.unique(data['Subject']))

# filtering data
data_filter = data[data["Subject"] == subject_id]

# define empty state for update element
placeholder = st.empty()


with placeholder.container():

    # metrics visualisation
    kpi1, kpi2, kpi3 = st.columns(3)

    # calculate pct_rate 
    label    = data_filter['Label'].mode().tolist()[0]
    pct_rate = np.round((data_filter[data_filter['Label'] == label].shape[0] / len(data_filter)) * 100, 2)
    label    = "Confuse" if label == 1 else "Not Confuse"

    kpi1.metric(label = "Age ⏳", value = data_filter['age'].mode())
    kpi2.metric(label = "Gender ⚧️", value = "Man 👨🏼" if data_filter['gender'].iloc[0] == 1 else "Woman 👩🏻")
    kpi3.metric(label = "Confusion Rate %", value = f"{label} - {pct_rate}")

    # plot visualisation
    fig_col1, fig_col2, fig_col3 = st.columns(3)

    with fig_col1:
        st.markdown("### Raw EEG Chart")
        fig = px.line(data_filter, x = [i for i in range(len(data_filter))], y = data_filter['Raw'], color = "Label")
        st.write(fig)

    with fig_col2:
        st.markdown("### Delta Chart")
        fig = px.line(data_filter, x = [i for i in range(len(data_filter))], y = data_filter['Delta'], color = "Label")
        st.write(fig)

    with fig_col3:
        st.markdown("### Theta Chart")
        fig = px.line(data_filter, x = [i for i in range(len(data_filter))], y = data_filter['Theta'], color = "Label")
        st.write(fig)
        
    pc1, pc2 = st.columns(2)

    with pc1:
        st.markdown("### Dataset EEG Overview")
        st.dataframe(data_filter, height = 500)

    with pc2:
        st.markdown("### Video Learning Sample")
        path = f"data/video/{subject_id}.m4v"
        st.video(open(path, "rb").read())
