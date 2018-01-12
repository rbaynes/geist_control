#!/bin/bash

# Get the current real-time wattage used by every outlet of every strip 
# in container 3 and sum it.

OUTPUT_FN="watts.csv"

# Output the wattage from all 4 outlets on a strip/IP.
# Args: the IP address.
all_watts(){
  IP=$1 # IP address 
  echo "Getting wattage from $IP..."
  geist_wattage.py --IP $IP --outlet 1 --csv >> $OUTPUT_FN
  geist_wattage.py --IP $IP --outlet 2 --csv >> $OUTPUT_FN
  geist_wattage.py --IP $IP --outlet 3 --csv >> $OUTPUT_FN
  geist_wattage.py --IP $IP --outlet 4 --csv >> $OUTPUT_FN
}

# Reset the output file
echo "" > $OUTPUT_FN

# The 8 strips on the left:
all_watts 172.17.2.11 
all_watts 172.17.2.12 
all_watts 172.17.2.13 
all_watts 172.17.2.14 
all_watts 172.17.2.15 
all_watts 172.17.2.16 
all_watts 172.17.2.17 
all_watts 172.17.2.18 

# The 8 strips on the right:
all_watts 172.17.2.21 
all_watts 172.17.2.22 
all_watts 172.17.2.23 
all_watts 172.17.2.24 
all_watts 172.17.2.25 
all_watts 172.17.2.26 
all_watts 172.17.2.27 
all_watts 172.17.2.28 

# Sum 
WATTS=`cut -d , -f 3 $OUTPUT_FN | awk '{total = total + $1}END{print total}'`
echo "Total power used by container 2 is $WATTS watts."

