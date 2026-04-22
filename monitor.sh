#!/bin/bash

CPU=$(top -l 1 | grep "CPU usage" | awk '{print $3}')
MEM=$(vm_stat | grep "Pages active" | awk '{print $3}' | tr -d '.')
DISK=$(df -h / | tail -1 | awk '{print $5}')
PROC=$(ps aux | wc -l)

TIMESTAMP=$(date)

echo "{
   \"cpu\": \"$CPU\",
   \"memory\": \"$MEM\",
   \"disk\": \"$DISK\",
   \"PROCESSES\": \"$PROC\"
   \"timestamp\": \"${TIMESTAMP}\"
}"
