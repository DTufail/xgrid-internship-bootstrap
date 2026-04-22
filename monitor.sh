#!/bin/bash

# System Monitor with Professional JSON Logging
REFRESH_RATE=2
LOG_FILE="monitor.log"

# Function to generate UUID-like trace ID (simple version for compatibility)
generate_trace_id() {
    uuidgen 2>/dev/null || python3 -c "import uuid; print(str(uuid.uuid4()))"
}

# Function to log JSON format
log_json() {
    local level=$1
    local message=$2
    local cpu=$3
    local memory=$4
    local disk=$5
    local processes=$6
    local trace_id=$7
    
    # Generate ISO 8601 timestamp
    local timestamp=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    
    # Create JSON log entry
    printf '{"timestamp":"%s","level":"%s","message":"%s","trace_id":"%s"' "$timestamp" "$level" "$message" "$trace_id"
    
    # Add metrics if provided
    if [[ -n "$cpu" ]]; then
        printf ',"metrics":{"cpu":%s,"memory_mb":%s,"disk_percent":%s,"process_count":%s}' "$cpu" "$memory" "$disk" "$processes"
    fi
    
    printf '}\n'
}

# Initialize log file with startup info
trace_id=$(generate_trace_id)
log_json "INFO" "System monitor started" "" "" "" "" "$trace_id" > "$LOG_FILE"

while true; do
    clear
    
    # Generate new trace ID for this monitoring cycle
    trace_id=$(generate_trace_id)
    
    CPU=$(top -l 2 | grep "CPU usage" | tail -n 1 | awk '{print $7}' | sed 's/%//' | awk '{print 100 - $1}')
    MEM=$(ps aux | awk '{sum += $6} END {printf "%.1f", sum/1024}')
    DISK=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
    PROC=$(ps aux | wc -l)
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    TIMESTAMP_ISO=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    
    # Display in terminal (human-readable)
    echo "=== System Monitor [$(date '+%H:%M:%S')] ==="
    echo "Trace-ID:  $trace_id"
    echo "CPU:       ${CPU}%"
    echo "Memory:    ${MEM}MB"
    echo "Disk:      ${DISK}%"
    echo "Processes: $PROC"
    echo "======================================"
    
    # Log to JSON file (PROFESSIONAL LOGS)
    log_json "INFO" "Metrics collected" "$CPU" "$MEM" "$DISK" "$PROC" "$trace_id" >> "$LOG_FILE"
    
    sleep $REFRESH_RATE
done
