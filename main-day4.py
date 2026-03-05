import streamlit as st
import pandas as pd
import numpy as np

st.markdown('#Sample DataFrame')

np.random.seed(42)

dates = pd.date_range(start='2025-01-01', periods=20, freq="D")

property_type = np.random.choice(["Condo", "Landed", "Apartment"], size=20)

location = np.random.choice(["KL", "Selangor", "Penang"], size=20)

price = np.random.randint(300000, 1500000, size=20) # Property price (RM)
size_sqft = np.random.randint(600, 3500, size=20) # Size in square feet
bedrooms = np.random.randint(1, 6, size=20) # Number of bedrooms

df = pd.DataFrame({

"Listing Date": dates,
"Property Type": property_type,
"Location": location,
"Price (RM)": price,
"Size (sqft)": size_sqft,
"Bedrooms": bedrooms

})

st.title("Real Estate Listings")
st.subheader("Data Visualisation")
st.dataframe(df)

st.subheader("Line Chart: Price Trends Over Time")
line_df = df.set_index("Listing Date")[["Price (RM)"]]