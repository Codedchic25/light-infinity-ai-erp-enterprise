import subprocess
import sys
import time
import os

print("[âž”] Se curata procesele vechi de uvicorn...")
if sys.platform == "win32":
    subprocess.run(
        "taskkill /f /im uvicorn.exe",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

# Configuratie mediu de productie si cai
env_config = os.environ.copy()
env_config["RUN_ENV"] = "prod"
env_config["PYTHONPATH"] = "."

# 1. Terminalul 1: Backend FastAPI (Port 8000)
print("[âž”] Terminal 1: Se lanseaza Backend FastAPI (Port 8000)...")
backend_proc = subprocess.Popen(
    [
        sys.executable,
        "-m",
        "uvicorn",
        "main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
    ],
    env=env_config,
)

time.sleep(3)

# 2. Terminalul 2: Magazinul Public (Port 8599)
print("[âž”] Terminal 2: Se lanseaza Magazinul Public (Port 8599)...")
shop_proc = subprocess.Popen(
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "frontend/public_shop.py",
        "--server.port",
        "8599",
    ],
    env=env_config,
)

# 3. Terminalul 3: Dashboard-ul Tau Real (Mutat pe portul liber 8570 pentru a sparge cache-ul)
print("[âž”] Terminal 3: Se lanseaza Dashboard-ul Tau Real (Port 8570)...")
try:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "dashboard.py",
            "--server.port",
            "8570",
        ],
        env=env_config,
        check=True,
    )
except KeyboardInterrupt:
    print("\n[!] Oprire solicitata.")
finally:
    backend_proc.terminate()
    shop_proc.terminate()
    print("[âœ“] Toate procesele au fost inchise.")

