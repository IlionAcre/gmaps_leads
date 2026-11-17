"""Streamlit dashboard for the Google Local Services lead scraper in main.py.

Run a search, review the collected listings, then export them as CSV, Excel or JSON.
"""
import io
import re

import pandas as pd
import streamlit as st

from main import gmaps_scraper

# Card fields from main.py and the column names shown in the dashboard
COLUMNS = {
    "title": "Company",
    "rating": "Rating",
    "ratings_count": "Reviews",
    "phone": "Phone",
    "website": "Website",
    "address": "Address",
    "services": "Services",
    "services_location": "Service area",
    "age": "Years in business",
}

st.set_page_config(page_title="GMaps Leads", page_icon="📍", layout="wide")


def to_rating(text):
    """A rating such as '4.9' or '4,9' as a number, or None."""
    match = re.search(r"\d+(?:[.,]\d+)?", text) if isinstance(text, str) else None
    return float(match.group().replace(",", ".")) if match else None


def to_count(text):
    """A review count such as '(512)' or '1,204 reviews' as a whole number, or None."""
    match = re.search(r"\d[\d,.]*", text) if isinstance(text, str) else None
    return int(re.sub(r"\D", "", match.group())) if match else None


def run_search(query, location):
    cards = gmaps_scraper(f"{query} in {location}")
    df = pd.DataFrame([card.model_dump() for card in cards], columns=list(COLUMNS))
    df = df.rename(columns=COLUMNS)
    df["Rating"] = df["Rating"].map(to_rating)
    df["Reviews"] = df["Reviews"].map(to_count).astype("Int64")
    return df


with st.sidebar:
    st.title("📍 Search")
    query = st.text_input("Business type", value="Tattoo studios")
    location = st.text_input("City or region", value="Toronto, ON")
    shown = st.multiselect("Columns", options=list(COLUMNS.values())[1:], default=list(COLUMNS.values())[1:6])
    start = st.button("Collect listings", width="stretch", type="primary")

st.title("GMaps Leads")
st.caption("Collects Google Local Services listings for a business type and area, then exports them for a sales workflow.")

if start:
    with st.spinner(f"Collecting '{query}' listings in {location}. A browser window opens while it runs."):
        try:
            st.session_state.leads = run_search(query, location)
            st.session_state.file_stem = f"{query}_{location}".replace(" ", "_").replace(",", "")
        except Exception as error:  # the scraper drives a live page: report the failure instead of crashing the app
            st.error(f"The scraper stopped: {error}")

df = st.session_state.get("leads")
if df is None:
    st.info("Enter a business type and an area in the sidebar, then select **Collect listings**.")
    st.stop()

total = len(df)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Listings", total)
col2.metric("With phone", f"{df['Phone'].notna().sum()}/{total}")
col3.metric("With website", f"{df['Website'].notna().sum()}/{total}")
col4.metric("Average rating", f"{df['Rating'].mean():.2f} ★" if df["Rating"].notna().any() else "–")

st.dataframe(
    df[["Company", *shown]],
    width="stretch",
    hide_index=True,
    column_config={
        "Rating": st.column_config.NumberColumn(format="%.1f ★"),
        "Website": st.column_config.LinkColumn(),
    },
)

st.subheader("Export")
stem = st.session_state.file_stem
excel = io.BytesIO()
with pd.ExcelWriter(excel, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="Leads")
csv_col, excel_col, json_col = st.columns(3)
csv_col.download_button("CSV", df.to_csv(index=False).encode("utf-8"), f"{stem}.csv", "text/csv", width="stretch")
excel_col.download_button(
    "Excel",
    excel.getvalue(),
    f"{stem}.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    width="stretch",
)
json_col.download_button(
    "JSON", df.to_json(orient="records", indent=2).encode("utf-8"), f"{stem}.json", "application/json", width="stretch"
)
