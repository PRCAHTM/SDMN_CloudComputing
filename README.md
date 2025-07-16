# SDMN — Homework 2  

> **Course:** Software‑Defined & Mobile Networks (SDMN)  
> **Term:** Spring 2025  
> **Student:** Parsa Hatami
> **Instructor:** Dr.Khalaj & Dr.Ravanshid

---

## What you’ll find in this repo

| Folder | Problem | One‑liner |
|--------|---------|-----------|
| `Problem1/` | **Virtual Network Topology** | Builds a five‑node lab (4 hosts + router) entirely with Linux namespaces, veths, and bridges. |
| `Problem2/` | **Mini‑Container Runtime** | A “very small Docker” CLI that spawns an Ubuntu 20.04 rootfs in fresh `pid`, `net`, `mnt`, `uts` namespaces, with optional memory cgroup limits. |
| `Problem3/` | **Status REST API in Docker** | Tiny Python HTTP server (`/api/v1/status`) plus a production‑ready `Dockerfile`. |

Each problem folder contains its own **README.md**, scripts, and (where needed) a `Dockerfile`.

---

## Quick prerequisites

| Component | Tested version(s) |
|-----------|------------------|
| **OS** | Ubuntu 20.04 LTS on VirtualBox |
| **Python** | 3.8 – 3.12 |
| **Docker** | 24.x (Engine + CLI + Buildx) |
| **iproute2** tools | pre‑installed on Ubuntu |

---
