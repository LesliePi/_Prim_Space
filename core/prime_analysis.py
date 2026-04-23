# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 01:56:57 2026

@author: Laszlo
"""

import sys

def read_primes(filename):
    """Beolvassa a prímszámokat a fájlból."""
    primes = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                primes.append(int(line))
    return primes

def analyze(primes, max_limit):
    """Elemzi a prímeket a megadott határig."""
    primes_in_range = [p for p in primes if p <= max_limit]
    count = len(primes_in_range)
    if count == 0:
        return count, 0, 0.0, 0
    # Prímhézagok
    gaps = [primes_in_range[i] - primes_in_range[i-1] for i in range(1, count)]
    max_gap = max(gaps) if gaps else 0
    avg_gap = sum(gaps) / len(gaps) if gaps else 0.0
    # Ikerprímek
    twin_count = 0
    for i in range(count - 1):
        if primes_in_range[i] + 2 == primes_in_range[i+1]:
            twin_count += 1
    return count, max_gap, avg_gap, twin_count

def main():
    if len(sys.argv) < 2:
        print("Használat: python prime_analysis.py <fájlnév>")
        sys.exit(1)
    filename = sys.argv[1]
    primes = read_primes(filename)
    print(f"A fájlban {len(primes)} prímszám található.")
    if primes:
        print(f"A legkisebb prím: {primes[0]}")
        print(f"A legnagyobb prím: {primes[-1]}")
    # Elméleti prímszámok a tartományokban
    theoretical_counts = {
        10000: 1229,
        100000: 9592,
        1000000: 78498
    }
    limits = [10000, 100000, 1000000]
    for limit in limits:
        print(f"\n--- Tartomány: 1 – {limit} ---")
        count, max_gap, avg_gap, twin_count = analyze(primes, limit)
        print(f"Prímek száma a fájlban: {count}")
        if count > 0:
            print(f"Legnagyobb prímhézag: {max_gap}")
            print(f"Átlagos prímhézag: {avg_gap:.2f}")
            print(f"Ikerprímek száma: {twin_count}")
        theoretical = theoretical_counts[limit]
        print(f"Elvárható prímek száma (elméleti): {theoretical}")
        if count < theoretical:
            print(f"Hiányzó prímek: {theoretical - count}")
        elif count > theoretical:
            print(f"Többlet prímek: {count - theoretical}")

if __name__ == "__main__":
    main()