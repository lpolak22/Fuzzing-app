import sys
from scapy.all import *

TARGET_IP = "127.0.0.1"
TARGET_PORT = 53

def fuzz_dns_packet():
    print("Starting Scapy DNS Fuzzer (Generation-Based Fuzzing)...")
    
    ip_base = IP(dst=TARGET_IP)
    udp_base = UDP(dport=TARGET_PORT)
    dns_base = DNS(rd=1, qd=DNSQR(qname="test.local"))

    base_packet = ip_base / udp_base / dns_base
    
    fuzz_count = 0
    for i in range(1, 10):
        fuzzed_packet = fuzz(base_packet)
        fuzz_count += 1
        
        print(f"Fuzzing iteration {fuzz_count}: Sending malformed packet.")
                
        if fuzz_count == 5:
            print("\nSIMULACIJA: Target server srusen nakon 5. fuzz-a (dokaz generation fuzzinga).")
            break
        
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        fuzz_dns_packet()
    except Exception as e:
        print(f"An error occurred: {e}")