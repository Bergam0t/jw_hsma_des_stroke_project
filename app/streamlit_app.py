"""
Set-up the app (called as `streamlit run app/streamlit_app.py`).
"""

import streamlit as st


pg = st.navigation(
    [
        st.Page("run_model.py", title="Run the Model"),
        st.Page("about.py", title="About")
    ],
    position="top",
)
pg.run()
