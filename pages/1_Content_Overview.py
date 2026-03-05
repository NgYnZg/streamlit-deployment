import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Content Overview")

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    return df

df = load_data()

# UI Components
content_type = st.selectbox("Select Content Type", df["type"].unique())
year_range = st.slider(
    "Select Release Year Range",
    int(df["release_year"].min()),
    int(df["release_year"].max()),
    (2010, 2020)
)

filtered_df = df[
    (df["type"] == content_type) &
    (df["release_year"].between(year_range[0], year_range[1]))
]

st.write("Filtered Data:", filtered_df.shape[0], "records")

tab1, tab2 = st.tabs(["Distribution", "Yearly Trend"])

# ---- TAB 1 ----
with tab1:
    fig1 = px.histogram(
        filtered_df,
        x="release_year",
        nbins=20,
        title="Distribution of Release Years"
    )
    st.plotly_chart(fig1, use_container_width=True)

# ---- TAB 2 ----
with tab2:
    yearly = filtered_df.groupby("year_added").size().reset_index(name="count")
    fig2 = px.line(
        yearly,
        x="year_added",
        y="count",
        title="Content Added Over Time"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Download button
st.download_button(
    "Download Filtered Data",
    filtered_df.to_csv(index=False),
    file_name="filtered_netflix_data.csv",
    mime="text/csv"
)