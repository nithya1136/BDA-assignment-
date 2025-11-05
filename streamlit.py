import streamlit as st
from cassandra.cluster import Cluster

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('canteen')

st.set_page_config(page_title="Canteen Analytics", page_icon="📈", layout="centered")

st.title("🍴 Canteen Analytics Dashboard")

# --- Top Items ---
def top_items():
    rows = session.execute("SELECT item, count FROM item_counts")
    sorted_rows = sorted(rows, key=lambda r: r.count, reverse=True)
    output = "Top 10 Most Sold Items:\n\n"
    for r in sorted_rows[:10]:
        output += f"{r.item} -> {r.count}\n"
    return output

# --- Top Pairs ---
def top_pairs():
    rows = session.execute("SELECT pair, count FROM item_pairs")
    sorted_rows = sorted(rows, key=lambda r: r.count, reverse=True)
    output = "Top 10 Frequently Bought Together Pairs:\n\n"
    for r in sorted_rows[:10]:
        output += f"{r.pair} -> {r.count}\n"
    return output

# --- Streamlit UI ---
if st.button("📊 Show Top Analytics"):
    st.subheader("Top 10 Most Sold Items")
    st.text(top_items())
    st.markdown("---")
    st.subheader("Top 10 Frequently Bought Together Pairs")
    st.text(top_pairs())
else:
    st.info("Click the button above to fetch analytics from Cassandra.")
