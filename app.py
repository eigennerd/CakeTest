import pandas as pd
import streamlit as st
import openpyxl

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

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
            temp_df = pd.read_csv(f, error_bad_lines=False, sep=',')
        else:
            temp_df = pd.read_excel(f, engine='openpyxl', sheet_name=0)
        df = df.append(temp_df)


    #st.write(df)
    #st.write(f'{f.name[:-4]}')
    df['Sub ID 3'] = df['Sub ID 3'].str.replace('",void 0', '')
    df['Sub ID 5'] = df['Sub ID 5'].astype(str)
    df['Price']    = df['Price'].replace('\$|,', '', regex=True).astype(float)

    ids = st.sidebar.multiselect('Select:', options=df['Sub ID 5'].unique())

    group_by = st.sidebar.radio('Group by',
                                ('Sub ID 3', 'Sub ID 2')
                                 )

    if ids:
        #st.write(ids)

        output_df = df.loc[df['Sub ID 5'].isin(ids)][['Sub ID 3', 'Sub ID 2', 'Price']].\
                    groupby([group_by]).sum().sort_values('Price', ascending=False).reset_index()

        st.dataframe(output_df,
                    height = 800)

        # copy_button = Button(label="Copy to Clipboard")
        #
        # copy_button.js_on_event("button_click", CustomJS(args=dict(df=output_df.to_csv(sep='\t')), code="""
        #     navigator.clipboard.writeText(df);
        #     """))
        #
        # no_event = streamlit_bokeh_events(
        #     copy_button,
        #     events="GET_TEXT",
        #     key="get_text",
        #     refresh_on_update=True,
        #     override_height=75,
        #     debounce_time=0)

    else:
        st.write('none selected')
        st.write(df)