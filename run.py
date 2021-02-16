"""
    PacketGen1.0

    PacketGen1.0 is a packet generator tool that can be used to craft a single pack based off of a yaml file
    Author: Mike Lozevski
"""
from scapy.all import IP, ICMP, Ether, TCP, UDP, sendp, send
import sys
import yaml

packet = None
L2 = False
L3 = False
settings = None

def packet_stitcher(packet, new_packet):
    if packet:
        return packet/new_packet
    else:
        return new_packet


def config_transport_helper(obj, t_config):
    global packet
    if t_config.get('port_src') and t_config.get('port_dst') is None:
        packet = packet_stitcher(packet,obj(sport=t_config.get('port_src')))
    elif t_config.get('port_dst') and t_config.get('port_src') is None:
        packet = packet_stitcher(packet, obj(dport=t_config.get('port_dst')))
    else:
        packet = packet_stitcher(packet, obj(sport=t_config.get('port_src'), dport=t_config.get('port_dst')))


def main():
    global packet, settings, L2, L3
    with open("packet_config.yaml", 'r') as stream:
        try:
            print("loading config...")
            config = yaml.safe_load(stream)
            if 'Ether' in config:
                L2 = True
                ether_config = config['Ether']
                if ether_config.get('mac_src') and ether_config.get('mac_dst') is None:
                    packet = Ether(src=ether_config.get('mac_src'))
                elif ether_config.get('mac_dst') and ether_config.get('mac_src') is None:
                    packet = Ether(dst=ether_config.get('mac_dst'))
                else:
                    packet = Ether(src=ether_config.get('mac_src'), dst=ether_config.get('mac_dst'))
            if 'IP' in config:
                L3 = True
                ip_config = config['IP']
                if ip_config.get('ip_src') and ip_config.get('ip_dst') is None:
                    packet = packet_stitcher(packet, IP(src=ip_config.get('ip_src')))
                elif ip_config.get('ip_dst') and ip_config.get('ip_src') is None:
                    packet = packet_stitcher(packet, IP(dst=ip_config.get('ip_dst')))
                else:
                    packet = packet_stitcher(packet, IP(src=ip_config.get('ip_src'), dst=ip_config.get('ip_dst')))
            if 'IP' in config and ('TCP' in config or 'UDP' in config):
                if 'TCP' in config:
                    transport_config = config['TCP']
                    config_transport_helper(TCP, transport_config)
                elif 'UDP' in config:
                    transport_config = config['UDP']
                    config_transport_helper(UDP, transport_config)
            print("packet created...")
            if 'Settings' in config:
                settings = config['Settings']
            else:
                print("settings are missing. Exiting")
                sys.exit(1)
        except yaml.YAMLError as exc:
            print("Error reading yaml file. Exiting")
            sys.exit(1)


def send_packet():
    global packet, L2, L3
    if L3 and L2:
        sendp(packet)
    elif L2 and not L3:
        sendp(packet)
    else:
        send(packet)


if __name__ == '__main__':
    main()
    if packet and settings:
        if settings.get('mode') == 'one-time':
            send_packet()

