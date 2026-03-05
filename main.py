import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

st.title("🎬 Netflix Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    return df

df = load_data()

# =====================
# Chart 1: Movies vs TV Shows
# =====================

type_counts = df["type"].value_counts()

fig1, ax1 = plt.subplots()
ax1.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%')
ax1.set_title("Movies vs TV Shows")

st.pyplot(fig1)


# =====================
# Chart 2: Release Year Trend
# =====================

year_counts = df["release_year"].value_counts().sort_index()

fig2, ax2 = plt.subplots()
ax2.plot(year_counts.index, year_counts.values)
ax2.set_title("Titles Released Per Year")
ax2.set_xlabel("Year")
ax2.set_ylabel("Number of Titles")

st.pyplot(fig2)


# =====================
# Chart 3: Top Countries
# =====================

df["country"] = df["country"].fillna("Unknown")
top_countries = df["country"].value_counts().head(10)

fig3, ax3 = plt.subplots()
ax3.bar(top_countries.index, top_countries.values)
ax3.set_title("Top 10 Countries Producing Content")
ax3.set_xlabel("Country")
ax3.set_ylabel("Titles")
plt.xticks(rotation=45)

st.pyplot(fig3)


# =====================
# Function: Create PDF
# =====================

def create_pdf():

    buffer = BytesIO()
    styles = getSampleStyleSheet()

    story = []
    story.append(Paragraph("Netflix Dashboard Report", styles['Title']))
    story.append(Spacer(1,20))

    # Save figures as images
    img1 = BytesIO()
    fig1.savefig(img1, format="png")
    img1.seek(0)

    img2 = BytesIO()
    fig2.savefig(img2, format="png")
    img2.seek(0)

    img3 = BytesIO()
    fig3.savefig(img3, format="png")
    img3.seek(0)

    story.append(Paragraph("Movies vs TV Shows", styles['Heading2']))
    story.append(Image(img1, width=500, height=300))
    story.append(Spacer(1,20))

    story.append(Paragraph("Release Trend", styles['Heading2']))
    story.append(Image(img2, width=500, height=300))
    story.append(Spacer(1,20))

    story.append(Paragraph("Top Countries", styles['Heading2']))
    story.append(Image(img3, width=500, height=300))

    pdf = SimpleDocTemplate(buffer)
    pdf.build(story)

    buffer.seek(0)
    return buffer


# =====================
# Download Button
# =====================

st.subheader("Download Report")

pdf_file = create_pdf()

st.download_button(
    label="Download Dashboard as PDF",
    data=pdf_file,
    file_name="netflix_dashboard_report.pdf",
    mime="application/pdf"
)