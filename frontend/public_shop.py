import os
import requests
import streamlit as st
from dotenv import load_dotenv

# ÃŽncarcam variabilele de mediu din fisierul .env
load_dotenv()

# Configuratii initiale de tema - Magazin Public Retail Premium
st.set_page_config(
    page_title="ðŸ›’ Light Infinity AI - E-Shop",
    page_icon="ðŸ›’",
    layout="wide",
    initial_sidebar_state="expanded",
)

URL_API = os.getenv(
    "URL_API", "http://localhost:8000"
)  # Schimbat din 127.0.0.1 in localhost

if "comanda_confirmata_id" in st.session_state:
    st.success(f"ðŸŽ‰ {st.session_state['mesaj_succes_persistent']}")
    if st.button("Am inteles / ÃŽnchide notificarea", key="btn_inchide_notif"):
        del st.session_state["comanda_confirmata_id"]
        del st.session_state["mesaj_succes_persistent"]
        st.rerun()
        
# --- MATRICEA DE TRADUCERI MULTI-LANGUAGE (i18n) ---
TRADUCERI = {
    "RO": {
        "titlu": "âš¡ LIGHT INFINITY AI - Magazin LumÃ¢nari",
        "info_stoc": "Toate comenzile sunt legate live de retetarul industrial ERP (BOM) cu protectie anti-stoc negativ.",
        "cos": "ðŸ›’ Cosul tau",
        "nume": "Nume si Prenume Client",
        "adresa": "Adresa Completa Livrare",
        "buton_comanda": "ðŸš€ Trimite Comanda Reala",
        "aduga_cos": "Adauga in cos",
        "succes": "ðŸŽ‰ Comanda plasata cu succes! ID Comanda inregistrat in DB: #",
        "gol": "Cosul de cumparaturi este gol.",
        "pret": "Pret:",
        "total": "Total de plata:",
        "campuri_obligatorii": "Va rugam sa completati numele si adresa de livrare.",
    },
    "EN": {
        "titlu": "âš¡ LIGHT INFINITY AI - Candles Shop",
        "info_stoc": "All orders are linked live to the industrial ERP recipe (BOM) with anti-negative stock protection.",
        "cos": "ðŸ›’ Your Cart",
        "nume": "Customer Full Name",
        "adresa": "Full Delivery Address",
        "buton_comanda": "ðŸš€ Place Real Order",
        "aduga_cos": "Add to cart",
        "succes": "ðŸŽ‰ Order placed successfully! Order ID registered in DB: #",
        "gol": "Your shopping cart is empty.",
        "pret": "Price:",
        "total": "Total amount:",
        "campuri_obligatorii": "Please fill in your name and delivery address.",
    },
    "DE": {
        "titlu": "âš¡ LIGHT INFINITY AI - Kerzenladen",
        "info_stoc": "Alle Bestellungen sind live mit dem industriellen ERP-Rezept (BOM) verknÃ¼pft, mit Schutz vor gegen negativem Lagerbestand.",
        "cos": "ðŸ›’ Ihr Warenkorb",
        "nume": "VollstÃ¤ndiger Kundenname",
        "adresa": "VollstÃ¤ndige Lieferadresse",
        "buton_comanda": "ðŸš€ Echte Bestellung Absenden",
        "aduga_cos": "In den Warenkorb",
        "succes": "ðŸŽ‰ Bestellung erfolgreich aufgegeben! Bestell-ID in DB registriert: #",
        "gol": "Ihr Warenkorb ist leer.",
        "pret": "Preis:",
        "total": "Gesamtbetrag:",
        "campuri_obligatorii": "Bitte fÃ¼llen Sie Ihren Namen und Ihre Lieferadresse aus.",
    },
    "IT": {
        "titlu": "âš¡ LIGHT INFINITY AI - Negozio di Candele",
        "info_stoc": "Tutti gli ordini sono collegati in tempo reale alla ricetta industriale ERP (BOM) con protezione stock anti-negativo.",
        "cos": "ðŸ›’ Il tuo Carrello",
        "nume": "Nome Completo del Cliente",
        "adresa": "Indirizzo di Spedizione Completo",
        "buton_comanda": "ðŸš€ Invia Ordine Reale",
        "aduga_cos": "Aggiungi al carrello",
        "succes": "ðŸŽ‰ Ordine effettuato con successo! ID Ordine registrato nel DB: #",
        "gol": "Il tuo carrello Ã¨ vuoto.",
        "pret": "Prezzo:",
        "total": "Totale da pagare:",
        "campuri_obligatorii": "Si prega di inserire il nome e l'indirizzo di spedizione.",
    },
}

# --- MANAGEMENTUL DINAMIC AL LIMBII (REBUILD SECURIZAT FÄ‚RÄ‚ RERUN) ---
# Initializam limba implicita direct in starea sesiunii daca nu exista
if "limba_activa" not in st.session_state:
    st.session_state["limba_activa"] = "RO"

st.sidebar.markdown("### ðŸŒ Language / Limba")

# Folosim cheia directa din session_state pentru a lasa Streamlit sa gestioneze automat starea
limba_selectata = st.sidebar.selectbox(
    "Choose Language:",
    options=["RO", "EN", "DE", "IT"],
    key="limba_activa",  # Se leaga nativ de st.session_state["limba_activa"]
    format_func=lambda x: (
        "ðŸ‡·ðŸ‡´ RomÃ¢na"
        if x == "RO"
        else "ðŸ‡ºðŸ‡¸ English"
        if x == "EN"
        else "ðŸ‡©ðŸ‡ª Deutsch"
        if x == "DE"
        else "ðŸ‡®ðŸ‡¹ Italiano"
    ),
    label_visibility="collapsed",
)

# Preluam traducerile pentru limba curenta
txt = TRADUCERI[st.session_state["limba_activa"]]

# Initializam cosul de cumparaturi daca nu exista
if "cos" not in st.session_state:
    st.session_state["cos"] = []

# --- RENDERE TITLU È˜I CONTEXT LOGISTIC DINAMIC TRADUS ---
st.title(txt["titlu"])
st.info(txt["info_stoc"])

# --- EXTRACT LIVE CATALOG CU RUTA CORECTÄ‚ DIN BACKEND ---
if "produse_catalog" not in st.session_state or not st.session_state["produse_catalog"]:
    try:
        # CORECTAT: Schimbat din /catalog/lumanari in calea oficiala inregistrata /api/v1/
        # Adaugam un timeout generos de 15 secunde pentru a preveni erorile de tip Read Timeout
        url_catalog_real = f"{URL_API}/api/v1/"

        raspuns_catalog = requests.get(url_catalog_real, timeout=15)

        if raspuns_catalog.status_code == 200:
            st.session_state["produse_catalog"] = raspuns_catalog.json()
        else:
            st.session_state["produse_catalog"] = []
            st.error(
                f"âš ï¸ Serverul a raspuns cu codul {raspuns_catalog.status_code} la solicitarea catalogului."
            )

    except Exception as e:
        st.error(
            f"âš ï¸ Conexiune esuata cu API-ul de catalog la {URL_API}/api/v1/: {str(e)}"
        )
        st.session_state["produse_catalog"] = []

# Mapam produsele din starea sigura a sesiunii
produse = st.session_state["produse_catalog"]


# --- MAPARE TRADUCERI PRODUSE DIN DB PENTRU I18N (VARIANTÄ‚ IMUNÄ‚ LA DIACRITICE) ---
# --- MAPARE TRADUCERI PRODUSE DIN DB PENTRU I18N ---
# Folosim exclusiv litere mici fara diacritice pentru chei sigure
TRADUCERI_PRODUSE = {
    "lumanare relaxare": {
        "RO": "LumÃ¢nare Relaxare",
        "EN": "Relaxing Candle",
        "DE": "Entspannungskerze",
        "IT": "Candela Relax",
    },
    "lumanare parfumata lavanda": {
        "RO": "LumÃ¢nare Parfumata Lavanda",
        "EN": "Scented Lavender Candle",
        "DE": "Duftende Lavendelkerze",
        "IT": "Candela Profumata alla Lavanda",
    },
}

# Randare dinamica pe 3 coloane pentru vitrina de produse finite
if produse:
    cols = st.columns(3)
    limba_curenta = st.session_state["limba_activa"]

    for idx, prod in enumerate(produse):
        with cols[idx % 3]:
            with st.container(border=True):
                id_prod = prod.get("id_lumanare")
                nume_original = str(prod.get("nume", "Lumanare"))
                pret_prod = float(prod.get("pret") or 0.0)

                # Curatam textul brut din DB pentru a evita blocajele de encoding sau diacritice
                nume_cheie = (
                    nume_original.lower()
                    .replace("Ã¢", "a")
                    .replace("a", "a")
                    .replace("ÅŸ", "s")
                    .replace("Å£", "t")
                    .replace("s", "s")
                    .replace("t", "t")
                    .strip()
                )

                # ÃŽncercam traducerea. Daca esueaza sau nu exista, cadem pe numele brut din DB
                try:
                    if nume_cheie in TRADUCERI_PRODUSE:
                        nume_afisat = TRADUCERI_PRODUSE[nume_cheie][limba_curenta]
                    else:
                        nume_afisat = nume_original
                except Exception:
                    nume_afisat = nume_original

                st.subheader(nume_afisat)
                st.markdown(f"**{txt['pret']}** {pret_prod:.2f} RON")
                st.write(prod.get("descriere", ""))

                # Buton de adaugare in cos
                if st.button(
                    txt["aduga_cos"],
                    key=f"add_{id_prod}_{idx}",
                    use_container_width=True,
                ):
                    prod_copie = prod.copy()
                    prod_copie["nume"] = nume_afisat
                    st.session_state["cos"].append(prod_copie)
                    st.toast("ðŸ›’ Adaugat in cos!")
                    st.rerun()
else:
    st.warning("âš ï¸ Catalogul de produse a returnat o lista goala de la API.")

# --- STRUCTURÄ‚ LOGICÄ‚ PENTRU SIDEBAR: CHECKOUT È˜I COÈ˜ ---
with st.sidebar:
    st.markdown("---")
    st.header(txt["cos"])

    if not st.session_state["cos"]:
        st.write(txt["gol"])
        total_plata = 0.0
    else:
        total_plata = 0.0
        for item in st.session_state["cos"]:
            st.markdown(
                f"ðŸ”¹ **{item.get('nume')}** â€” {float(item.get('pret', 0.0)):.2f} RON"
            )
            total_plata += float(item.get("pret") or 0.0)

        st.markdown(f"### {txt['total']} {total_plata:.2f} RON")

        if st.button("Clear", use_container_width=True):
            st.session_state["cos"] = []
            st.rerun()

        st.markdown("---")

        nume_client = st.text_input(txt["nume"], placeholder="Mary Pop")
        email_client = st.text_input("Email", placeholder="mary.pop@infinity.ai")
        adresa_livrare = st.text_area(txt["adresa"], placeholder="Strada...")

        if st.button(txt["buton_comanda"], type="primary", use_container_width=True):
            if not nume_client or not adresa_livrare:
                st.error(txt["campuri_obligatorii"])
            else:
                linii_produse_payload = []
                for item in st.session_state["cos"]:
                    linii_produse_payload.append(
                        {
                            "id_lumanare": int(item.get("id_lumanare")),
                            "cantitate": 1,
                            "pret_salvat": float(item.get("pret", 0.0)),
                        }
                    )

                # Construirea payload-ului oficial aliniat la schema Pydantic din backend
                payload = {
                    "nume_client": str(nume_client),
                    "email_client": str(email_client)
                    if email_client
                    else "client@infinity.ai",
                    "adresa_livrare": str(adresa_livrare),
                    "produse": linii_produse_payload,
                }

                try:
                    with st.spinner("Se proceseaza tranzactia securizata..."):
                        raspuns = requests.post(
                            f"{URL_API}/orders/checkout", json=payload, timeout=10
                        )

                    if raspuns.status_code == 201:
                        date_raspuns = raspuns.json()
                        id_comanda = date_raspuns.get("id_comanda", "1")

                        # âœ… SALVÄ‚M CONFIRMAREA ÃŽN STAREA SESIUNII PENTRU A FI PERSISTENTÄ‚
                        st.session_state["comanda_confirmata_id"] = id_comanda
                        st.session_state["mesaj_succes_persistent"] = (
                            f"{txt['succes']}{id_comanda}"
                        )

                        st.session_state["cos"] = []  # Golim cosul dupa succes
                        st.balloons()
                        st.rerun()

                    else:
                        try:
                            eroare_msg = raspuns.json().get("detail", raspuns.text)
                        except Exception:
                            eroare_msg = raspuns.text
                        st.error(
                            f"âš ï¸ Eroare Server Backend ({raspuns.status_code}): {eroare_msg}"
                        )
                except Exception as e:
                    st.error(f"âŒ Conexiune esuata cu serverul API: {str(e)}")

