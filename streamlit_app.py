import streamlit as st
import pandas as pd
from datetime import datetime
import time
from rdflib import Graph

# ---------- Setup ----------
st.set_page_config(page_title="Cloud Storage Ontology Experiment", layout="centered")

# Ontology
g = Graph()
g.parse("formal_cloud_storage.owl")  # <-- Use your real OWL file name

# Session State for timing and logs
if 'search_start_time' not in st.session_state:
    st.session_state['search_start_time'] = None
if 'log' not in st.session_state:
    st.session_state['log'] = []

def log_action(action, query=None, results=None, time_taken=None):
    st.session_state['log'].append({
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'query': query,
        'results': results,
        'time_taken': time_taken
    })

# ---------- UI ----------
st.title("Cloud Storage Interoperability Experiment")
st.info(
    """
    Welcome! Please follow the instructions below:
    1. Use the search bar to look up cloud storage features or providers.
    2. Try at least 3 different searches (e.g. "encryption", "archive", "OpenStack").
    3. After searching, complete the feedback survey at the bottom.
    4. If you're done, you can download your activity log.
    """
)

# ---------- Search ----------
st.header("1. Search Cloud Storage Ontology")
query = st.text_input("Enter your search term (e.g., 'encryption', 'archive', 'OpenStack'):")

# Set start time when user begins typing
if query and st.session_state['search_start_time'] is None:
    st.session_state['search_start_time'] = time.time()

if st.button("Search"):
    # Run ontology query (simple example: match by substring in service name)
    sparql = f"""
        SELECT ?service WHERE {{
            ?service rdf:type <http://example.org/cloud#ObjectStorage> .
            FILTER(CONTAINS(LCASE(STR(?service)), "{query.lower()}"))
        }}
    """
    qres = g.query(sparql)
    results = [str(row.service).split("#")[-1] for row in qres]
    
    # Calculate time taken
    time_taken = None
    if st.session_state['search_start_time'] is not None:
        time_taken = round(time.time() - st.session_state['search_start_time'], 2)
    
    st.write("**Results:**", results if results else "No results found.")
    log_action("search", query=query, results=", ".join(results), time_taken=time_taken)
    st.session_state['search_start_time'] = None  # Reset

# ---------- Feedback Survey ----------
st.header("2. Feedback Survey")
with st.form("survey_form"):
    ease = st.slider("How easy was it to find a storage service?", 1, 5, 3)
    both_found = st.radio("Did the results include both AWS and OpenStack options?", ["Yes", "No"])
    missing = st.text_input("Was any important storage provider missing?")
    satisfaction = st.slider("Overall satisfaction with this system?", 1, 5, 3)
    comments = st.text_area("Any suggestions to improve the tool or ontology?")
    submitted = st.form_submit_button("Submit Survey")
    if submitted:
        log_action(
            "survey",
            query=None,
            results=f"ease:{ease}, both_found:{both_found}, missing:{missing}, satisfaction:{satisfaction}, comments:{comments}",
            time_taken=None
        )
        st.success("Thank you! Your feedback has been recorded.")

# ---------- Researcher Log Download with Password ----------
with st.expander("For Researchers Only"):
    password = st.text_input("Enter researcher password to access the activity log:", type="password")
    if password == "babe123":  # Change this!
        st.success("Access granted.")
        if st.button("Download Activity Log"):
            df_log = pd.DataFrame(st.session_state['log'])
            df_log.to_csv("user_activity_log.csv", index=False)
            st.success("Log saved as user_activity_log.csv")
            st.dataframe(df_log)
    elif password != "":
        st.error("Incorrect password. Please try again.")
