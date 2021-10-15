import pandas as pd
import streamlit as st


st.header('Cake')

files = st.sidebar.file_uploader('Upload your csv'
                         , type='csv'
                         , accept_multiple_files=True)
df = pd.DataFrame()
if files:
    for f in files:
        temp_df = pd.read_csv(f)
        df = df.append(temp_df)


    st.write(df)