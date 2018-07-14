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
pping 192.168.151.72 
pping 192.168.151.73 
pping 192.168.151.74 
pping 192.168.151.75 
pping 192.168.151.76 
pping 192.168.151.77 
pping 192.168.151.78 
pping 192.168.151.79 

# The 8 strips on the right:
pping 192.168.151.82 
pping 192.168.151.83 
pping 192.168.151.84 
pping 192.168.151.85 
pping 192.168.151.86 
pping 192.168.151.87 
pping 192.168.151.88 
pping 192.168.151.89 
