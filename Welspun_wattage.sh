#!/bin/bash

# Get the current real-time wattage used by every outlet of every strip 
# in container 3 and sum it.

OUTPUT_FN=`date "+FS2-watts-%Y-%m-%d-%H-%M-%S-%s.csv"`

# Output the wattage from all 4 outlets on a strip/IP.
# Args: the IP address.
all_watts(){
  IP=$1 # IP address 
  echo "Getting wattage from $IP..."
  ./geist_wattage.py --IP $IP --outlet 1 --csv >> $OUTPUT_FN
  ./geist_wattage.py --IP $IP --outlet 2 --csv >> $OUTPUT_FN
  ./geist_wattage.py --IP $IP --outlet 3 --csv >> $OUTPUT_FN
  ./geist_wattage.py --IP $IP --outlet 4 --csv >> $OUTPUT_FN
}

# Reset the output file
echo "" > $OUTPUT_FN

# The 8 strips on the left:
all_watts 192.168.151.72 
all_watts 192.168.151.73 
all_watts 192.168.151.74 
all_watts 192.168.151.75 
all_watts 192.168.151.76 
all_watts 192.168.151.77 
all_watts 192.168.151.78 
all_watts 192.168.151.79 

# The 8 strips on the right:
all_watts 192.168.151.82 
all_watts 192.168.151.83 
all_watts 192.168.151.84 
all_watts 192.168.151.85 
all_watts 192.168.151.86 
all_watts 192.168.151.87 
all_watts 192.168.151.88 
all_watts 192.168.151.89 

# Sum 
WATTS=`cut -d , -f 3 $OUTPUT_FN | awk '{total = total + $1}END{print total}'`
TOTAL="Total power used by container 2 is $WATTS watts."
echo $TOTAL >> $OUTPUT_FN
echo $TOTAL

