import numpy as np
import pandas as pd
import streamlit as st
import openpyxl
from src.fun import read_cake, read_fb
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

st.set_page_config(page_title="Cake",
                   page_icon="🎂",
                   layout='wide')

st.header('Cake')

files = st.sidebar.file_uploader('Bring your cake'
                         , type=['csv', 'xlsx', 'xls']
                         , accept_multiple_files=True)

#files = pd.read_csv('Conversion_Report_10-10-2021_10-15-2021')

df = pd.DataFrame()

if files:

    df = read_cake(files)

    ids = st.sidebar.selectbox('Select Pixels:', options=np.delete(df['Sub ID 5'].unique(), np.where(df['Sub ID 5'].unique()=='nan')))

    group_by = st.sidebar.radio('Group by',
                                ('Sub ID 3', 'Sub ID 2')
                                 )

    fb = st.sidebar.file_uploader('Bring your FB'
                         , type=['csv'])

    if ids:
        col1, col2 = st.columns([1,2])
        with col1:
            with st.expander('Cake Data (Expand)', expanded=True):
                output_df = df.loc[df['Sub ID 5'].isin([ids])][[group_by, 'Revenue']]. \
                    groupby([group_by]).sum().sort_values('Revenue', ascending=False).reset_index()

                output_df.rename(columns={output_df.columns[0]:"Adset"}, inplace=True)

                st.write(output_df.to_html(index=False), unsafe_allow_html=True)
                           # height = 800
                st.write(' ')
        if fb:
            fb_df = read_fb(fb)
            with col2:
                with st.expander('FB Data', expanded=True):
                    st.write(fb_df.to_html(index=False), unsafe_allow_html=True)

    else:
        st.write('none selected')
        st.write(df)