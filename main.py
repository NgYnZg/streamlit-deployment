import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

st.title("🎬 Netflix Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["year_added"] = df["date_added"].dt.year
    return df

df = load_data()

st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", len(df))
col2.metric("Movies", len(df[df["type"] == "Movie"]))
col3.metric("TV Shows", len(df[df["type"] == "TV Show"]))


# =========================
# CHART 1: Content Type
# =========================

type_count = df["type"].value_counts().reset_index()
type_count.columns = ["type", "count"]

fig1 = px.pie(
    type_count,
    names="type",
    values="count",
    title="Movies vs TV Shows"
)

st.plotly_chart(fig1, use_container_width=True)


# =========================
# CHART 2: Release Trend
# =========================

year_data = df.groupby("release_year").size().reset_index(name="count")

fig2 = px.line(
    year_data,
    x="release_year",
    y="count",
    title="Titles Released Per Year"
)

st.plotly_chart(fig2, use_container_width=True)


# =========================
# CHART 3: Top Countries
# =========================

df["country"] = df["country"].fillna("Unknown")
country_counts = df["country"].value_counts().head(10).reset_index()
country_counts.columns = ["country", "count"]

fig3 = px.bar(
    country_counts,
    x="country",
    y="count",
    title="Top 10 Content Producing Countries"
)

st.plotly_chart(fig3, use_container_width=True)


# =====================================
# FUNCTION TO GENERATE PDF REPORT
# =====================================

def create_pdf():

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Netflix Dashboard Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    # Convert charts to images
    img1 = BytesIO(pio.to_image(fig1, format="png"))
    img2 = BytesIO(pio.to_image(fig2, format="png"))
    img3 = BytesIO(pio.to_image(fig3, format="png"))

    elements.append(Paragraph("Content Type Distribution", styles["Heading2"]))
    elements.append(Image(img1, width=500, height=300))

    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Release Year Trend", styles["Heading2"]))
    elements.append(Image(img2, width=500, height=300))

    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Top Producing Countries", styles["Heading2"]))
    elements.append(Image(img3, width=500, height=300))

    pdf.build(elements)

    buffer.seek(0)
    return buffer


# =====================================
# DOWNLOAD BUTTON
# =====================================

st.subheader("Export Report")

pdf_file = create_pdf()

st.download_button(
    label="📄 Download Dashboard Report (PDF)",
    data=pdf_file,
    file_name="netflix_dashboard_report.pdf",
    mime="application/pdf"
)