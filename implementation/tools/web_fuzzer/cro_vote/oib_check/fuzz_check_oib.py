import requests
import urllib3
import os
import datetime

TARGET_URL = "https://localhost:8000"  
ENDPOINT = "/api/check-existing-oib"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FUZZ_LIST_PATH = os.path.join(SCRIPT_DIR, "fuzz_list.txt")

LOG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR))))), 
    "results", 
    "logs", 
    "cro-vote-app", 
    "check_oib_fuzz.txt"
)

def log_fuzz_result(message, details=""):
    try:
        log_dir = os.path.dirname(LOG_FILE_PATH)
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE_PATH, 'a', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write(f"VRIJEME: {timestamp}\nREZULTAT: {message}\nDETALJI:\n{details}\n")
            f.write("=" * 60 + "\n\n")
        print(f"!!! LOGIRANO: {message} -> {LOG_FILE_PATH}")
    except Exception as e:
        print(f"!!! GREŠKA pri logiranju rezultata: {e}")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

def load_fuzz_payloads(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"!!! GREŠKA: Fuzz lista nije pronađena na putanji: {filepath}")
        return []

def fuzz_oib_check():
    payloads = load_fuzz_payloads(FUZZ_LIST_PATH)
    if not payloads:
        return

    print(f"[*] Pokreće se fuzzing POST {TARGET_URL}{ENDPOINT} sa {len(payloads)} payloadova.")
    
    for payload in payloads:
        data_to_send = {"oib": payload}
        
        try:
            response = requests.post(
                f"{TARGET_URL}{ENDPOINT}",
                json=data_to_send,
                verify=False,
                timeout=5
            )

            if response.status_code >= 500:
                message = f"KRITIČNA GREŠKA (Status: {response.status_code})"
                details = f"Payload: {payload}\nOdgovor: {response.text[:1000]}"
                log_fuzz_result(message, details)
                print(f"!!! {message} s payloadom: {payload[:30]}...")
            
            elif response.status_code not in (200, 201, 400):
                message = f"ZANIMLJIV STATUS (Status: {response.status_code})"
                details = f"Payload: {payload}\nOdgovor: {response.text[:1000]}"
                log_fuzz_result(message, details)
                print(f"!!! {message} s payloadom: {payload[:30]}...")


        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.ConnectionError):
                message = "SERVER PAO: Greška u konekciji"
                details = f"Payload: {payload}\nServer je prestao odgovarati."
                log_fuzz_result(message, details)
                return
            pass

if __name__ == "__main__":
    fuzz_oib_check()