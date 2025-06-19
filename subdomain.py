#!/usr/bin/python

import requests
import sys

subList = open("wordlists/subdomains-1000.txt").read()
subs= subList.splitlines()

for sub in subs: 
	checkingUrl = f"http://{sub}.{sys.argv[1]}"

	try:
		requests.get(checkingUrl)

	except requests.ConnectionError:
		pass

	else: 
		print(f"Valid URL ` {checkingUrl}")