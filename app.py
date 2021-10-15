import pandas as pd
import streamlit as st
import openpyxl

st.set_page_config(page_title="Cake",
                   page_icon="🎂",
                   layout='wide')

st.header('Cake')

files = st.sidebar.file_uploader('Upload your csv'
                         , type=['csv', 'xlsx', 'xls']
                         , accept_multiple_files=True)
df = pd.DataFrame()
if files:
    for f in files:
        if 'csv' in f.name[-4:]:
            temp_df = pd.read_csv(f, error_bad_lines=False, sep=';')
        else:
            temp_df = pd.read_excel(f, engine='openpyxl', sheet_name=0)
        df = df.append(temp_df)

    #st.write(f'{f.name[:-4]}')
    df['Sub ID 3'] = df['Sub ID 3'].str.replace('",void 0', '')
    df['Sub ID 5'] = df['Sub ID 5'].astype(str)
    df['Price']    = df['Price'].replace('\$|,', '', regex=True).astype(float)

    ids = st.sidebar.multiselect('Select:', options=df['Sub ID 5'].unique())

    if ids:
        #st.write(ids)
        st.write(df.loc[df['Sub ID 5'].isin(ids)][['Sub ID 3', 'Price']].\
                    groupby(['Sub ID 3']).sum().sort_values('Price', ascending=False))
    else:
        st.write('none selected')
        st.write(df)