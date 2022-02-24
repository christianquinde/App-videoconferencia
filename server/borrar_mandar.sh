#!/bin/bash
rm ip.txt
ip_server=$1
nc -w 3 $ip_server 8899 < name_ip.txt
echo $ip_server


