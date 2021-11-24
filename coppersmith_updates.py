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

# @st.cache(ttl=300)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')


# Functions
def list_categories():
    search_list = []
    for row in rows:
        if row.Category in search_list:
            continue
        else:
            search_list.append(row.Category)
    return search_list

def list_suppliers():
    search_list = []
    for row in rows:
        if row.Supplier in search_list:
            continue
        else:
            search_list.append(row.Supplier)
    return search_list

def list_departments():
    search_list = []
    for row in rows:
        if row.Department in search_list:
            continue
        else:
            search_list.append(row.Department)
    return search_list


categories = list_categories()
suppliers = list_suppliers()
departments = list_departments()


# App
st.header("CopperSmith")

st.subheader("Latest Updates")

# Print results.
for row in rows:
    st.write(row.Update)

# Side bar
st.sidebar.subheader("Sorting Options")

# date_options = st.sidebar.selectbox('Date', ('11/23/2021', '11/24/2021'))
category_options = st.sidebar.selectbox('Category', (categories))
supplier_options = st.sidebar.selectbox('Supplier', (suppliers))
department_options = st.sidebar.selectbox('Department', (departments))

