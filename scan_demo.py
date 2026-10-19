#!/usr/bin/env python3
"""
Arek Scan Suite — DEMO (legalna wersja edukacyjna)

Skaner portów + analiza, ograniczony do WŁASNYCH sieci/hosta.
Demo pokazuje wzorzec: wywołanie masscan, parsowanie wyników, raport.
Działa tylko na: localhost, Twoje IP (automatycznie) lub z --target i potwierdzeniem.

Przykład:
  python3 scan_demo.py                     # skanuje localhost + własne IP
  python3 scan_demo.py --target 192.168.1.1   # wymaga potwierdzenia, że to Twoje
"""
import argparse
import os
import subprocess
import sys
from datetime import datetime

PORTS = "22,80,443,3389,8080"
OUTPUT_DIR = "reports"


import ipaddress

def is_local(ip: str) -> bool:
    if ip in ("localhost", "127.0.0.1", "::1"):
        return True
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return (addr.is_loopback or addr.is_private or addr.is_link_local
            or str(addr).startswith("100.64."))


def own_ip() -> str:
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.100.1", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def confirm(target: str) -> bool:
    print(f"\n[Cel] {target}")
    print("[!] To narzędzie wolno używać WYŁĄCZNIE na własnym sprzęcie / własnej sieci.")
    print("    Skanowanie cudzych systemów bez zgody jest nielegalne.\n")
    try:
        ans = input("Czy to Twoje urządzenie/należysz do sieci? Potwierdź 'tak': ").strip().lower()
    except EOFError:
        sys.exit("Anulowano (brak potwierdzenia).")
    return ans == "tak"


def run_masscan(target: str) -> str:
    out = os.path.join(OUTPUT_DIR, f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    try:
        cmd = ["sudo", "masscan", "-p", PORTS, target, "--rate", "1000", "-oL", out]
        print(f"[+] masscan: {' '.join(cmd)}")
        subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL)
    except FileNotFoundError:
        print("[!] masscan nie jest zainstalowany. Zainstaluj: sudo apt install masscan")
        sys.exit(1)
    return out


def report(out: str) -> None:
    print("\n=== OTWARTE PORTY / USŁUGI ===")
    found = 0
    if not os.path.exists(out):
        print("(brak wyników)")
        return
    with open(out) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 4:
                proto, ip, port, status = parts[0], parts[1], parts[2], parts[3]
                if status == "open":
                    found += 1
                    print(f"  {ip}:{port} [{proto}]")
    if found == 0:
        print("  brak otwartych portów.")
    print(f"\nRaport zapisany: {out}")


def main():
    parser = argparse.ArgumentParser(description="Demo skaner — tylko własne sieci")
    parser.add_argument("--target", default="localhost")
    args = parser.parse_args()

    targets = [args.target]
    if args.target == "localhost":
        own = own_ip()
        targets = [args.target, own]
        print(f"[+] Wykryto własne IP: {own}")

    for t in targets:
        if not is_local(t):
            print(f"[!] Cel '{t}' nie jest siecią lokalną. Demo blokuje skanowanie zewnętrznych adresów.")
            sys.exit(1)
        if not confirm(t):
            sys.exit("Anulowano.")

    print(f"\n[+] Skanuję {len(targets)} cel(e)…")
    for t in targets:
        out = run_masscan(t)
        report(out)


if __name__ == "__main__":
    main()