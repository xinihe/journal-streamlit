import streamlit as st
import pandas as pd
import re

import altair as alt
from urllib.error import URLError

#st.set_page_config(page_title="DataFrame Demo", page_icon="📊")

st.markdown("## AJG (ABS) 2021 Rating")
#st.sidebar.header("ABS List Search")
st.write(
    """
You might use this app to look up the AJG rankings for a specific journal. (The lastest metrics is accessable through the [website](https://charteredabs.org/academic-journal-guide-2021/).)
If you would want to conduct a search for `finance` or `accounting`, please enter `finance|accounting`.
"""
)

# Cache the dataframe so it's only loaded once
@st.cache
def get_data():
    df = pd.read_csv('abs2021.csv')
    return df

df = get_data()
kyword = st.text_input('Please provide the journal title\'s keyword(s):', 'Finance')

abs = df[df['JournalTitle'].str.contains(kyword, na=False, flags=re.IGNORECASE, regex=True)]


abs = abs[['AJG2021','JournalTitle','Field','ISSN']]
if len(abs) == 0:
    st.write(""" There is no result based on your keywords. Please make sure to separate the keywords by `|` (i.e. Accounting|Finance)
     """)
else:
    st.write('There are `{}` journals match your search.'.format(str(len(abs))))
    st.dataframe(abs.sort_values(by=['AJG2021'],ascending=False), use_container_width=True)
    st.write('The table is interactive. You can resize tables by dragging and dropping the bottom right corner of tables. Please [let me know](mailto:nihe78@gmail.com) if you experience any difficulty.')
