PacketGen1.0 is a tool written in Python3 to craft Ethernet/IP packets.

# Installation
```bash
pip3 install -r requirements.txt
```
# Configuration
The Packet Configuration settings are in the packet_config.yaml file.

The configuration file will accept the following parameters

Key: Field Type (default value)
## TCP
- sport: ShortEnumField (20)
- dport: ShortEnumField (80)
- seq: IntField (0)
- ack: IntField (0)
- dataofs: BitField (None)
- reserved: BitField (0)
- flags: FlagsField (<Flag 2 (S)>)
- window: ShortField (8192)
- chksum: XShortField (None)
- urgptr: ShortField (0)
- options: TCPOptionsField (b'')
## UDP
- sport: ShortEnumField (53)
- dport: ShortEnumField (53)
- len: ShortField (None)
- chksum: XShortField (None)
## IP
- version: BitField (4)
- ihl: BitField (None)
- tos: XByteField (0)
- len: ShortField (None)
- id: ShortField (1)
- flags: FlagsField (<Flag 0 ()>)
- frag: BitField (0)
- ttl: ByteField (64)
- proto: ByteEnumField (0)
- chksum: XShortField (None)
- src: SourceIPField (None)
- dst: DestIPField (None)
- options: PacketListField ([])
## Ether
- dst: DestMACField (None)
- src: SourceMACField (None)
- type: XShortEnumField (36864)
## Settings
- mode: String (once | loop )
- iface_index: Int (None)
- interval: Int (1) #loop interval in seconds


# Usage
## List Interfaces
```bash
python3 run.py interfaces
```
## Packet Generation
```bash
python3 run.py
```
