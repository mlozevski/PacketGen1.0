"""
    PacketGen1.0

    PacketGen1.0 is a packet generator tool that can be used to craft a single pack based off of a yaml file
    Author: Mike Lozevski
"""
from scapy.all import IP, ICMP, Ether, TCP, UDP, sendp, send, ifaces
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
                packet = Ether(**config['Ether'])
            if 'IP' in config:
                L3 = True
                packet = packet_stitcher(packet, IP(**config['IP']))
            if 'IP' in config and ('TCP' in config or 'UDP' in config):
                if 'TCP' in config:
                    packet = packet_stitcher(packet, TCP(**config['TCP']))
                elif 'UDP' in config:
                    packet = packet_stitcher(packet, UDP(**config['UDP']))
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
    global packet, L2, L3, settings
    iface = None
    loop = 0
    inter = 1
    if settings.get('mode') == 'loop':
        loop = 1
    if settings.get('iface_index'):
        iface = ifaces.dev_from_index(settings.get('iface_index'))
    if settings.get('interval'):
        inter = int(settings.get('interval'))
    if L2:
        sendp(packet, iface=iface, loop=loop, inter=inter)
    else:
        send(packet)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
        if packet and settings:
            send_packet()
    else:
        if sys.argv[1].lower() == "interfaces":
            print(ifaces)

