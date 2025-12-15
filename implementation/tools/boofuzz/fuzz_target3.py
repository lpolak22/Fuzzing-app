import socket
import time
import sys
import random

TARGET_IP = "127.0.0.1"
TARGET_PORT = 9999

PROTOCOL_MAGIC = b"CMD:"
FUZZ_KEYWORD = b"FUZZ"

def create_fuzzed_payload(length):
    """
    Generira payload koji slijedi gramatiku protokola, 
    a zatim stvara ulaz za Buffer Overflow.
    Gramatika: CMD:FUZZ[junk][overflow_payload]
    """
    
    fixed_header = PROTOCOL_MAGIC + FUZZ_KEYWORD 
    
    padding_to_offset_10 = b"XX"
    
    payload_len = length
    
    overflow_payload = b"A" * payload_len
        
    full_payload = fixed_header + padding_to_offset_10 + overflow_payload
    return full_payload

def fuzz_tcp_connection():
    print("Starting Grammar/Generation Fuzzer (Buffer Overflow Test)...")
    
    test_lengths = [15, 16, 24, 64, 128] 
    
    for i, payload_len in enumerate(test_lengths):
        
        payload = create_fuzzed_payload(payload_len)
        
        total_len = len(payload)
        
        if total_len <= 30:
            print(f"[{i+1}/{len(test_lengths)}] Preskakanje: Totalna duljina ({total_len}) je prekratka za ulazak u tajnu putanju.")
            continue
            
        print(f"\n[{i+1}/{len(test_lengths)}] Testiranje duljine B.O. payloada: {payload_len} (Ukupna duljina: {total_len})")
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((TARGET_IP, TARGET_PORT))
            
            s.sendall(payload)
            
            time.sleep(0.5)
            s.close()
            
            s_check = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_check.settimeout(1)
            s_check.connect((TARGET_IP, TARGET_PORT))
            s_check.close()
            
            print("Status: Server je preživio.")
            
        except ConnectionRefusedError:
            print("!!! CRITICAL: Server srušen (Connection Refused). Payload je bio uspješan!")
            print(f"Uspješan Payload (duljina B.O. dijela): {payload_len} bajtova.")
            return

        except socket.timeout:
            print("Status: Timeout pri komunikaciji.")
            
        except Exception as e:
            print(f"Došlo je do nepoznate greške: {e}")
            
if __name__ == "__main__":
    fuzz_tcp_connection()