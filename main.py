import streamlit as st

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

st.title("🎬 Netflix Data Dashboard")
st.markdown("""
This dashboard analyzes the Netflix Movies & TV Shows dataset from Kaggle.

### Features:
- Interactive charts
- Multiple pages
- Filters and controls
- Downloadable reports
""")

st.info("Use the sidebar to navigate between all pages.")