#!/usr/bin/python
import os
import platform
import time
import threading
import socket

from datetime import datetime
from queue import Queue
def ping_check():
   net = input("Enter the Network Address: ")
   net1= net.split('.')
   a = '.'

   net2 = net1[0] + a + net1[1] + a + net1[2] + a
   st1 = int(input("Enter the Starting Number: "))
   en1 = int(input("Enter the Last Number: "))
   en1 = en1 + 1
   oper = platform.system()

   if (oper == "Windows"):
      ping1 = "ping -n 1 "
   else :
      ping1 = "ping -c 1 "
   t1 = datetime.now()
   print ("Scanning in Progress:")

   for ip in range(st1,en1):
       addr = net2 + str(ip)
       comm = ping1 + addr
       response = os.popen(comm)
      
       for line in response.readlines():
           if "ttl" in line.lower():
               print(addr, "--> Live")
               break


   t2 = datetime.now()
   total = t2 - t1
   print ("Scanning completed in: ",total)





def start_scan():
    socket.setdefaulttimeout(0.5)
    print_lock = threading.Lock()

    target = input('Enter the host to be scanned: ')
    t_IP = socket.gethostbyname(target)
    print('Starting scan on host:', t_IP)

    def portscan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            s.connect((t_IP, port))
            
            # Try to grab banner
            try:
                banner = s.recv(1024).decode().strip()
                if not banner:
                    banner = "No banner"
            except:
                banner = "No banner"

            # Try to identify service by port
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

    for worker in range(1, 500):
        q.put(worker)

    q.join()
    print('Time taken:', time.time() - startTime)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "ping":
        ping_check()
    elif len(sys.argv) > 1 and sys.argv[1] == "scan":
        start_scan()
    else:
        print("Usage:")
        print("  python3 functions.py ping   # to do ping scan")
        print("  python3 functions.py scan   # to do port scan")
