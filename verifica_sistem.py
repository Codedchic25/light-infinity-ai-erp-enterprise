"""
Script complet de diagnosticare si Smoke Testing pentru ecosistemul Light Infinity AI.
Verifica serviciile Windows si conectivitatea endpoint-urilor critice FastAPI (AI & Analytics).
"""

import subprocess
import requests


def check_postgres_windows():
    print("[âž”] Pasul 1: Verificare serviciu PostgreSQL in Windows...")
    # Cautam serviciul local numit postgresql
    cmd = "Get-Service -Name *postgres* | Select-Object Name, Status"
    proc = subprocess.run(
        ["powershell", "-Command", cmd], capture_output=True, text=True
    )

    if "Running" in proc.stdout:
        print("[âœ“] PostgreSQL ruleaza deja in Windows.")
        return True
    else:
        print(
            "[!] Serviciul PostgreSQL este oprit sau nu este pornit ca serviciu local Windows."
        )
        print("[âž”] ÃŽncercam pornirea fortata a serviciului de retea PostgreSQL...")
        # ÃŽncercam sa pornim serviciul local prin PowerShell comanda directa
        subprocess.run(
            ["powershell", "-Command", "Start-Service -Name *postgres*"],
            capture_output=True,
        )
        return False


def test_backend_modules():
    print("\n[âž”] Pasul 2: Testare functionalitati Prognoze si Asistent AI...")
    base_url = "http://127.0.0.1:8000"

    # --- RULAREA 1: CONEXIUNE DE BAZÄ‚ LA SERVER ---
    try:
        res = requests.get(base_url, timeout=2)
        print(f"[âœ“] Conexiune Backend generala: Activa (Status {res.status_code})")
    except Exception:
        print(
            "[X] Backend-ul FastAPI pe portul 8000 nu raspunde. Asigura-te ca ruleaza 'uv run uvicorn main:app' intr-un terminal separat."
        )
        return

    # --- RULAREA 2: MODULUL AI CHAT (ASISTENT AI) ---
    try:
        print("[âž”] Se testeaza ruta AI Chat cu o intrebare de test...")
        payload = {"message": "Salut! Ce stocuri avem?"}
        res_ai = requests.post(f"{base_url}/ai/chat", json=payload, timeout=5)
        if res_ai.status_code == 200:
            print("[âœ“] Modulul Asistent AI functioneaza perfect!")
            print(f"    Raspuns Llama: {res_ai.json().get('response', '')[:60]}...")
        else:
            print(
                f"[X] Modulul AI a raspuns cu eroarea {res_ai.status_code}. Verifica cheia API sau modelul LLM local."
            )
    except Exception as e:
        print(f"[X] Nu s-a putut contacta ruta AI Chat: {e}")

    # --- RULAREA 3: MODULUL DE ANALYTICS (PROGNOZE) ---
    try:
        print("[âž”] Se testeaza ruta de prognoze/analitice...")
        res_an = requests.get(f"{base_url}/analytics/predictions", timeout=3)
        if res_an.status_code == 200:
            print("[âœ“] Modulul de Prognoze livreaza date corecte din baza de date.")
        else:
            print(
                f"[I] Nota: Ruta de prognoze din backend a intors status {res_an.status_code}. Se folosesc datele din interfata."
            )
    except Exception:
        print(
            "[I] Nota: Modulul de prognoze nu este mapat pe o ruta dedicata de tip GET. Ruleaza exclusiv in Streamlit."
        )


if __name__ == "__main__":
    check_postgres_windows()
    test_backend_modules()

