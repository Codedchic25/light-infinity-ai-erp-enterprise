import os

bloc_cod = """import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="⚡ LIGHT INFINITY AI - Admin ERP",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

URL_API = os.getenv("URL_API", "http://localhost:8000")

TRADUCERI_ADMIN = {
    "RO": {
        "navigare": "Navigare",
        "utilizator": "Utilizator activ:",
        "deconectare": "Deconectare",
        "panou_titru": "⚡ LIGHT INFINITY AI - MANAGEMENT TRANZACȚIONAL",
        "m1": "📊 Dashboard BI & Vânzări",
        "m2": "⚙️ Management Producție Loturi",
        "m3": "🤖 Copilot AI Producție (Llama 3.3)",
        "m4": "📦 Catalog Produse Active",
        "bi_titlu": "Analiză Economică Avansată și Indicatori KPI",
        "bi_context": "Sistemul tranzacțional este activ în mediul: {mediu}. Datele sunt procesate live.",
        "kpi_inventar": "Valoare Inventar Reală",
        "kpi_comenzi": "Comenzi în Așteptare",
        "kpi_stoc": "Stoc Critic Materie Prima (Ceară)",
        "kpi_delta_stoc": "-4.0 kg (Consum Automat BOM)",
        "kpi_delta_comenzi": "↑ Nouă comandă recepționată",
        "login_titlu": "⚡ LIGHT INFINITY AI",
        "login_sub": "Autentificare Securizată Panou Executiv",
        "login_email": "Securitate Identitate (Email)",
        "login_pass": "Cheie Criptată (Parolă)",
        "login_btn": "Conectare Securizată",
        "login_success": "Autentificare reușită! Se încarcă sistemul...",
    },
    "EN": {
        "navigare": "Navigation",
        "utilizator": "Active user:",
        "deconectare": "Sign Out",
        "panou_titru": "⚡ LIGHT INFINITY AI - TRANSACTIONAL MANAGEMENT",
        "m1": "📊 BI Dashboard & Sales",
        "m2": "⚙️ ERP Production Management",
        "m3": "🤖 Production AI Copilot (Llama 3.3)",
        "m4": "📦 Active Products Catalog",
        "bi_titlu": "Advanced Economic Analysis & KPI Metrics",
        "bi_context": "The transactional system is active in environment: {mediu}. Data is processed live.",
        "kpi_inventar": "Real Inventory Value",
        "kpi_comenzi": "Pending Orders",
        "kpi_stoc": "Critical Raw Material Stock (Wax)",
        "kpi_delta_stoc": "-4.0 kg (Automatic BOM Consumed)",
        "kpi_delta_comenzi": "↑ New order received",
        "login_titlu": "⚡ LIGHT INFINITY AI",
        "login_sub": "Secure Executive Panel Authentication",
        "login_email": "Identity Security (Email)",
        "login_pass": "Encrypted Key (Password)",
        "login_btn": "Secure Sign In",
        "login_success": "Authentication successful! Loading system...",
    },
"""
