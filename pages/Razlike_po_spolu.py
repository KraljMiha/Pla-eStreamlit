import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Spolne razlike po regijah", layout="wide")
st.markdown("<h1 style='color: salmon;'>♀️♂️ Spolne razlike po regijah</h1>", unsafe_allow_html=True)

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../placa_utf8.csv"))
df = pd.read_csv(base_path)
df["DATA"] = pd.to_numeric(df["DATA"], errors="coerce")

col1, col2 = st.columns([1, 2])
with col1:
    leto = st.selectbox("📅 Izberi leto", sorted(df["LETO"].unique(), reverse=True))
    placa_tip = st.radio("💰 Tip plače", ["Bruto", "Neto"], index=0)
with col2:
    st.markdown("#### ℹ️ Vizualizacija prikazuje razliko med povprečnimi plačami moških in žensk po regijah.")
    with st.expander("❓ Kaj pomeni razlika (%)"):
        st.markdown("""
        Pozitivna vrednost pomeni, da moški zaslužijo več kot ženske v posamezni regiji.
        Negativna vrednost pomeni, da ženske zaslužijo več.
        """)

df_spol = df[
    (df["LETO"] == leto) &
    (df["PLAČA"] == placa_tip) &
    (df["MERITVE"] == "Povprečje") &
    (df["STAROST"] == "Starost - SKUPAJ") &
    (df["STATISTIČNA REGIJA"] != "SLOVENIJA") &
    (df["SPOL"].isin(["Moški", "Ženske"]))
]

pivot = df_spol.pivot_table(index="STATISTIČNA REGIJA", columns="SPOL", values="DATA").dropna()
pivot["RAZLIKA (%)"] = ((pivot["Moški"] - pivot["Ženske"]) / pivot["Ženske"]) * 100
pivot = pivot.sort_values("RAZLIKA (%)", ascending=False)

colors = ["#ff9999" if val > 0 else "#99ccff" for val in pivot["RAZLIKA (%)"]]

st.markdown("### 📊 Razlika v povprečnih plačah po regijah")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=pivot.index, y=pivot["RAZLIKA (%)"], palette=colors, ax=ax)
ax.axhline(0, color='gray', linestyle='--')
plt.xticks(rotation=45, ha='right')
plt.ylabel("Razlika v %")
plt.title(f"Spolna razlika v povprečni {placa_tip.lower()} plači po regijah ({leto})")
st.pyplot(fig)

st.markdown("### 📄 Podatkovna tabela")
st.dataframe(pivot.reset_index().rename(columns={"RAZLIKA (%)": "Razlika (%)"}), use_container_width=True)
