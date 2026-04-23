#!/usr/bin/env python3
"""
Primspace Model - Deep Analysis of Twin Prime Pattern and Multi-layer Prediction
"""

import numpy as np
from typing import List, Tuple

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def get_primes(k: int):
    primes = []
    n = 2
    while len(primes) < k:
        if is_prime(n):
            primes.append(n)
        n += 1
    return primes

def compute_mod_k(n: int, primes):
    return tuple(n % p for p in primes)

def compute_alpha_k(n: int, primes):
    k = len(primes)
    residues = [n % p for p in primes]
    normalized = [r / (p - 1) for r, p in zip(residues, primes)]
    return sum(normalized) / k

def compute_kapv_greedy(n: int, max_prime: int = 200):
    if n == 1:
        return [1]
    
    primes = [p for p in range(2, max_prime + 1) if is_prime(p)]
    result = []
    remaining = n
    
    while remaining > 0:
        found = False
        for p in reversed(primes):
            if p <= remaining:
                result.append(p)
                remaining -= p
                found = True
                break
        if not found:
            result.append(1)
            remaining -= 1
    
    result.sort()
    return result

def has_zero_modulo(n: int, primes) -> bool:
    """Check if Mod_k(n) contains any zero."""
    return any(n % p == 0 for p in primes)

def analyze_twin_prime_pattern(n_max=200, k=4):
    """
    Detailed analysis of twin prime gap pattern.
    """
    print("=" * 80)
    print("TWIN PRIME PATTERN ANALYSIS")
    print("=" * 80)
    print()
    
    primes = get_primes(k)
    print(f"Using k={k} primes: {primes}")
    print()
    
    # Find twin primes
    twin_primes = []
    for n in range(2, n_max):
        if is_prime(n) and is_prime(n + 2):
            twin_primes.append((n, n + 2))
    
    print(f"Found {len(twin_primes)} twin prime pairs in [2, {n_max})")
    print()
    
    # Analyze pattern
    print("Twin Prime Gap Pattern Analysis:")
    print("-" * 80)
    print(f"{'Pair':<15} {'α(p₁)':<10} {'α(gap)':<10} {'α(p₂)':<10} {'Drop₁':<10} {'Drop₂':<10} {'Gap/Avg':<10}")
    print("-" * 80)
    
    gap_drops_1 = []
    gap_drops_2 = []
    gap_relative = []
    
    for p1, p2 in twin_primes:
        gap = p1 + 1
        
        alpha_p1 = compute_alpha_k(p1, primes)
        alpha_gap = compute_alpha_k(gap, primes)
        alpha_p2 = compute_alpha_k(p2, primes)
        
        drop1 = alpha_p1 - alpha_gap
        drop2 = alpha_p2 - alpha_gap
        avg_prime_alpha = (alpha_p1 + alpha_p2) / 2
        gap_ratio = alpha_gap / avg_prime_alpha if avg_prime_alpha > 0 else 0
        
        gap_drops_1.append(drop1)
        gap_drops_2.append(drop2)
        gap_relative.append(gap_ratio)
        
        print(f"({p1:3d}, {p2:3d})   {alpha_p1:.4f}    {alpha_gap:.4f}    {alpha_p2:.4f}    "
              f"{drop1:+.4f}    {drop2:+.4f}    {gap_ratio:.4f}")
    
    print("-" * 80)
    print()
    
    # Statistics
    print("Gap Drop Statistics:")
    print(f"  Mean drop from p₁: {np.mean(gap_drops_1):.4f} ± {np.std(gap_drops_1):.4f}")
    print(f"  Mean drop from p₂: {np.mean(gap_drops_2):.4f} ± {np.std(gap_drops_2):.4f}")
    print(f"  Min drop: {min(min(gap_drops_1), min(gap_drops_2)):.4f}")
    print(f"  Max drop: {max(max(gap_drops_1), max(gap_drops_2)):.4f}")
    print(f"  Gap/Average ratio: {np.mean(gap_relative):.4f} ± {np.std(gap_relative):.4f}")
    print()
    
    # WHY does this happen?
    print("EXPLANATION: Why does α_k drop at twin prime gaps?")
    print("-" * 80)
    print("For twin primes (p, p+2):")
    print("  • p and p+2 are both odd → p+1 is EVEN → divisible by 2")
    print("  • If p ≡ 1 (mod 3), then p+2 ≡ 0 (mod 3) OR vice versa")
    print("  • The gap (p+1) typically has MORE zero modulo components")
    print("  • This LOWERS α_k(p+1) systematically")
    print()
    
    # Verify this
    zero_counts = []
    for p1, p2 in twin_primes:
        gap = p1 + 1
        mod_gap = compute_mod_k(gap, primes)
        zero_count = sum(1 for r in mod_gap if r == 0)
        zero_counts.append(zero_count)
    
    print(f"Zero modulo components in gaps:")
    print(f"  Mean: {np.mean(zero_counts):.2f}")
    print(f"  Min: {min(zero_counts)}")
    print(f"  Max: {max(zero_counts)}")
    print()
    
    return twin_primes, gap_drops_1, gap_drops_2

def multi_layer_prediction(n_max=100, k=4):
    """
    Test multi-layer prediction accuracy.
    Combine all three layers: Mod_k, K-APV, α_k
    """
    print("=" * 80)
    print("MULTI-LAYER PREDICTION ANALYSIS")
    print("=" * 80)
    print()
    
    primes = get_primes(k)
    print(f"Using k={k} primes: {primes}")
    print(f"Testing on n ∈ [2, {n_max}]")
    print()
    
    # Collect data
    results = {
        'alpha_only': {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0},
        'mod_only': {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0},
        'kapv_only': {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0},
        'alpha_and_mod': {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0},
        'all_three': {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0},
    }
    
    for n in range(2, n_max + 1):
        is_p = is_prime(n)
        
        # Layer 1: Alpha threshold
        alpha = compute_alpha_k(n, primes)
        pred_alpha = alpha > 0.6
        
        # Layer 2: Modular (no zeros)
        has_zero = has_zero_modulo(n, primes)
        pred_mod = not has_zero
        
        # Layer 3: K-APV cardinality = 1
        kapv = compute_kapv_greedy(n)
        pred_kapv = len(kapv) == 1
        
        # Combined predictions
        pred_alpha_and_mod = pred_alpha and pred_mod
        pred_all_three = pred_alpha and pred_mod and pred_kapv
        
        # Update confusion matrices
        def update_conf(pred, actual, results_dict):
            if pred and actual:
                results_dict['TP'] += 1
            elif not pred and not actual:
                results_dict['TN'] += 1
            elif pred and not actual:
                results_dict['FP'] += 1
            else:  # not pred and actual
                results_dict['FN'] += 1
        
        update_conf(pred_alpha, is_p, results['alpha_only'])
        update_conf(pred_mod, is_p, results['mod_only'])
        update_conf(pred_kapv, is_p, results['kapv_only'])
        update_conf(pred_alpha_and_mod, is_p, results['alpha_and_mod'])
        update_conf(pred_all_three, is_p, results['all_three'])
    
    # Calculate metrics
    print("Prediction Performance:")
    print("-" * 80)
    print(f"{'Method':<20} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1':<12}")
    print("-" * 80)
    
    for method, conf in results.items():
        tp, tn, fp, fn = conf['TP'], conf['TN'], conf['FP'], conf['FN']
        
        accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"{method:<20} {accuracy:>10.1%}  {precision:>10.1%}  {recall:>10.1%}  {f1:>10.3f}")
    
    print("-" * 80)
    print()
    
    # Detailed breakdown
    print("Key Insight:")
    print("-" * 80)
    
    # Find false positives and false negatives for "all_three"
    false_positives = []
    false_negatives = []
    
    for n in range(2, n_max + 1):
        is_p = is_prime(n)
        alpha = compute_alpha_k(n, primes)
        has_zero = has_zero_modulo(n, primes)
        kapv = compute_kapv_greedy(n)
        
        pred_all = (alpha > 0.6) and (not has_zero) and (len(kapv) == 1)
        
        if pred_all and not is_p:
            false_positives.append((n, alpha, kapv))
        if not pred_all and is_p:
            false_negatives.append((n, alpha, kapv))
    
    print(f"False Positives (predicted prime, but composite): {len(false_positives)}")
    if false_positives:
        print("  Examples:")
        for n, alpha, kapv in false_positives[:5]:
            print(f"    n={n}: α_k={alpha:.3f}, K-APV={kapv}")
    print()
    
    print(f"False Negatives (predicted composite, but prime): {len(false_negatives)}")
    if false_negatives:
        print("  Examples:")
        for n, alpha, kapv in false_negatives[:5]:
            print(f"    n={n}: α_k={alpha:.3f}, K-APV={kapv}")
    print()
    
    return results

def combined_score_analysis(n_max=100, k=4):
    """
    Create a weighted combined score from all layers.
    """
    print("=" * 80)
    print("COMBINED SCORING SYSTEM")
    print("=" * 80)
    print()
    
    primes = get_primes(k)
    print(f"Weighted scoring: S(n) = w₁·α_k(n) + w₂·(1-has_zero) + w₃·(1/|K-APV|)")
    print()
    
    # Try different weight combinations
    weight_sets = [
        (1.0, 0.5, 0.5),   # Alpha dominant
        (0.5, 1.0, 0.5),   # Modular dominant
        (0.5, 0.5, 1.0),   # K-APV dominant
        (1.0, 1.0, 1.0),   # Equal weights
        (2.0, 1.5, 1.0),   # Optimized (guess)
    ]
    
    best_accuracy = 0
    best_weights = None
    best_threshold = None
    
    print(f"{'Weights (α,mod,K-APV)':<30} {'Best Threshold':<18} {'Accuracy':<12}")
    print("-" * 80)
    
    for w1, w2, w3 in weight_sets:
        scores_prime = []
        scores_composite = []
        
        for n in range(2, n_max + 1):
            alpha = compute_alpha_k(n, primes)
            has_zero = has_zero_modulo(n, primes)
            kapv_card = len(compute_kapv_greedy(n))
            
            score = w1 * alpha + w2 * (1 if not has_zero else 0) + w3 * (1.0 / kapv_card)
            
            if is_prime(n):
                scores_prime.append(score)
            else:
                scores_composite.append(score)
        
        # Find optimal threshold
        thresholds = np.linspace(0, max(scores_prime + scores_composite), 100)
        accuracies = []
        
        for thresh in thresholds:
            correct = sum(1 for s in scores_prime if s > thresh) + sum(1 for s in scores_composite if s <= thresh)
            accuracy = correct / (len(scores_prime) + len(scores_composite))
            accuracies.append(accuracy)
        
        best_idx = np.argmax(accuracies)
        best_acc = accuracies[best_idx]
        best_thr = thresholds[best_idx]
        
        print(f"({w1:.1f}, {w2:.1f}, {w3:.1f})             {best_thr:>12.3f}      {best_acc:>10.1%}")
        
        if best_acc > best_accuracy:
            best_accuracy = best_acc
            best_weights = (w1, w2, w3)
            best_threshold = best_thr
    
    print("-" * 80)
    print()
    print(f"BEST CONFIGURATION:")
    print(f"  Weights: α={best_weights[0]:.1f}, mod={best_weights[1]:.1f}, K-APV={best_weights[2]:.1f}")
    print(f"  Threshold: {best_threshold:.3f}")
    print(f"  Accuracy: {best_accuracy:.1%}")
    print()
    
    return best_weights, best_threshold, best_accuracy

if __name__ == "__main__":
    # Analysis 1: Twin prime pattern
    analyze_twin_prime_pattern(n_max=200, k=4)
    print("\n" * 2)
    
    # Analysis 2: Multi-layer prediction
    multi_layer_prediction(n_max=100, k=4)
    print("\n" * 2)
    
    # Analysis 3: Combined scoring
    combined_score_analysis(n_max=100, k=4)
    
    print("=" * 80)
    print("Analysis completed.")
    print("=" * 80)
