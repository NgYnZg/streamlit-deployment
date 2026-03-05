import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🎭 Genre Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    return df

df = load_data()

# Split genres
df['listed_in'] = df['listed_in'].str.split(',')
df_exploded = df.explode('listed_in')
df_exploded['listed_in'] = df_exploded['listed_in'].str.strip()

# UI Components
selected_genres = st.multiselect(
    "Select Genres",
    df_exploded['listed_in'].unique(),
    default=df_exploded['listed_in'].unique()[:5]
)

filtered = df_exploded[df_exploded['listed_in'].isin(selected_genres)]

tab1, tab2 = st.tabs(["Genre Count", "Genre by Type"])

# ---- TAB 1 ----
with tab1:
    genre_count = filtered['listed_in'].value_counts().reset_index()
    genre_count.columns = ['Genre', 'Count']

    fig = px.bar(
        genre_count,
        x='Genre',
        y='Count',
        title="Number of Titles per Genre"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---- TAB 2 ----
with tab2:
    cross = pd.crosstab(filtered['listed_in'], filtered['type']).reset_index()
    fig2 = px.bar(
        cross,
        x="listed_in",
        y=["Movie", "TV Show"],
        barmode="group",
        title="Genre Distribution by Type"
    )
    st.plotly_chart(fig2, use_container_width=True)