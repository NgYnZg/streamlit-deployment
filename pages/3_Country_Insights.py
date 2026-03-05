import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🌍 Country Insights")

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    return df

df = load_data()

df['country'] = df['country'].fillna("Unknown")
df['country'] = df['country'].str.split(',')
df_exploded = df.explode('country')
df_exploded['country'] = df_exploded['country'].str.strip()

# UI
top_n = st.slider("Select Top N Countries", 5, 30, 10)

country_count = df_exploded['country'].value_counts().head(top_n).reset_index()
country_count.columns = ['Country', 'Count']

# Pie chart
fig1 = px.pie(
    country_count,
    names='Country',
    values='Count',
    title="Top Producing Countries"
)
st.plotly_chart(fig1, use_container_width=True)

# Scatter chart
scatter_data = df_exploded.groupby(['country', 'release_year']).size().reset_index(name='count')

fig2 = px.scatter(
    scatter_data,
    x="release_year",
    y="count",
    size="count",
    color="country",
    title="Country Production Over Years"
)
st.plotly_chart(fig2, use_container_width=True)