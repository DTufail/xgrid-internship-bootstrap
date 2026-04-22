# System Monitoring Stack

Production-ready monitoring system with Prometheus, Grafana, and JSON logging.

## Quick Start

```bash
# Start Docker services
docker compose up -d

# Terminal 2: Start metrics exporter
python3 prometheus_exporter.py

# Terminal 3: Start system monitor
bash monitor.sh
```

**Access:**
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090
- Exporter: http://localhost:8000/metrics

## Files

| File | Purpose |
|------|---------|
| `prometheus_exporter.py` | Metrics exporter (CPU, memory, disk, processes) |
| `monitor.sh` | Real-time monitor + JSON logging |
| `docker-compose.yml` | Prometheus + Grafana containers |
| `prometheus.yml` | Prometheus configuration |
| `create_dashboard.py` | Auto-create Grafana dashboard |

## Logs

JSON logs with trace IDs in `exporter.log` and `monitor.log`:

```bash
tail -f monitor.log | python3 -m json.tool
```

## Stop Everything

```bash
docker compose down && pkill -f prometheus_exporter.py && pkill -f monitor.sh
```
