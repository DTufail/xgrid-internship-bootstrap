#!/usr/bin/env python3
import requests

URL = 'http://localhost:3000/api/dashboards/db'
AUTH = ('admin', 'admin')

payload = {
    "dashboard": {
        "title": "System Monitor",
        "refresh": "5s",
        "uid": "system-monitor",
        "panels": [
            {
                "title": "CPU Usage (%)",
                "type": "timeseries",
                "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8},
                "targets": [{"expr": "node_cpu_usage_percent", "refId": "A"}]
            },
            {
                "title": "Memory Used (bytes)",
                "type": "timeseries",
                "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8},
                "targets": [{"expr": "node_memory_used_bytes", "refId": "A"}]
            },
            {
                "title": "Disk Usage (%)",
                "type": "gauge",
                "gridPos": {"x": 0, "y": 8, "w": 12, "h": 8},
                "targets": [{"expr": "node_disk_usage_percent", "refId": "A"}]
            },
            {
                "title": "Process Count",
                "type": "stat",
                "gridPos": {"x": 12, "y": 8, "w": 12, "h": 8},
                "targets": [{"expr": "node_processes_total", "refId": "A"}]
            }
        ],
        "version": 1
    },
    "overwrite": True
}

def setup_dashboard():
    try:
        response = requests.post(URL, json=payload, auth=AUTH)
        if response.status_code == 200:
            print("✅ Dashboard created: http://localhost:3000/d/system-monitor")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == '__main__':
    setup_dashboard()
