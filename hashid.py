#!/usr/bin/python

import re
import sys

def identify_hash(hash_string):
    hash_patterns = {
        "MD5": r"^[a-fA-F0-9]{32}$",
        "SHA1": r"^[a-fA-F0-9]{40}$",
        "SHA256": r"^[a-fA-F0-9]{64}$",
        "bcrypt": r"^\$2[aby]?\$[0-9]{2}\$[./A-Za-z0-9]{53}$",
        "NTLM": r"^[A-F0-9]{32}$",
    }

    for hash_type, pattern in hash_patterns.items():
        if re.match(pattern, hash_string):
            return hash_type
    return "Unknown"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 hash_identifier.py <hash>")
        sys.exit(1)

    hash_input = sys.argv[1]
    print(f"Identified type: {identify_hash(hash_input)}")
