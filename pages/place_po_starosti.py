import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="Plače po starostnih skupinah", layout="wide")
st.markdown("<h1 style='color: #3366cc;'>👥 Povprečne bruto plače po starostnih skupinah in regijah</h1>", unsafe_allow_html=True)

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../placa_utf8.csv"))
df = pd.read_csv(base_path)
df["DATA"] = pd.to_numeric(df["DATA"], errors="coerce")

starostne_skupine = [
    "15-24 let", "25-34 let", "35-44 let",
    "45-54 let", "55-64 let", "65 let ali več"
]

with st.sidebar:
    st.header("🎛️ Filtri")
    leto = st.slider("Izberi leto", 2015, 2022, 2022)
    st.markdown("Podatki prikazujejo **bruto plače** v posameznih starostnih skupinah za regije (brez Slovenije kot celote).")

df_filtered = df[
    (df["LETO"] == leto) &
    (df["PLAČA"] == "Bruto") &
    (df["MERITVE"] == "Povprečje") &
    (df["SPOL"] == "Spol - SKUPAJ") &
    (df["STATISTIČNA REGIJA"] != "SLOVENIJA") &
    (df["STAROST"].isin(starostne_skupine))
].copy()

regija_avg = df_filtered.groupby("STATISTIČNA REGIJA")["DATA"].mean().sort_values(ascending=False)
df_filtered["STATISTIČNA REGIJA"] = pd.Categorical(
    df_filtered["STATISTIČNA REGIJA"],
    categories=regija_avg.index,
    ordered=True
)

fig = px.bar(
    df_filtered,
    x="STATISTIČNA REGIJA",
    y="DATA",
    color="STAROST",
    barmode="group",
    labels={
        "DATA": "Bruto plača (€)",
        "STATISTIČNA REGIJA": "Regija",
        "STAROST": "Starostna skupina"
    },
    title=f"📊 Povprečne bruto plače po regijah in starostnih skupinah ({leto})"
)
fig.update_layout(xaxis_tickangle=-45, title_x=0.05)

st.plotly_chart(fig, use_container_width=True)

with st.expander("📄 Prikaži podatkovno tabelo"):
    st.dataframe(df_filtered.sort_values(["STATISTIČNA REGIJA", "STAROST"]), use_container_width=True)
