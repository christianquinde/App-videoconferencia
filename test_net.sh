#!/bin/bash
ip=$1
#ping -c10 $ip > output.log 2>&1 &
iperf -p 8001 -c $ip -u -t 5 -b 4m > server/bw/net_check.txt 2>&1 &
