#!/usr/bin/env python3
"""Create Grafana dashboard programmatically"""
import requests

url = 'http://localhost:3000/api/dashboards/db'
auth = ('admin', 'admin')
payload = {
    "dashboard": {
        "title": "System Monitor",
        "refresh": "5s",
        "panels": [
            {
                "title": "CPU Usage (%)",
                "type": "timeseries",
                "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8},
                "targets": [{"expr": "node_cpu_percent", "refId": "A"}],
                "fieldConfig": {"defaults": {}, "overrides": []}
            },
            {
                "title": "Memory (MB)",
                "type": "timeseries",
                "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8},
                "targets": [{"expr": "node_memory_mb", "refId": "A"}],
                "fieldConfig": {"defaults": {}, "overrides": []}
            },
            {
                "title": "Disk Usage (%)",
                "type": "gauge",
                "gridPos": {"x": 0, "y": 8, "w": 12, "h": 8},
                "targets": [{"expr": "node_disk_percent", "refId": "A"}],
                "fieldConfig": {"defaults": {}, "overrides": []}
            },
            {
                "title": "Process Count",
                "type": "stat",
                "gridPos": {"x": 12, "y": 8, "w": 12, "h": 8},
                "targets": [{"expr": "node_processes_count", "refId": "A"}],
                "fieldConfig": {"defaults": {}, "overrides": []}
            }
        ],
        "version": 1,
        "uid": "system-monitor"
    },
    "overwrite": True
}

resp = requests.post(url, json=payload, auth=auth)
if resp.status_code == 200:
    print("✅ Dashboard created successfully!")
    print("📊 View at: http://localhost:3000/d/system-monitor")
else:
    print(f"Error: {resp.status_code} - {resp.text}")
