#  No Router (Figure 2)  
How to Reach 10.10.0.0/24 from 172.0.0.0/24 After Removing the Router

When the **`router`** namespace and its veth links are deleted, both subnets
remain wired to the host via **br1** and **br2**, but nothing forwards packets
between them.  
We can let the **host itself** act as a software router and restore full
connectivity with a handful of root‑namespace commands.

---

## 1  Concept

1. **Create a point‑to‑point link** between `br1` and `br2` (a veth pair).
2. **Give the host one IP in each subnet** on that link (`172.0.0.254` and `10.10.0.254`).
3. **Enable IP forwarding** on the host.
4. **Update each node’s default gateway** to the new host IP on its local
   bridge.

No changes are required inside the green namespaces besides the route update.

---

## 2  Step‑by‑step commands (run as root)

```bash
# 1) Create a veth pair that will represent "router ports"
ip link add br1-port type veth peer name br2-port

# 2) Attach each end to its respective bridge
ip link set br1-port master br1
ip link set br2-port master br2
ip link set br1-port up
ip link set br2-port up

# 3) Assign gateway IPs (host owns one per subnet)
ip addr add 172.0.0.254/24 dev br1-port
ip addr add 10.10.0.254/24  dev br2-port

# 4) Enable Layer‑3 forwarding in the host kernel
sysctl -w net.ipv4.ip_forward=1

# 5) Update default routes inside each node namespace
ip netns exec node1 ip route replace default via 172.0.0.254
ip netns exec node2 ip route replace default via 172.0.0.254
ip netns exec node3 ip route replace default via 10.10.0.254
ip netns exec node4 ip route replace default via 10.10.0.254

