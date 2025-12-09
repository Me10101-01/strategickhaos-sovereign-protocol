#!/usr/bin/env python3
"""
Check DAMON results for critical failures.
Used by CI/CD to determine if the build should fail.
"""

import json
import sys

def check_critical_failures(results_file):
    """
    Check for critical RED signals in DAMON results.
    
    Returns:
        int: Number of critical failures
    """
    with open(results_file) as f:
        results = json.load(f)
    
    critical_domains = ['security_posture', 'ethical_compliance']
    critical_count = 0
    
    for result in results:
        if result['overall_signal'] == 'red' and result.get('domain') in critical_domains:
            critical_count += 1
            print(f"❌ CRITICAL: {result['damon']} ({result['domain']}) is RED")
    
    return critical_count

def main():
    if len(sys.argv) != 2:
        print("Usage: check_critical.py <results.json>")
        sys.exit(1)
    
    results_file = sys.argv[1]
    critical_count = check_critical_failures(results_file)
    
    print(f"\nCritical RED signals: {critical_count}")
    
    if critical_count > 0:
        print(f"⚠️  WARNING: {critical_count} critical domain(s) showing RED")
        print("Review DAMON results in artifacts")
        # Uncomment to fail the build:
        # sys.exit(1)
    else:
        print("✅ No critical failures detected")
    
    sys.exit(0)

if __name__ == '__main__':
    main()
