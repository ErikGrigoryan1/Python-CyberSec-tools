#!/usr/bin/python3
import requests

target_url = input('[*] Enter Target URL (include http:// or https://): ').rstrip('/')
file_name = input('[*] Enter Name Of The File Containing Directories: ')

def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.RequestException:
        return None

with open(file_name, 'r') as file:
    for line in file:
        directory = line.strip()
        full_url = f"{target_url}/{directory}"
        response = request(full_url)
        if response and response.status_code == 200:
            print(f'[*] Discovered Directory At This Path: {full_url}')
