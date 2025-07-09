#!/usr/bin/env python3
import os
import platform
import time
import threading
import socket
import sys

from datetime import datetime
from queue import Queue

def ping_check():
    net = input("Enter the Network Address (e.g., 192.168.1.0): ")
    net1 = net.split('.')
    if len(net1) != 4:
        print("Invalid network address.")
        return

    net2 = f"{net1[0]}.{net1[1]}.{net1[2]}."
    try:
        st1 = int(input("Enter the Starting Number (e.g., 1): "))
        en1 = int(input("Enter the Last Number (e.g., 254): "))
    except ValueError:
        print("Invalid input range.")
        return

    en1 += 1
    oper = platform.system()
    ping1 = "ping -n 1 " if oper == "Windows" else "ping -c 1 "

    t1 = datetime.now()
    print("Scanning in Progress...")

    for ip in range(st1, en1):
        addr = net2 + str(ip)
        comm = ping1 + addr
        response = os.popen(comm)

        for line in response.readlines():
            if "ttl" in line.lower():
                print(addr, "--> Live")
                break

    t2 = datetime.now()
    total = t2 - t1
    print("Scanning completed in:", total)


def start_scan():
    socket.setdefaulttimeout(0.5)
    print_lock = threading.Lock()

    target = input('Enter the host to be scanned: ')
    try:
        t_IP = socket.gethostbyname(target)
    except socket.gaierror:
        print("Invalid host.")
        return

    print('Starting scan on host:', t_IP)

    def portscan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect((t_IP, port))

            banner = ""
            # Send minimal probes for some common ports to get version info
            try:
                if port in [80, 8080]:
                    s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                    banner = s.recv(1024).decode(errors="ignore").strip()
                elif port == 21:  # FTP usually sends banner first
                    banner = s.recv(1024).decode(errors="ignore").strip()
                elif port == 22:  # SSH usually sends banner first
                    banner = s.recv(1024).decode(errors="ignore").strip()
                elif port == 25:  # SMTP usually sends banner first
                    banner = s.recv(1024).decode(errors="ignore").strip()
                else:
                    # For other ports, just try to recv data if sent
                    s.settimeout(0.5)
                    banner = s.recv(1024).decode(errors="ignore").strip()
            except:
                banner = "No banner"

            if not banner:
                banner = "No banner"

            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"

            with print_lock:
                print(f"{port} is open | Service: {service} | Banner: {banner}")

            s.close()
        except:
            pass

    def threader():
        while True:
            worker = q.get()
            portscan(worker)
            q.task_done()

    q = Queue()
    startTime = time.time()

    for x in range(100):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    for worker in range(1, 1025):  # scanning ports 1 to 1024
        q.put(worker)

    q.join()
    print('Time taken:', round(time.time() - startTime, 2), "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "ping":
        ping_check()
    elif len(sys.argv) > 1 and sys.argv[1] == "scan":
        start_scan()
    else:
        print("Usage:")
        print("  python3 netscaner.py ping   # to do ping sweep")
        print("  python3 netscaner.py scan   # to do port scan")
