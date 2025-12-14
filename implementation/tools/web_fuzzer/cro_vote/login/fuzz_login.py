import requests
import random
import urllib3
import os
import datetime

TARGET_URL = "https://localhost:8000"  
LOGIN_ENDPOINT = "/api/login"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FUZZ_LIST_PATH = os.path.join(SCRIPT_DIR, "fuzz_list.txt")

VALID_OIB = "74597874674" 
VALID_PASS = "marin123"

LOG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR))))), 
    "results", 
    "logs", 
    "cro-vote-app", 
    "login_fuzz.txt"
)

def log_fuzz_result(message, details=""):
    """Zapisuje rezultate fuzzinga (status != 200/201) u datoteku."""
    try:
        log_dir = os.path.dirname(LOG_FILE_PATH)
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(LOG_FILE_PATH, 'a', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write(f"VRIJEME: {timestamp}\n")
            f.write(f"REZULTAT: {message}\n")
            f.write(f"DETALJI:\n{details}\n")
            f.write("=" * 60 + "\n\n")
            
        print(f"!!! LOGIRANO: {message} -> {LOG_FILE_PATH}")

    except Exception as e:
        print(f"!!! GREŠKA pri logiranju rezultata: {e}")


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

def load_fuzz_payloads(filepath):
    """Učitava zlonamjerne payloadove iz datoteke."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"!!! GREŠKA: Fuzz lista nije pronađena na putanji: {filepath}")
        return []

def fuzz_login():
    """Fuzza OIB i lozinku na /api/login endpointu."""
    payloads = load_fuzz_payloads(FUZZ_LIST_PATH)
    if not payloads:
        return

    print(f"[*] Pokreće se fuzzing POST {TARGET_URL}{LOGIN_ENDPOINT} (HTTPS) sa {len(payloads)} payloadova.")
    
    fuzz_targets = {
        'oib': VALID_OIB,
        'password': VALID_PASS
    }

    for target_field, default_value in fuzz_targets.items():
        print(f"\n--- Fuzzing polja: {target_field} ---")
        
        for payload in payloads:
            
            data_to_send = {
                "oib": VALID_OIB,
                "password": VALID_PASS,
                "recaptcha_token": "fuzzed_token"
            }
            
            data_to_send[target_field] = payload 
            
            try:
                response = requests.post(
                    f"{TARGET_URL}{LOGIN_ENDPOINT}",
                    data=data_to_send,
                    verify=False,
                    timeout=5
                )

                if response.status_code >= 500:
                    message = f"KRITIČNA GREŠKA (Status: {response.status_code})"
                    details = f"Polje: {target_field}\nPayload: {payload}\nOdgovor: {response.text[:1000]}"
                    log_fuzz_result(message, details)
                    print(f"!!! {message} kod {target_field} s payloadom: {payload[:30]}...")
                
                elif response.status_code not in (200, 201):
                    
                    message_type = "ZANIMLJIV STATUS" if response.status_code not in (400, 401, 403) else "OČEKIVANA GREŠKA (za analizu)"
                    
                    if "Invalid token" in response.text and response.status_code == 400:
                        pass
                    else:
                        message = f"{message_type} (Status: {response.status_code})"
                        details = f"Polje: {target_field}\nPayload: {payload}\nOdgovor: {response.text[:1000]}"
                        log_fuzz_result(message, details)
                        print(f"!!! {message_type} (Status: {response.status_code}) kod {target_field} s payloadom: {payload[:30]}...")


            except requests.exceptions.ConnectionError:
                message = "SERVER PAO: Greška u konekciji"
                details = f"Polje: {target_field}\nPayload: {payload}\nServer je prestao odgovarati."
                log_fuzz_result(message, details)
                print(f"!!! {message} kod {target_field} s payloadom: {payload[:30]}...")
                return
            except requests.exceptions.RequestException:
                pass

if __name__ == "__main__":
    fuzz_login()