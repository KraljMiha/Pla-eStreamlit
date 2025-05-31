import streamlit as st

st.image("slike/Regije_Slovenija.png", width=600)  # ali path do tvoje slike

st.markdown("<h1 style='color:#4db8ff;'>📊 Interaktivna analiza plač v Sloveniji</h1>", unsafe_allow_html=True)
st.markdown("""
Dobrodošli v aplikaciji, kjer si lahko interaktivno ogledate:
- bruto plače po regijah in starostnih skupinah
- razliko med spoloma
- trende skozi čas

Uporabite meni na levi za izbiro posamezne analize.
""")
name = st.text_input("Vnesi svoje ime:")
if name:
    st.write(f"Pozdravljen, {name}! 👋 Dobrodošel v analizi slovenskih plač.")

