import streamlit as st
from rdflib import Graph

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
