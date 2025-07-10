#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source-node> <destination-node>"
    exit 1
fi

SOURCE=$1
DEST=$2

if [ "$DEST" == "router" ]; then
    # You can choose which IP to use by specifying it directly
    # Let's assume you want to use the IP address on the first interface (172.0.0.1)
    DEST_IP="172.0.0.1"
else
    # Get IP address of the destination node
    DEST_IP=$(ip netns exec "$DEST" ip -4 -o addr show scope global \
          | awk '{split($4,a,"/"); print a[1]}' | head -n 1)
fi

# Ping the destination from the source
ip netns exec $SOURCE ping -c 4 $DEST_IP
