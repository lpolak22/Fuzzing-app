import requests
import urllib3
import os
import datetime
import re
import json

TARGET_URL = "https://localhost:8000"  
ENDPOINT = "/api/posts/new-post" 

RAW_AUTH_TOKEN = "Bearer [VAŠ_VALIDAN_JWT_TOKEN]" 

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FUZZ_LIST_PATH = os.path.join(SCRIPT_DIR, "fuzz_list.txt")

LOG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR))))), 
    "results", 
    "logs", 
    "cro-vote-app", 
    "admin_post_fuzz.txt"
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

def clean_payload_ascii(text):
    if isinstance(text, str):
        return re.sub(r'[^\x00-\x7F]+', '', text)
    return text

def fuzz_new_post():
    payloads = load_fuzz_payloads(FUZZ_LIST_PATH)
    if not payloads:
        return
    
    AUTH_TOKEN = clean_payload_ascii(RAW_AUTH_TOKEN)
    
    headers = {
        'Authorization': AUTH_TOKEN,
        'Content-Type': 'application/json; charset=utf-8' 
    }

    print(f"[*] Pokreće se fuzzing POST {TARGET_URL}{ENDPOINT} sa {len(payloads)} payloadova.")
    
    for payload in payloads:
        
        cleaned_payload = clean_payload_ascii(payload)
        
        data_to_send = {
            "name": cleaned_payload,
            "description": "Valid Description",
        }
        
        try:
            json_string = json.dumps(data_to_send, ensure_ascii=False)
        except TypeError as e:
            message = f"GREŠKA KODIRANJA (JSON dumps): {e}"
            log_fuzz_result(message, details=f"Payload: {payload}")
            continue

        try:
            response = requests.post(
                f"{TARGET_URL}{ENDPOINT}",
                data=json_string.encode('utf-8'),
                headers=headers,
                verify=False,
                timeout=5
            )

            if response.status_code == 200 or response.status_code == 201:
                message = f"KRITIČNA GREŠKA: USPJEŠAN UPIS (Status: {response.status_code})"
                details = f"Polje: name\nPayload: {payload}\nProvjerite BAC! (Broken Access Control)"
                log_fuzz_result(message, details)
                print(f"!!! {message} s payloadom: {payload[:30]}...")

            elif response.status_code >= 500:
                message = f"KRITIČNA GREŠKA (Status: {response.status_code})"
                details = f"Polje: name\nPayload: {payload}\nServer je pao."
                log_fuzz_result(message, details)
                print(f"!!! {message} s payloadom: {payload[:30]}...")

            elif response.status_code not in (401, 403, 400):
                 message = f"ZANIMLJIV STATUS (Status: {response.status_code})"
                 details = f"Polje: name\nPayload: {payload}\nOdgovor: {response.text[:1000]}"
                 log_fuzz_result(message, details)
                 print(f"!!! {message} s payloadom: {payload[:30]}...")

        except requests.exceptions.ConnectionError:
            message = "SERVER PAO: Greška u konekciji"
            log_fuzz_result(message, details=f"Payload: {payload}")
            return
        except requests.exceptions.RequestException as e:
            if "UnicodeEncodeError" in str(e):
                 message = f"GREŠKA KODIRANJA (Token/Headers): {e}"
                 log_fuzz_result(message, details=f"Originalni Payload: {payload}. Auth Token: {RAW_AUTH_TOKEN}")
            pass

if __name__ == "__main__":
    fuzz_new_post()