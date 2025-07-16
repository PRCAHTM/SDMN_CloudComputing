# Problem 2

This folder contains a **two‑file** implementation of a lightweight container
runtime:

| File | Role |
|------|------|
| **`filesystem.sh`** | One‑time helper that downloads and untars an **Ubuntu 20.04** base image into `./container/`. |
| **`cli.py`** | Python 3 launcher that unshares `pid`, `net`, `mnt`, and `uts` namespaces, pivots to the new root filesystem, sets the hostname, and (optionally) enforces a memory cgroup limit. |

---

## Prerequisites

| Package / Feature | Reason | Ubuntu 20.04 command |
|-------------------|--------|----------------------|
| **Python ≥ 3.8** | runs `cli.py` (stdlib‑only) | `sudo apt install python3` |
| **util‑linux** | provides the `unshare` CLI | *pre‑installed* |
| **uidmap** | clean UID‑mapping with user namespaces (optional) | `sudo apt install uidmap` |
| **wget & tar** | download + extract rootfs | `sudo apt install wget tar` |
| **sudo** | namespaces, mounts, and cgroups need root privs | `sudo apt install sudo` |


---

## Step‑by‑step guide

```bash
# 0) Clone / cd into Problem2 folder
cd Problem2

# 1) Make scripts executable once
chmod +x filesystem.sh cli.py

# 2) Download & unpack Ubuntu 20.04 rootfs (≈ 45 MB)
./filesystem.sh
#   └─ creates ./container/ with an Ubuntu base image inside

# 3) Launch a container
sudo ./cli.py mybox -m 64
#   └─ mybox   → hostname inside container
#   └─ -m 64   → memory cap = 64 MB (omit for unlimited)

# 4) Play inside the container
root@mybox:/# hostname
mybox
root@mybox:/# ps fax               # bash is PID 1
root@mybox:/# free -h              # shows 64 MB total
root@mybox:/# cat /etc/os-release  # Ubuntu 20.04 info
root@mybox:/# exit                 # or Ctrl‑D to leave

