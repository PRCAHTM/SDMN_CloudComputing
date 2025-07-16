#!/bin/bash

# Create network namespaces
ip netns add node1
ip netns add node2
ip netns add node3
ip netns add node4
ip netns add router

# Create bridges in the root namespace
ip link add br1 type bridge
ip link add br2 type bridge
ip link set br1 up
ip link set br2 up

# Create veth pairs and assign them to namespaces
ip link add veth-node1 type veth peer name veth-br11
ip link add veth-node2 type veth peer name veth-br12
ip link add veth-node3 type veth peer name veth-br23
ip link add veth-node4 type veth peer name veth-br24
ip link add veth-router1 type veth peer name veth-br1
ip link add veth-router2 type veth peer name veth-br2
ip link set veth-node1 netns node1
ip link set veth-node2 netns node2
ip link set veth-node3 netns node3
ip link set veth-node4 netns node4
ip link set veth-router1 netns router
ip link set veth-router2 netns router


ip netns exec node1 ip link set veth-node1 up
ip netns exec node2 ip link set veth-node2 up
ip netns exec node3 ip link set veth-node3 up
ip netns exec node4 ip link set veth-node4 up
ip netns exec router ip link set veth-router1 up
ip netns exec router ip link set veth-router2 up
ip link set veth-br1 up
ip link set veth-br2 up
ip link set veth-br11 up
ip link set veth-br12 up
ip link set veth-br23 up
ip link set veth-br24 up

# Connect veth pairs to bridges
echo "Connecting Bridges"
ip link set veth-br11 master br1
ip link set veth-br12 master br1
ip link set veth-br23 master br2
ip link set veth-br24 master br2
ip link set veth-br1 master br1
ip link set veth-br2 master br2

# Assign IP addresses to veth interfaces
echo "Set IPs"
ip netns exec node1 ip addr add 172.0.0.2/24 dev veth-node1
ip netns exec node2 ip addr add 172.0.0.3/24 dev veth-node2
ip netns exec node3 ip addr add 10.10.0.2/24 dev veth-node3
ip netns exec node4 ip addr add 10.10.0.3/24 dev veth-node4
ip netns exec router ip addr add 172.0.0.1/24 dev veth-router1
ip netns exec router ip addr add 10.10.0.1/24 dev veth-router2

# IP forwarding
ip netns exec router sysctl -w net.ipv4.ip_forward=1

ip netns exec node1 ip route add default via 172.0.0.1
ip netns exec node2 ip route add default via 172.0.0.1
ip netns exec node3 ip route add default via 10.10.0.1
ip netns exec node4 ip route add default via 10.10.0.1

echo "Network Created."
