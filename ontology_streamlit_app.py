import streamlit as st
from rdflib import Graph

st.set_page_config(page_title="Cloud Ontology Search", layout="centered")

# Load ontology
g = Graph()
g.parse("mock_cloud_storage_rdfxml.owl", format="xml")

# UI layout
st.title("🔍 Cloud Ontology Search")
st.write("Search concepts, classes, and instances in your OWL ontology.")

query = st.text_input("Enter a keyword (e.g. 's3', 'encryption')")

if query:
    sparql_query = f"""
    SELECT ?s WHERE {{
        ?s ?p ?o .
        FILTER(CONTAINS(LCASE(STR(?s)), "{query.lower()}"))
    }}
    """
    results = g.query(sparql_query)
    st.markdown("### Search Results")
    hits = [str(row.s) for row in results]
    if hits:
        for item in hits:
            st.write(f"- {item}")
    else:
        st.info("No matching results found.")
