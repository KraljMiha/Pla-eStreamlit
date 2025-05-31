import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../placa_utf8.csv"))
df = pd.read_csv(csv_path)
df["DATA"] = pd.to_numeric(df["DATA"], errors="coerce")

df = df[(df["LETO"] >= 2015) & (df["LETO"] <= 2022) & (df["MERITVE"] == "Povprečje")]

st.title("💸 Razmerje med neto in bruto plačo skozi čas (2015–2022)")

spol = st.radio("Izberi spol", sorted(df["SPOL"].dropna().unique()))
starost = st.selectbox("Izberi starostno skupino", sorted(df["STAROST"].dropna().unique()))
regija = st.selectbox("Izberi regijo", sorted(df["STATISTIČNA REGIJA"].dropna().unique()))

df_filtriran = df[
    (df["SPOL"] == spol) &
    (df["STAROST"] == starost) &
    (df["STATISTIČNA REGIJA"] == regija)
]

pivot = df_filtriran.pivot_table(index="LETO", columns="PLAČA", values="DATA")

pivot["Razmerje (%)"] = (pivot["Neto"] / pivot["Bruto"]) * 100

leta_v_grafu = pivot.index.tolist()
vsa_leta = list(range(2015, 2023)) 
manjkajoča_leta = sorted(set(vsa_leta) - set(leta_v_grafu))

if manjkajoča_leta:
    st.warning(f"⚠️ Za regijo **{regija}**, spol **{spol}** in starost **{starost}** ni podatkov za naslednja leta: {', '.join(map(str, manjkajoča_leta))}")

fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=pivot, x=pivot.index, y="Razmerje (%)", marker="o", ax=ax)
ax.set_title(f"Razmerje Neto/Bruto plače v regiji {regija} ({spol}, {starost})")
ax.set_ylabel("Razmerje (%)")
ax.set_xlabel("Leto")
plt.ylim(60, 70)
ax.grid(True)

st.pyplot(fig)
