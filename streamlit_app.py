import streamlit as st
from rdflib import Graph
import pandas as pd
from datetime import datetime

# Load ontology
g = Graph()
g.parse("formal_cloud_storage.owl")

# UI
st.title("Cloud Storage Ontology Explorer")
query_option = st.selectbox("Choose a query to run:", [
    "List all Object Storage services",
    "List services that support Encryption",
    "List services that support Archive tier",
    "List features of AWS S3",
    "List tiers of OpenStack Swift"
])

# Queries
queries = {
    "List all Object Storage services": """
        SELECT ?service WHERE {
            ?service rdf:type <http://example.org/cloud#ObjectStorage> .
        }
    """,
    "List services that support Encryption": """
        SELECT ?service WHERE {
            ?service <http://example.org/cloud#hasFeature> <http://example.org/cloud#Encryption> .
        }
    """,
    "List services that support Archive tier": """
        SELECT ?service WHERE {
            ?service <http://example.org/cloud#hasTier> <http://example.org/cloud#Archive> .
        }
    """,
    "List features of AWS S3": """
        SELECT ?feature WHERE {
            <http://example.org/cloud#AWS_S3> <http://example.org/cloud#hasFeature> ?feature .
        }
    """,
    "List tiers of OpenStack Swift": """
        SELECT ?tier WHERE {
            <http://example.org/cloud#OpenStack_Swift> <http://example.org/cloud#hasTier> ?tier .
        }
    """
}

# Run the selected query
st.subheader("Results")
qres = g.query(queries[query_option])
for row in qres:
    st.write(str(row[0]))

# Logging setup
if 'log' not in st.session_state:
    st.session_state['log'] = []

def log_action(action, query=None, results=None):
    st.session_state['log'].append({
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'query': query,
        'results': results
    })

# Main UI
st.title("Ontology-Backed Cloud Storage Explorer")
query = st.text_input("Enter your search term:")
if st.button("Search"):
    # Replace below with your real SPARQL call/result
    result_list = ["AWS S3", "OpenStack Swift"] if "storage" in query else []
    log_action("search", query=query, results=", ".join(result_list))
    st.write(result_list)

# User Feedback Survey (in-app option)
with st.form("survey"):
    st.header("Quick Feedback Survey")
    ease = st.slider("How easy was it to find a storage service?", 1, 5)
    satisfaction = st.slider("Overall satisfaction with the tool?", 1, 5)
    comments = st.text_area("Any suggestions or comments?")
    submitted = st.form_submit_button("Submit Survey")
    if submitted:
        log_action("survey", query=None, results=f"ease:{ease}, satisfaction:{satisfaction}, comments:{comments}")
        st.success("Thank you for your feedback!")

if st.button("Download Activity Log"):
    df_log = pd.DataFrame(st.session_state['log'])
    df_log.to_csv("user_activity_log.csv", index=False)
    st.success("Log saved as user_activity_log.csv")
    st.dataframe(df_log)

