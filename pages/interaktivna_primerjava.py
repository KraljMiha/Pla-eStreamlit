import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../placa_utf8.csv"))
df = pd.read_csv(base_path)
df["DATA"] = pd.to_numeric(df["DATA"], errors="coerce")

df = df[
    (df["PLAČA"] == "Bruto") &
    (df["MERITVE"] == "Povprečje") &
    (df["STATISTIČNA REGIJA"] != "SLOVENIJA")
]

st.title("📈 Interaktivna analiza bruto plač po regijah")
leto = st.slider("Izberi leto", int(df["LETO"].min()), int(df["LETO"].max()), 2022)
regija = st.selectbox("Izberi regijo", sorted(df["STATISTIČNA REGIJA"].unique()))
spol = st.radio("Izberi spol", ["Moški", "Ženske", "Spol - SKUPAJ"])
starost = st.selectbox("Izberi starostno skupino", sorted(df["STAROST"].unique()))

filt = (
    (df["LETO"] == leto) &
    (df["SPOL"] == spol) &
    (df["STATISTIČNA REGIJA"] == regija) &
    (df["STAROST"] == starost)
)
value = df[filt]["DATA"].values

user_age = st.slider("Izberi svojo starost:", 15, 65, 30)
if user_age <= 24:
    starost_skupina = "15-24 let"
elif user_age <= 34:
    starost_skupina = "25-34 let"
elif user_age <= 44:
    starost_skupina = "35-44 let"
elif user_age <= 54:
    starost_skupina = "45-54 let"
elif user_age <= 64:
    starost_skupina = "55-64 let"
else:
    starost_skupina = "65 let ali več"

st.write(f"Spadaš v skupino: **{starost_skupina}**")

if value.size > 0:
    st.metric(label="Povprečna bruto plača (€)", value=f"{value[0]:.0f}")
else:
    st.warning("Za izbrano kombinacijo ni podatkov.")

st.subheader(f"📉 Trendi plače v regiji {regija} ({spol}, {starost})")

trend_df = df[
    (df["SPOL"] == spol) &
    (df["STATISTIČNA REGIJA"] == regija) &
    (df["STAROST"] == starost)
].copy()

trend_df["LETO"] = pd.to_numeric(trend_df["LETO"], errors="coerce")
trend_df = trend_df.sort_values("LETO")
trend_df = trend_df.dropna(subset=["DATA"])


if trend_df["LETO"].nunique() < (df["LETO"].max() - df["LETO"].min() + 1):
    st.warning("⚠️ Nekatera leta manjkajo v podatkih za izbrano kombinacijo.")

fig, ax = plt.subplots()
sns.lineplot(data=trend_df, x="LETO", y="DATA", ax=ax, marker="o")
ax.set_ylabel("Bruto plača (€)")
ax.set_xlabel("Leto")
ax.grid(True)
st.pyplot(fig)

st.write("✅ Podatki za izris:")
st.dataframe(trend_df[["LETO", "DATA"]])
