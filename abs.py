import streamlit as st
import pandas as pd
import re

import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="Journal Search Demo", layout="wide")

st.markdown("## Journal Rating")

st.write(
    """
You might use this app to look up the AJG/ZJGSU/ABDC rankings for a specific journal. (The lastest metrics is accessable through the [website](https://charteredabs.org/academic-journal-guide-2021/).)
If you would want to conduct a search for `finance` or `accounting`, please enter `finance|accounting`.
"""
)

# Cache the dataframe so it's only loaded once
#@st.cache
# def get_data():
#     df = pd.read_csv('abs2021.csv')
#     df_abdc = pd.read_csv('ABDC-finance_A copy.csv')
#     df_zjgsu = pd.read_excel('zjgsu_journal_rank_en.xlsx', index_col=0)
#     return df, df_abdc, df_zjgsu

# df, df_abdc, df_zjgsu = get_data()

df = pd.read_csv('abs2021.csv')
df_abdc = pd.read_csv('ABDC-finance_A copy.csv')
df_zjgsu = pd.read_csv('zjgsu_journal_rank_en.csv', index_col=0)

df_abdc['ABDC2022'] = df_abdc['Rating']
df_zjgsu['ZJGSU2022'] = df_zjgsu['rank']
st.sidebar.header("Journal Search")

# st.sidebar.subheader('List search')

# rank = st.sidebar.select_slider(
#     'Select a rank of the AJG score',
#     options=['4*', '4', '3', '2', '1'])

# field = st.sidebar.multiselect('Please choose your interested field', df['Field'].unique().tolist() , ['FINANCE'])

#st.sidebar.subheader('Journal name or keywords search (通过期刊名称或者名称的关键词搜索)')

st.sidebar.markdown("\n")
kyword = st.sidebar.text_input('Please provide the journal title or it\'s keyword(s): (键入关键词后回车)', 'Journal of Finance')

options = st.sidebar.multiselect('We have data released in 2021 and 2020:',
    ['AJG2021','ABDC2022','ZJGSU2022'],
    ['AJG2021','ABDC2022','ZJGSU2022'])

if 'ZJGSU2022' in options:
    zjgsu = df_zjgsu[df_zjgsu['title'].str.contains(kyword, na=False, flags=re.IGNORECASE, regex=True)]
    zjgsu = zjgsu[['title','ZJGSU2022','area','type']].reset_index(drop=True)
    if len(zjgsu) == 0:
        st.write(""" There is no result in the ZJGSU list based on your keywords. Please make sure to separate the keywords by `|` (i.e. Accounting|Finance)
     """)
    else:
        st.write('There are `{}` ZJGSU(2022) ranked journals match your search.'.format(str(len(zjgsu))))
        st.dataframe(zjgsu.sort_values(by=['ZJGSU2022'],ascending=False), use_container_width=True)

if 'AJG2021' in options:
    abs = df[df['JournalTitle'].str.contains(kyword, na=False, flags=re.IGNORECASE, regex=True)]
    abs = abs[['JournalTitle','AJG2021','Field','ISSN']].reset_index(drop=True)
    if len(abs) == 0:
        st.write(""" There is no result in the ABS list based on your keywords. Please make sure to separate the keywords by `|` (i.e. Accounting|Finance)
     """)
    else:
        st.write('There are `{}` ABS ranked journals match your search.'.format(str(len(abs))))
        st.dataframe(abs.sort_values(by=['AJG2021'],ascending=False), use_container_width=True)

if 'ABDC2022' in options:
    abdc = df_abdc[df_abdc['Title'].str.contains(kyword, na=False, flags=re.IGNORECASE, regex=True)]
    abdc = abdc[['Title','ABDC2022','Field of Research','ISSN']].reset_index(drop=True)
    if len(abdc) == 0:
        st.write(""" There is no result in the ABDC list based on your keywords. Please make sure to separate the keywords by `|` (i.e. Accounting|Finance)
     """)
    else:
        st.write('There are `{}` ABDC ranked journals match your search.'.format(str(len(abdc))))
        st.dataframe(abdc.sort_values(by=['ABDC2022'],ascending=True), use_container_width=True)


st.write('The table is interactive. You can resize tables by dragging and dropping the bottom right corner of tables. Please [let me know](mailto:nihe78@gmail.com) if you experience any difficulty.')
