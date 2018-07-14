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
pping 172.17.3.11 
pping 172.17.3.12 
pping 172.17.3.13 
pping 172.17.3.14 
pping 172.17.3.15 
pping 172.17.3.16 
pping 172.17.3.17 
pping 172.17.3.18 

# The 8 strips on the right:
pping 172.17.3.21 
pping 172.17.3.22 
pping 172.17.3.23 
pping 172.17.3.24 
pping 172.17.3.25 
pping 172.17.3.26 
pping 172.17.3.27 
pping 172.17.3.28 


