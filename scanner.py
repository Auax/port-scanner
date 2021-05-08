import argparse
import os
import socket
import sys
import threading
import tqdm
import colorama
from typing import Any
import re

colorama.init(autoreset=True)  # Start colorama instance

os.system("cls") if os.name == "nt" else os.system("clear")  # Clear console

open_ports = []  # Open ports list


def log(v: Any, mode: int = 1) -> None:
    """
    Simple function to improve text printing
    :param v: text to print
    :param mode: (1=Success)(2=Warning)(3=Error)
    :return: None
    """
    if mode == 1:
        print(f"[{colorama.Fore.GREEN}${colorama.Fore.RESET}] {v}")

    elif mode == 2:
        print(f"[{colorama.Fore.YELLOW}^{colorama.Fore.RESET}] {v}")

    elif mode == 3:
        print(f"[{colorama.Fore.RED}!{colorama.Fore.RESET}] {v}")


def portscan(target: str, port: int) -> None:
    """
    Connect to a given target with a given port.
    :param target: target to connect
    :param port: port
    :return: None
    """
    global open_ports

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Initialize socket instance
        s.settimeout(0.5)  # Timeout time
        conn = s.connect_ex((target, port))  # Connect to target
        if conn == 0:
            open_ports.append(str(port))  # Append port to list if the connection was successful
        s.close()  # Close instance

    except:
        pass


# Arguments
parser = argparse.ArgumentParser(description='Analyze the ports of a given IP')
parser.add_argument('--target',
                    metavar='target',
                    type=str,
                    nargs='?',
                    help='target ip or host')

args = parser.parse_args()  # Parse args
ip = args.target  # Get target argument

# Regex pattern to check if str is an ip
pattern = re.compile("'\\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\\.|$)){4}\\b'")

if not ip:
    ip = socket.gethostbyname(socket.gethostname())  # Assign local IP if no target specified
    log("No IP specified, using local IP.", 2)

elif not pattern.search(ip):
    try:
        ip = socket.gethostbyname(ip)
    except socket.gaierror:
        log(f"Error in target '{ip}'. Target format must be: 'example.com' or '192.168.1.1'")
        sys.exit(-1)

log("Connected to: " + ip, 1)
print("\nScanning ports...")

# Scan ports
for i in tqdm.tqdm(range(1, 65535), bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):
    t = threading.Thread(target=portscan, args=(ip, i))
    t.start()

if not open_ports:
    log("No open ports.", 3)  # No ports were found

else:
    ports = '\n'.join(open_ports)

    print()
    for i in open_ports:
        print(f"Port {colorama.Fore.LIGHTMAGENTA_EX}{i}{colorama.Fore.RESET}:\tOpen")  # Print ports
