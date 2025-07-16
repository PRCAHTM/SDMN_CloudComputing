# Problem 1

This folder contains two Bash scripts that build, test, and (optionally) tear
down a **self‑contained network lab** .

| Script | Purpose |
|--------|---------|
| **`create_topology.sh`** | Creates 5 network namespaces (`node1 … node4`, `router`), wires them with veth pairs, bridges them on the host, assigns IPv4 addresses, enables IP‑forwarding, and pushes default routes. |
| **`ping_from_to.sh`** | Convenience wrapper to verify reachability: *source‑NS → destination‑NS*. Resolves the destination’s IP automatically (or uses `172.0.0.1` when you ping the router). |


<br>

## Quick‑start

```bash
# 1) Make scripts executable once
chmod +x create_topology.sh ping_from_to.sh

# 2) Build the lab (needs sudo for namespace + bridge operations)
sudo ./create_topology.sh          # → "Network Created."

# 3) Ping‑tests
sudo ./ping_from_to.sh node1 node2      # same subnet
sudo ./ping_from_to.sh node1 node3      # routed via 'router'
sudo ./ping_from_to.sh node3 router     # reach router interface

