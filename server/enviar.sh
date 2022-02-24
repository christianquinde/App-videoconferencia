#!/bin/bash
ip_me=$1
ip_server=$2

echo $ip_me > cliente.txt

nc -w 3 $ip_server 8888 < cliente.txt
netcat -l 7777 | pv > base_datos.txt

