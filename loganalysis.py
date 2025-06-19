#!/usr/bin/python

import re
import sys
from collections import Counter

def analyze_log(log_path):
    ip_pattern = r"Failed password.*from (\d+\.\d+\.\d+\.\d+)"
    ips = []

    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            match = re.search(ip_pattern, line)
            if match:
                ips.append(match.group(1))

    count = Counter(ips)
    print("Top IPs with failed SSH login attempts:")
    for ip, num in count.most_common(10):
        print(f"{ip}: {num} times")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 log_analyzer.py <log_file_path>")
        sys.exit(1)

    analyze_log(sys.argv[1])
