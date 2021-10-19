import streamlit as st
import pandas as pd
import numpy as np

def identify_adset(row):
    adset_id = ''
    age = ''

    adset_values = row[[0]].str.split('|')

    for v in adset_values['Adset']:
        #print(v)
        if 'ad' in v[0:2]:
            #print(f'ad: {v}')
            adset_id = v
        elif v[0].isdigit():
            #print(f'age: {v}')
            age = v

    age = '26-65' if age=='' else age

    return adset_id, age

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
    df['Sub ID 2'] = df['Sub ID 2'].str.replace(' ', '').str.rstrip('|')
    df['Sub ID 3'] = df['Sub ID 3'].str.replace('",void 0', '').replace(' ', '').str.rstrip('|')
    df['Sub ID 5'] = df['Sub ID 5'].astype(str).replace(' ', '')
    df['Price'] = df['Price'].replace('\$|,', '', regex=True).astype(float)

    df = df.rename(columns={'Price':'Revenue'})

    return df


#@st.cache()
def read_fb(file):

    output = pd.read_csv(file)
    adset_id = pd.DataFrame()

    if 'Ad name' in output.columns.values:
        output = output.rename(columns={'Ad name': 'Ad set name'})

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
                    'Results': 'FB Purchases',
                    'Amount spent (USD)':'Cost',
                    'CPC (cost per link click)':'CPC',
                    'CTR (link click-through rate)':'CTR'
                }
            )

        output['Adset'] = output['Adset'].str.replace(' ','').str.rstrip('|')

        output = output.dropna(subset=['Cost', 'FB Purchases'])

        if output.shape[0]==0:
            st.warning('No Results or Costs in the file')
            output = output.append(pd.DataFrame(columns=['adset_id', 'age']))
        else:
            output[['adset_id', 'age']] = output.apply(identify_adset, axis=1, result_type='expand')

        return output

    else:
        st.sidebar.error('Wrong FB file')
        return pd.DataFrame(columns=[
                                'Adset',
                                'FB Purchases',
                                'Cost',
                                'CPC',
                                'CTR',
                                'adset_id',
                                'age'
                                ])