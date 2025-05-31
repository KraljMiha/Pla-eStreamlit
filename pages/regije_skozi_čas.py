import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="Primerjava regij", layout="wide")
st.markdown("<h1 style='color: #ff4d4d;'>📍 Primerjava bruto plač med regijami skozi leta</h1>", unsafe_allow_html=True)

csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../placa_utf8.csv"))
df = pd.read_csv(csv_path)
df["DATA"] = pd.to_numeric(df["DATA"], errors="coerce")

df = df[
    (df["PLAČA"] == "Bruto") &
    (df["MERITVE"] == "Povprečje") &
    (df["STATISTIČNA REGIJA"] != "SLOVENIJA")
].copy()

with st.sidebar:
    st.header("🎛️ Filtri")
    spol = st.radio("Spol", ["Moški", "Ženske", "Spol - SKUPAJ"])
    starost = st.selectbox("Starostna skupina", sorted(df["STAROST"].unique()))
    st.markdown("Podatki prikazujejo povprečne **bruto plače** po regijah skozi leta.")

df_filtered = df[(df["SPOL"] == spol) & (df["STAROST"] == starost)]

fig = px.line(
    df_filtered,
    x="LETO",
    y="DATA",
    color="STATISTIČNA REGIJA",
    markers=True,
    labels={"DATA": "Bruto plača (€)", "LETO": "Leto", "STATISTIČNA REGIJA": "Regija"},
    title=f"📈 Bruto plače po regijah skozi čas ({spol}, {starost})"
)
fig.update_layout(legend_title_text="Regija", title_x=0.05)

st.plotly_chart(fig, use_container_width=True)

with st.expander("📄 Pokaži podatkovno tabelo"):
    st.dataframe(df_filtered.sort_values(["STATISTIČNA REGIJA", "LETO"]), use_container_width=True)
