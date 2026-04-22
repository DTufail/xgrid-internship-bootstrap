#!/usr/bin/env python3
"""
Simple Prometheus Exporter - Educational Implementation
Demonstrates how metrics are exposed for Prometheus to scrape
"""

import subprocess
import time
import json
import uuid
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from datetime import datetime, timezone

# Configure professional JSON logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.FileHandler('exporter.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class JSONFormatter(logging.Formatter):
    """Format logs as JSON for machine readability"""
    def format(self, record):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "trace_id": getattr(record, 'trace_id', None)
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

# Apply JSON formatter
for handler in logger.handlers:
    handler.setFormatter(JSONFormatter())

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests to /metrics endpoint"""
        trace_id = str(uuid.uuid4())
        
        if self.path == '/metrics':
            # Create logger with trace ID context
            handler_logger = logging.LoggerAdapter(logger, {'trace_id': trace_id})
            
            try:
                # Collect METRICS (not logs/traces, but numeric measurements)
                metrics = self.collect_metrics(handler_logger, trace_id)
                
                handler_logger.info("Metrics collected successfully", extra={'trace_id': trace_id})
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(metrics.encode('utf-8'))
            except Exception as e:
                handler_logger.error(f"Failed to collect metrics: {e}", exc_info=True, extra={'trace_id': trace_id})
                self.send_response(500)
                self.end_headers()
        else:
            handler_logger = logging.LoggerAdapter(logger, {'trace_id': trace_id})
            handler_logger.warning(f"Unknown endpoint: {self.path}", extra={'trace_id': trace_id})
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass
    
    def collect_metrics(self, handler_logger, trace_id):
        """Collect system metrics in Prometheus format"""
        try:
            handler_logger.debug("Starting metrics collection", extra={'trace_id': trace_id})
            
            # Get CPU usage
            cpu = subprocess.check_output(
                "top -l 1 | grep 'CPU usage' | awk '{print $3}'",
                shell=True
            ).decode().strip().rstrip('%')
            
            # Get memory usage
            mem = subprocess.check_output(
                "ps aux | awk '{sum += $6} END {print sum/1024}'",
                shell=True
            ).decode().strip()
            
            # Get disk usage
            disk = subprocess.check_output(
                "df -h / | tail -1 | awk '{print $5}' | sed 's/%//'",
                shell=True
            ).decode().strip()
            
            # Get process count
            proc = subprocess.check_output(
                "ps aux | wc -l",
                shell=True
            ).decode().strip()
            
            handler_logger.debug(
                f"Collected metrics: CPU={cpu}%, Memory={mem}MB, Disk={disk}%, Processes={proc}",
                extra={'trace_id': trace_id, 'cpu': cpu, 'memory': mem, 'disk': disk, 'processes': proc}
            )
            
            # Format as Prometheus metrics
            metrics = f"""# HELP node_cpu_percent CPU usage percentage
# TYPE node_cpu_percent gauge
node_cpu_percent {cpu}

# HELP node_memory_mb Memory usage in megabytes
# TYPE node_memory_mb gauge
node_memory_mb {mem}

# HELP node_disk_percent Disk usage percentage
# TYPE node_disk_percent gauge
node_disk_percent {disk}

# HELP node_processes_count Number of running processes
# TYPE node_processes_count gauge
node_processes_count {proc}
"""
            return metrics
        except Exception as e:
            handler_logger.error(f"Error collecting metrics: {e}", exc_info=True, extra={'trace_id': trace_id})
            return f"# Error collecting metrics: {e}"

def start_exporter(port=8000):
    """Start Prometheus exporter server"""
    trace_id = str(uuid.uuid4())
    handler_logger = logging.LoggerAdapter(logger, {'trace_id': trace_id})
    
    handler_logger.info(f"Starting Prometheus exporter on port {port}", extra={'trace_id': trace_id})
    server = HTTPServer(('localhost', port), MetricsHandler)
    handler_logger.info(f"Prometheus exporter listening on http://localhost:{port}/metrics", extra={'trace_id': trace_id})
    server.serve_forever()

if __name__ == '__main__':
    trace_id = str(uuid.uuid4())
    startup_logger = logging.LoggerAdapter(logger, {'trace_id': trace_id})
    startup_logger.info("Application startup", extra={'trace_id': trace_id})
    start_exporter(8000)
