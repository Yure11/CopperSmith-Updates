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

# Layout Templates
update_temp = """
<div style="background-color:#b87333;padding:10px;border-radius:10px;margin:10px;">
<h5 style="color:white;text-align:center;">{} for {}</h5>
<h6 style="color:white;">Change applies to: {} Department(s) and {} supplier(s)</h6>
<h6 style="color:white;">Exceptions: {}</h6>
<h6 style="color:white;">Approved on {} by {} </h6>
</div>
"""


# Functions
def list_categories():
    search_list = []
    for row in rows:
        if row.Category in search_list:
            continue
        else:
            search_list.append(row.Category)
    search_list.append(" None")
    search_list.sort()
    return search_list

def list_suppliers():
    search_list = []
    for row in rows:
        if row.Supplier in search_list:
            continue
        else:
            search_list.append(row.Supplier)
    search_list.append(" None")
    search_list.sort()
    return search_list

def list_departments():
    search_list = []
    for row in rows:
        if row.Department in search_list:
            continue
        else:
            search_list.append(row.Department)
    search_list.append(" None")
    search_list.sort()
    return search_list


categories = list_categories()
suppliers = list_suppliers()
departments = list_departments()


# App
st.header("CopperSmith")

st.subheader("Latest Updates")

# Print results
for row in rows:
    st.markdown(update_temp.format(row.Update, row.Category, row.Department, row.Supplier, row.Exceptions, row.Date, row.Approved_By), unsafe_allow_html=True)


# Sidebar
st.sidebar.subheader("Sorting Options")

# date_options = st.sidebar.selectbox('Date', ('11/23/2021', '11/24/2021'))
category_options = st.sidebar.selectbox('Category', (categories), index=0)
supplier_options = st.sidebar.selectbox('Supplier', (suppliers))
department_options = st.sidebar.selectbox('Department', (departments))

