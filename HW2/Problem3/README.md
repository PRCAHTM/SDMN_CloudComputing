# Problem 3


1. A full description and usage guide  
2. Comprehensive test commands  
3. The complete source code (`server.py`)  
4. The production Dockerfile

---

## 1  Endpoint contract

| Method | Path | Body (JSON) | HTTP code | Response body |
|--------|------|-------------|-----------|---------------|
| **GET** | `/api/v1/status` | — | `200 OK` | `{"status":"<current>"}` |
| **POST** | `/api/v1/status` | `{"status":"<new‑value>"}` | `201 Created` | echoes the same JSON |

* First GET (or after container restart) returns `{"status":"OK"}`.  
* Any POST updates the server‑side variable; subsequent GETs return the new value.

---

## 2  Build & run

### 2.1  Docker prerequisites

| Component | Ubuntu command |
|-----------|----------------|
| Docker Engine ≥ 24.x | `sudo apt install docker.io` |


### 2.2  Image build

```bash
docker build -t status-server:1.0 .

docker run --name status-server -p 8000:8000 status-server:1.0

# Open a second terminal while the container is running and execute:

# 1) Baseline: first GET should be "OK"
curl -i http://localhost:8000/api/v1/status

# 2) Update status via POST
curl -i -X POST -H "Content-Type: application/json" \
     -d '{"status":"not OK"}' \
     http://localhost:8000/api/v1/status

# 3) Confirm persistence
curl -i http://localhost:8000/api/v1/status

# 4) Reset back to OK
curl -i -X POST -H "Content-Type: application/json" \
     -d '{"status":"OK"}' \
     http://localhost:8000/api/v1/status

# 5) Check reset after container restart
docker restart status-server
sleep 2
curl -i http://localhost:8000/api/v1/status

# 6) Concurrency smoke‑test: 5 parallel GETs
for i in {1..5}; do curl -s http://localhost:8000/api/v1/status & done; wait; echo


