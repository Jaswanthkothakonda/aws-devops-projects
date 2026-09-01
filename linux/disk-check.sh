#!/bin/bash
usage=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
echo "Disk usage: $usage%"
if [ "$usage" -ge 90 ]; then
    echo "CRITICAL: Disk usage is very high!"
elif [ "$usage" -ge 80 ]; then
    echo "WARNING: Disk usage is high."
else
    echo "OK: Disk usage is normal."
fi
