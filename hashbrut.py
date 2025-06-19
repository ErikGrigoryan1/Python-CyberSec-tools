#!/usr/bin/python

import hashlib
import sys

def crack_hash(hash_value, wordlist_path):
    hash_length = len(hash_value)

    if hash_length == 32:
        algo = hashlib.md5
    elif hash_length == 40:
        algo = hashlib.sha1
    elif hash_length == 64:
        algo = hashlib.sha256
    else:
        print("Unsupported hash length.")
        return

    with open(wordlist_path, 'r') as f:
        for word in f:
            word = word.strip()
            if algo(word.encode()).hexdigest() == hash_value:
                print(f"[+] Hash cracked! Plaintext: {word}")
                return

    print("[-] Hash not found in wordlist.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 hash_cracker.py <hash> <wordlist>")
        sys.exit(1)

    crack_hash(sys.argv[1], sys.argv[2])
