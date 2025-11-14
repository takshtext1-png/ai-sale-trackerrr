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
import json
from oauth2client.service_account import ServiceAccountCredentials

service_account_info = json.loads(os.environ[{
  "type": "service_account",
  "project_id": "ringed-rune-478116-g8",
  "private_key_id": "d5dbc062f39f9d24d109759d9434f4ce22825c3d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCwLmZz6kgoddCt\nX/zDwEmKm9f/yDnK8Y85rXT/wBBtj8+VKd2awIwuT6BV8Ym7muC1WEVckiLcSKAB\n2sDU8eHVVobOAp9u8RMHyZfkj7XG4NgCwY7hK1wfP/YEdO8+vWGqcdCDS7hF22Nr\nmR3159fZW/1owv5znt3vpUPjDRDLjZrb0jUnmJy4fcE1VoXIP7PoiNOkd4L0oJ1p\nBG1ZHb9sX2UI6P2rJRNHFTQrk9ZdyGd81T7tA6JL0KSYy8be2o1NalFKaH7yMgy0\n9AH1yZlV0m8tqtVi/j8vwYqqVSKBNZA3ouqjD8kUw5/dP/5pcSq0co2yBfdAa+kN\nrf6yD9kPAgMBAAECggEABgv8UDYroS00qv6vD447TUU+tfS1UcCAs0YUzJesTgEF\nlY+zn2rEZO0utO8ZVGsNvgD4QHkeNoP3me4GzZ2PrAwljE84EaK3OH6JdrrH+Q92\nhSxc2bWXRStOJ6ZWdRzNjAAOsV2ZRtcveQiZp/r7xDtisy8eH0cbREJegMh4rxka\nXKX4ho5ko7VmIMvk0MXtzGxa24jAMK+vzMN9WNqTM1dstC+CR4p4/EamtQZIanK9\nTZvQ9sq55Grohoqg0/nlERVlnwp03utc28pnaNtpo9TNTc+uFABzXWBs64Tu2h7Z\nxGqymTooq55FQTDLolFl/ma7+XvG2z0YcCgY4MqrgQKBgQD3GpuEwVIm9c9kuTEo\nPopZm2al3ggrheDUjlHBwne9yciZpjaq39KanO4RRaueytB4zyS99zYbWDInZWgo\nA2YZRbTjUbt6tJJS/S1FP6IXTkgvsd8ox6ru3h21z0JOPORW+SyIcyv1kKdwPQ30\nPOrxmw0EtQkdyyHbHBjHwaSm0QKBgQC2hiVBkCER0ojScoHmfbYfTo7CzhEjEUk2\nq0gN4ey3D2XGRTutzMEJRZW5nxRdH+MryycukTqOfBoOkA1Y6H+3OCO/G2rdPIj9\nCfTO2o5prxicXB6xf7kOtQ8o7klXLpM/Pt1hlrB4kW7KKs/qjzH3kQsgQcIVgszm\nCwQGbh453wKBgB8Td4+AiIZhz41JRQdcpiWSx5wAimJ+2cGhjGKjxE9X+yRnpORk\ndaYAKmh9rJGxy/oFgwdo+aMCunv94tV1Z/exrogQFVXfM6/AK1tUH1xy+d0Vr4z/\nX13fDTl6MUqJmeXePF2ErniZkpUo+IJIzvtHlqGK6vSWQVG+/NbSYZShAoGAV2aI\n9Iolq7ka11sJpOtRiFA/wDyYrCgc3NbL3AnxJf9zhqukVicT0HLHrWjlgWpBh7jx\n/DSCy7PVbl/AZHCAp6V0SJDCbUoNds2LsnmpdCXqLQVXlTtJzCcbKUhhSiP9Um2x\n6IcV3cYWPSye/vyuupNztnCGlXJa11UzCjk0tBUCgYEApVKmVf0bP9QOTQZDDxHi\nILL09KXFI48io74S0VXD5UX1/SjzY7YiRaL7wmaQiX5F8BV3tAoMOo2OvKnTfJ5Q\nQ3tHSAcsSIbzFHJH0KMEZo+ECZIQsysvvc3fEiUjpHHQVz5fH1vQ1TJHkNCB7agW\nnkKeRQxmvJj3dJDmeRenEfU=\n-----END PRIVATE KEY-----\n",
  "client_email": "ai-sales-track@ringed-rune-478116-g8.iam.gserviceaccount.com",
  "client_id": "101811149548929761877",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ai-sales-track%40ringed-rune-478116-g8.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
])
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
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
