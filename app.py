# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 23:18:14 2025

@author: tarse
"""

import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
import openai
from datetime import datetime

# --- CONFIGURATION ---
openai.api_key = ""  # your OpenAI API key here
GOOGLE_SHEET_NAME = "sales_data"
SERVICE_ACCOUNT_FILE = "client_secret.json"

# --- CONNECT TO GOOGLE SHEET ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
client = gspread.authorize(credentials)
sheet = client.open(GOOGLE_SHEET_NAME).sheet1

# --- APP TITLE ---
st.title("🧠 AI Sales Tracker (Daily Summary Version)")

# --- ADD SALES ENTRY ---
st.header("Add New Sale")
with st.form("sales_form"):
    product = st.text_input("Product Name")
    quantity = st.number_input("Quantity Sold", min_value=1, step=1)
    price = st.number_input("Price per Item (₹)", min_value=1.0, step=0.5)
    status = st.selectbox("Status", ["Sold", "Defected"])
    submitted = st.form_submit_button("Add Sale")

if submitted:
    date = datetime.now().strftime("%Y-%m-%d")
    sheet.append_row([date, product, quantity, price, status])
    st.success(f"✅ Recorded: {product} ({status})")

# --- LOAD DATA ---
data = pd.DataFrame(sheet.get_all_records())

if not data.empty:
    data["Quantity"] = pd.to_numeric(data["Quantity"], errors="coerce")
    data["Price"] = pd.to_numeric(data["Price"], errors="coerce")
    data["Revenue"] = data["Quantity"] * data["Price"]

    today = datetime.now().strftime("%Y-%m-%d")
    today_data = data[data["Date"] == today]

    st.subheader(f"📅 Today's Sales ({today})")
    st.dataframe(today_data)

    if not today_data.empty:
        total_sales = today_data[today_data["Status"] == "Sold"]["Revenue"].sum()
        defective = len(today_data[today_data["Status"] == "Defected"])
        st.metric("Total Revenue (₹)", f"{total_sales:,.2f}")
        st.metric("Defected Items", defective)

        top_products = today_data.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
        if not top_products.empty:
            fig, ax = plt.subplots()
            top_products.plot(kind="bar", ax=ax)
            ax.set_title("Top Selling Products (Today)")
            ax.set_ylabel("Revenue (₹)")
            st.pyplot(fig)

        # --- DAILY AI SUMMARY BUTTON ---
if st.button("🧠 Generate AI Daily Summary"):
    from openai import OpenAI

    prompt = f"""
    Summarize today's sales performance based on this data:
    {today_data.to_string(index=False)}
    Highlight top-selling items, total revenue, and any defects.
    """

    try:
        client = OpenAI(api_key=openai.api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        summary = response.choices[0].message.content
        st.subheader("🧠 AI Summary:")
        st.write(summary)

    except Exception as e:
        st.warning(f"OpenAI error: {e}")

    else:
        st.info("No sales recorded today yet.")
else:
    st.info("No data found. Add your first sale above.")
