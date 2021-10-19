import numpy as np
import pandas as pd
import streamlit as st
import openpyxl
from src.fun import read_cake, read_fb, identify_adset
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

st.set_page_config(page_title="Cake",
                   page_icon="🎂",
                   layout='wide')

st.header('Cake')

col_order = ['Adset', 'Revenue', 'Cost', 'FB Purchases', 'CPC', 'CTR']

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
                cake_df = df.loc[df['Sub ID 5'].isin([ids])][[group_by, 'Revenue']]. \
                    groupby([group_by]).sum().sort_values('Revenue', ascending=False).reset_index()

                cake_df.rename(columns={cake_df.columns[0]:"Adset"}, inplace=True)

                st.write(cake_df.to_html(index=False), unsafe_allow_html=True)
                           # height = 800
                st.write(' ')
        if fb:
            fb_df = read_fb(fb)
            cake_df[['adset_id', 'age']] = cake_df.apply(identify_adset, axis=1, result_type='expand')

            merged_df = fb_df.merge(cake_df.drop(columns='Adset'),
                                    on=['adset_id', 'age'],
                                    how='left')

            with col2:
                with st.expander('FB data', expanded=False):
                    st.write(fb_df.drop(columns=['adset_id', 'age']).to_html(index=False), unsafe_allow_html=True)
                with st.expander('Detected adsets:', expanded=True):
                    st.write(merged_df.drop(columns=['adset_id', 'age']).dropna(subset=['Revenue'])[col_order].to_html(index=False),
                             unsafe_allow_html=True)
                    st.write(' ')

    else:
        st.write('none selected')
        st.write(df)