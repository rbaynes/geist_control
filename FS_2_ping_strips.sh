#!/bin/bash

# Args: the IP address.
pping(){
  IP=$1 # IP address 
  ping -q -c 1 $IP > /dev/null
  if [ $? -ne 0 ]; then
    echo "$IP not responding."
    return
  fi
  echo "$IP OK."
}

# The 8 strips on the left:
pping 172.17.2.11 
pping 172.17.2.12 
pping 172.17.2.13 
pping 172.17.2.14 
pping 172.17.2.15 
pping 172.17.2.16 
pping 172.17.2.17 
pping 172.17.2.18 

# The 8 strips on the right:
pping 172.17.2.21 
pping 172.17.2.22 
pping 172.17.2.23 
pping 172.17.2.24 
pping 172.17.2.25 
pping 172.17.2.26 
pping 172.17.2.27 
pping 172.17.2.28 


