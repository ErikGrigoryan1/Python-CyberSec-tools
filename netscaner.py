#!/usr/bin/python
import sys
import subprocess

def print_help():
    print("\nUsage:")
    print("  python3 main_menu.py -p       # Run basic port scan")
    print("  python3 main_menu.py -t       # Run threaded port scan with service detection")
    print("  python3 main_menu.py -n       # Run network ping scan")
    print("  python3 main_menu.py -h       # Show this help menu")

def main():
    if len(sys.argv) < 2:
        print("No arguments provided.")
        print_help()
        return

    arg = sys.argv[1]

    if arg == '-p':
        subprocess.run(["python3", "functions.py", "scan"])
    elif arg == '-t':
        subprocess.run(["python3", "functions.py", "scan"])  # both -p and -t currently do same
    elif arg == '-n':
        subprocess.run(["python3", "functions.py", "ping"])
    elif arg == '-h':
        print_help()
    else:
        print(f"Unknown option: {arg}")
        print_help()

if __name__ == "__main__":
    main()
