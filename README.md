# System Monitoring Stack

Production-ready monitoring system with Prometheus, Grafana, and JSON logging.

## What It Does

- **Real-time system metrics** (CPU, memory, disk, processes)
- **Metrics collection** via Prometheus exporter
- **Dashboard visualization** in Grafana
- **Professional JSON logging** with trace IDs for debugging
- **Docker-based deployment** for consistency

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.7+
- macOS/Linux

### Run Everything

```bash
# Start Prometheus + Grafana
docker compose up -d

# Start metrics exporter (new terminal)
python3 prometheus_exporter.py

# Start system monitor with logging (new terminal)
bash monitor.sh
```

### Access Services
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Metrics endpoint**: http://localhost:8000/metrics

### Create Dashboard (optional)
```bash
python3 create_dashboard.py
```

## Files

| File | Purpose |
|------|---------|
| `prometheus_exporter.py` | HTTP server exposing system metrics / JSON logs to `exporter.log` |
| `monitor.sh` | Real-time terminal display / JSON logs to `monitor.log` |
| `docker-compose.yml` | Prometheus + Grafana containers |
| `prometheus.yml` | Prometheus scrape configuration |
| `create_dashboard.py` | Auto-create Grafana dashboard |
| `setup.sh` | Initial setup (if needed) |

## Logging

Professional JSON logging with trace IDs for request correlation:

```json
{"timestamp":"2026-04-22T10:55:45Z","level":"INFO","message":"Metrics collected","trace_id":"x7y8z9a0-b1c2-3d4e-5f6g-7h8i9j0k1l2","metrics":{"cpu":25.5,"memory_mb":7234.8}}
```

View logs:
```bash
tail -f monitor.log | python3 -m json.tool
tail -f exporter.log | python3 -m json.tool
```

## Architecture

- **Metrics**: Custom exporter scrapes system data → Prometheus stores → Grafana visualizes
- **Logs**: Bash/Python write JSON logs with trace IDs for debugging
- **Traces**: Trace IDs link events across services for end-to-end visibility

## Code Quality

- Simple, production-ready code
- No over-engineering (Python stdlib only, minimal bash)
- Comprehensive error handling
- JSON structured logging for cloud integration

## Cloud Integration

Logs ready for: AWS CloudWatch, ELK Stack, Datadog, Splunk, Google Cloud Logging
# xgrid-internship-bootstrap

Production-ready DevOps workstation setup.

## Stack
- WSL/Linux
- Python, Docker, Git, Terraform
- AWS CLI
- VS Code

---

## System Monitoring & Prometheus Learning

Real-time monitoring system demonstrating **Metrics**, **Logs**, and **Prometheus** concepts.

### Quick Start
```bash
# Setup
bash setup.sh

# Terminal 1: Real-time monitor + logging
./monitor.sh

# Terminal 2: Prometheus metrics exporter
python3 prometheus_exporter.py

# Terminal 3: Test the endpoint
curl http://localhost:8000/metrics
```

### What You'll Learn
- **Metrics vs Logs vs Traces** - The 3 pillars of observability
- **Prometheus Scraping** - How metrics are collected
- **Node Exporter Flow** - How system metrics are exposed

### Files
- `monitor.sh` - Real-time display + CSV logging
- `prometheus_exporter.py` - HTTP metrics endpoint (educational)
- `system_metrics.log` - Historical data
- `MONITORING_GUIDE.md` - Complete learning guide

### Monitoring Concepts
See [MONITORING_GUIDE.md](MONITORING_GUIDE.md) for detailed explanations of:
- How metrics differ from logs
- Prometheus scraping flow
- Node exporter architecture
