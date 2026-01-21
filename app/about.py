"""
About page
"""

import streamlit_mermaid as stmd
import streamlit as st

from app_utils import read_file_contents


# Page configuration
st.set_page_config(layout="wide")

# Load custom CSS
with open("app/resources/style.css", encoding="utf-8") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# Tabs
tab_diagram, tab_pathway, tab_model = st.tabs(
    ["Model Diagram", "About the Stroke Pathway", "About the Model"]
)

# Tab 1: Model diagram
with tab_diagram:
    stmd.st_mermaid(read_file_contents("docs/diagrams/pathway_diagram.mmd"))

# Tab 2: Pathway information
with tab_pathway:
    st.header("Key Stroke Pathway Information")

    st.subheader(
        "What is the difference between CT scanning and CT perfusion scanning?"
    )

    st.write(
        """
CT perfusion (CTP) scanning is an advanced technique that allows stroke
clinicians to identify areas of brain tissue that is irreversibly injured and
that which has the potential for salvage if treated promptly with thrombolysis
(clot-busting drugs) or thrombectomy (mechanical clot removal).

CTP scanning is particularly useful in cases of unknown stroke onset, which is
more common at night or in the early hours of the morning when patients display
stroke symptoms on waking. CTP scans allow clinicians to make their decisions
based on the salvageable brain tissue rather than purely on a standard time
based criteria. This potentially leads to much improved outcomes for
individuals, reducing the level of disability they experience after their
stroke. It can also extend the window for thrombectomy and thrombolysis even
when the onset time is known.

Overall, the use of CTP scanning can improve outcomes and lead to shortened
stays for a range of patients. However, CTP scanning is not always available as
it requires additional software, a modern scanner with a high number of slices,
and people trained in the interpretation of the scans. It also results in a
higher dose of radiation being applied to patients, so its usage needs to be
considered carefully.
        """
    )

    st.subheader("What is the modified Rankin scale (mRS)?")
    st.write("Coming Soon!")

    st.subheader(
        """
        Why can't thrombolysed patients be considered for admission avoidance?
        """
    )
    st.write("Coming Soon!")

# Tab 3: Model information
with tab_model:
    st.header("Where can I find technical details about the model?")
    st.write("Coming Soon!")
    # TODO: Link to the documentation and STRESS guidance within documentation

    st.header("Can I adapt and use the model with my own trust?")
    st.write("Coming Soon!")
