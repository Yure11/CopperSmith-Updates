#Use strlit env to run this program

## Modules
import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect

# Create a Google Authentication connection object
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn =connect(credentials=credentials)

@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
for row in rows:
    st.write(row)