#!/bin/bash
ip_me=$1
#sudo tcpdump 'icmp[icmptype] == icmp-echo' and dst $ip_me -c 5 -w llamada_entrante.pcap -i tun0  # cambiar interfaz

iperf -s -p 8001 -u -P 1 > bw/net_check.txt 2>&1 &
sudo tcpdump udp port 8001 and dst $ip_me -c 1600 -w llamada_entrante.pcap -i tun0

