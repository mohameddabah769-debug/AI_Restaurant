"""
Runner script for Eng. Mohamed Dabah 3D Portfolio
Run with: python run.py
"""

import sys
import os
from pathlib import Path
import webbrowser
import threading
import time
import uvicorn

CURRENT_DIR = Path(__file__).resolve().parent

# Ensure the current directory and its parent are in sys.path
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))
if str(CURRENT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR.parent))

def open_browser(url: str):
    time.sleep(1.5)
    try:
        webbrowser.open(url)
    except Exception:
        pass

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8500
    local_url = f"http://localhost:{port}"
    network_url = f"http://192.168.1.7:{port}"
    
    print("\n" + "=" * 60)
    print("ENG / MOHAMED DABAH - 3D AI PORTFOLIO SERVER")
    print("=" * 60)
    print(f"Local URL:   {local_url}")
    print(f"Network URL: {network_url} (Open from your mobile!)")
    print("Three.js 3D Engine and Dynamic QR Codes Active")
    print("=" * 60 + "\n")
    
    threading.Thread(target=open_browser, args=(local_url,), daemon=True).start()
    
    try:
        from portfolio.app.main import app
        uvicorn.run(app, host=host, port=port)
    except Exception:
        from app.main import app
        uvicorn.run(app, host=host, port=port)
