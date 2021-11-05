import os
import sys
import traceback
import pandas as pd
from tabulate import tabulate
from IPython.display import display


print("0SPLOIT BY DMX")


def config0():
    global up_interface
    up_interface = open(
        'C:\\Users\\shubh\\Documents\\Github Projects\\Network Scanner\\tools\\files\\iface.txt', 'r').read()

    if up_interface == "0":
        up_interface = os.popen(
            "route | awk '/Iface/{getline; print $8}'").read()
    up_interface = up_interface.replace('\n', '')

    global gateway
    gateway = open(
        'C:\\Users\\shubh\\Documents\\Github Projects\\Network Scanner\\tools\\files\\gateway.txt', 'r').read()
    if gateway == "0":
        gateway = os.popen(
            "ip route show | grep -i 'default via'| awk '{print $3 }'").read()
    gateway = gateway.replace('\n', '')


def home():
    config0()
    n_name = os.popen('iwgetid -r').read()
    n_mac = os.popen(
        "ip addr | grep 'state UP' -A1 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'").read()
    n_ip = os.popen("hostname -I").read()
    n_host = os.popen("hostname").read()

    table = {
        "IP Address": [n_ip],
        "MAC Address": [n_mac.upper()],
        "Gateway": [gateway],
        "Iface": [up_interface],
        "Hostname": [n_host]
    }

    df = pd.DataFrame(table)

    print(tabulate(df, headers='keys', tablefmt='psql'))


def scan():

    config0()
    scan = os.popen("arp-scan --interface=" +
                    up_interface + " -localnet ").read()

    f = open(
        'C:\\Users\\shubh\\Documents\\Github Projects\\Network Scanner\\tools\\log\\scan.txt', 'w')
    f.write(scan)
    f.close()

    devices = os.popen(
        " cat C:\\Users\\shubh\\Documents\\Github Projects\\Network Scanner\\tools\\log\\scan.txt | awk '{print $1}' | head -n -2 | sed  '1,2d'").read()

    devices_mac = os.popen(
        "cat C:\\Users\\shubh\\Documents\\Github Projects\\Network Scanner\\tools\\log\\scan.txt | sed '1,2d' | head -n -2 | awk '{print $2}'").read().upper()

    devices_name = os.popen(
        "cat C:\\Users\\shubh\\Documents\\Github Projects\\Network Scanner\\tools\\log\\scan.txt |sed '1,2d' | head -n -2 | awk '{print $3,$4,$5,$6}' ").read()

    table = {
        "IP Address": [devices],
        "MAC Address": [devices_mac],
        "Manufacturer": [devices_name]
    }

    df = pd.DataFrame(table)

    print(tabulate(df, headers='keys', tablefmt='psql'))


home()

print("network scan:\n")


scan()
