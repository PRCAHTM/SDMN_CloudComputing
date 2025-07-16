# Routing Between Two Hosts, Each Running Its Own Namespace Topology  
(Figure 3 — “Namespaces on Two Physical/Virtual Servers”)

In Figure 3, **server 1** holds `node1` + `node2` on bridge **br1**  
(`172.0.0.0/24`), while **server 2** holds `node3` + `node4` on bridge **br2**  
(`10.10.0.0/24`). The two servers are plugged into the **same Layer‑2 switch**
(plain Ethernet connectivity, no VLANs).

Goal: allow full IP reachability between the two /24 networks **without moving
namespaces or creating extra VMs**.

---

## 1  Chosen design — make *one* server a software router

* **server 1** will own an IP in **both subnets** and forward packets.
* A simple **veth pair** forms an L2 patch‑cord between the bridges, traversing
  the physical switch.
* Nodes keep using a gateway in their own subnet (`172.0.0.254` or
  `10.10.0.254`) but that gateway now lives on server 1.

> Alternative designs (L3 switch, BGP, VXLAN) are mentioned at the end, but the
> “one server routes” approach works everywhere with zero extra hardware.

---

## 2  Implementation details

### 2.1  Create a cross‑server veth pair

| Step | Command | Where |
|------|---------|-------|
| 1 | `ip link add s1-port type veth peer name s2-port` | **server 1** |
| 2 | **Pass `veth s2-port`** to **server 2**<br>(e.g., attach to a virtual NIC, move into server 2’s namespace, or create a second veth locally on server 2 with matching MAC) | host / hypervisor |
| 3 | `ip link set s1-port master br1` | **server 1** |
| 4 | `ip link set s2-port master br2` | **server 2** |
| 5 | `ip link set s1-port up && ip link set s2-port up` | both |

After these steps, frames from br1 can reach br2 purely at Layer 2 through the
physical switch and the veth cable.

### 2.2  Give server 1 gateway IPs

```bash
# on server 1
ip addr add 172.0.0.254/24 dev br1    # gateway for node1/2
ip addr add 10.10.0.254/24 dev s1-port  # gateway for node3/4
sysctl -w net.ipv4.ip_forward=1


```

2.4  Limit forwarding with firewall rules

``` bash
# on server 1
iptables -A FORWARD -i br1 -o s1-port -j ACCEPT
iptables -A FORWARD -i s1-port -o br1 -j ACCEPT
iptables -P FORWARD DROP    # default deny the rest

```

Verification

``` bash
# Ping across servers
ip netns exec node1 ping -c 3 10.10.0.2   # node1 → node3 (should succeed)
ip netns exec node4 ping -c 3 172.0.0.3   # node4 → node2

# Show routes on server 1 (two connected nets)
ip route show
