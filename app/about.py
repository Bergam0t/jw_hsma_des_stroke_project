import streamlit_mermaid as stmd
import streamlit as st

st.set_page_config(layout="wide")


with open("app/resources/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(
    ["Model Diagram", "About the Stroke Pathway", "About the Model"]
)

with tab1:
    diagram = """
flowchart TB
    A["In-hours admissions"] --> n12["Patient Generated"]
    B["Nurse Triage"] --> C(["Is the CTP perfusion scanner open?"])
    C -- Yes --> n2["CTP Scan <br>(Advanced Scan)"]
    C -- No --> n3["CT Scan"]
    n2 --> n4(["Patient has Ischaemic Stroke <br>AND rankin score on presentation is 1 or above"]) & n18(["Patient has other kind of stroke or no stroke<br>OR Rankin score is 0<br>OR Onset time not known or CTP scan not available"])
    n3 --> n5(["Patient has Ischaemic Stroke<br>AND rankin score on presentation is 1 or above <br><b>AND onset time is known</b>"]) & n18
    n6(["Is SDEC open?"]) -- Yes --> n7(["Is a bed available in SDEC?"])
    n7 -- Yes --> n8["Admit to SDEC"]
    n7 -- No --> n9["Admit to Ward"]
    n6 -- No --> n9
    n9 --> n11["Discharge"]
    n8 --> n9
    n8 -- If goes directly from SDEC to discharge, </br>considered an 'avoided admission' --> n11
    n1["Out-of-hours admissions (less frequent)"] --> n12
    n12 --> B
    n12 -.- n13["<b>Mean Rankin Score on Presentation <br></b><br>0 least disabled<br>5 most disabled"] & n14["<b>Stroke Onset Type<br></b><br>Known<br>OR Unknown but in CT window<br>OR unknown and outside CT window"]
    n15["<b>Patient Diagnosis<br></b><br>Intracerebral Haemorrhage<br>OR Ischaemic Strke<br>OR Transient Ischaemic Attach<br>OR Stroke Mimic<br>OR Non-Stroke"] -.- n12
    n16["Triage Priority <br><br>Not currently used"] -.- n12
    n4 --> n17["Thrombolyse<br><br>Reduces LOS by a defined factor"]
    n5 --> n17
    n17 --> n6
    n18 --> n6

    style C fill:#FFF9C4
    style n4 fill:#FFF9C4
    style n18 fill:#FFF9C4
    style n5 fill:#FFF9C4
    style n6 fill:#FFF9C4
    style n7 fill:#FFF9C4
    style n13 fill:#C8E6C9
    style n14 fill:#C8E6C9
    style n15 fill:#C8E6C9
    style n16 fill:#C8E6C9
    """

    stmd.st_mermaid(diagram)

with tab2:
    st.header("Key Stroke Pathway Information")

    st.subheader(
        "What is the difference between CT scanning and CT perfusion scanning?"
    )

    st.write("""
CT perfusion (CTP) scanning is an advanced technique that allows stroke clinicians to identify areas of brain tissue that is irreversibly injured and
that which has the potential for salvage if treated promptly with thrombolysis (clot-busting drugs) or thrombectomy (mechanical clot removal).

CTP scanning is particularly useful in cases of unknown stroke onset, which is more common at night or in the early hours of the morning when patients display stroke symptoms on waking.
CTP scans allow clinicians to make their decisions based on the salvageable brain tissue rather than purely on a standard time based criteria.
This potentially leads to much improved outcomes for individuals, reducing the level of disability they experience after their stroke.
It can also extend the window for thrombectomy and thrombolysis even when the onset time is known.

Overall, the use of CTP scanning can improve outcomes and lead to shortened stays for a range of patients.
However, CTP scanning is not always available as it requires additional software, a modern scanner with a high number of slices, and people trained in the interpretation of the scans.
It also results in a higher dose of radition being applied to patients, so its usage needs to be considered carefully.

""")

    st.subheader("What is the modified Rankin scale (mRS)?")
