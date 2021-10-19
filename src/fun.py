import streamlit as st
import pandas as pd

@st.cache()
def read_cake(files):
    df = pd.DataFrame()
    for f in files:
        if 'csv' in f.name[-4:]:
            temp_df = pd.read_csv(f, error_bad_lines=False, sep=',')
        else:
            temp_df = pd.read_excel(f, engine='openpyxl', sheet_name=0)
        df = df.append(temp_df)

        # st.write(df)
        # st.write(f'{f.name[:-4]}')
    df['Sub ID 2'] = df['Sub ID 2'].str.replace(' ', '')
    df['Sub ID 3'] = df['Sub ID 3'].str.replace('",void 0', '').replace(' ', '')
    df['Sub ID 5'] = df['Sub ID 5'].astype(str).replace(' ', '')
    df['Price'] = df['Price'].replace('\$|,', '', regex=True).astype(float)

    df = df.rename(columns={'Price':'Revenue'})

    return df



def read_fb(file):
    output = pd.read_csv(file)

    if 'Ad set name' in output.columns.values:
        #st.write(output.columns.values)
        output = output[['Ad set name',
                         'Results',
                         'Amount spent (USD)',
                         'CPC (cost per link click)',
                         'CTR (link click-through rate)']]\
            .rename(
                columns={
                    'Ad set name':'Adset',
                    'Results': 'FB Purchase',
                    'Amount spent (USD)':'Cost',
                    'CPC (cost per link click)':'CPC',
                    'CTR (link click-through rate)':'CTR'
                }
            )

        output['Adset'] = output['Adset'].str.replace(' ','')

        return output.dropna()

    else:
        st.sidebar.error('Wrong FB file')
        return pd.DataFrame()