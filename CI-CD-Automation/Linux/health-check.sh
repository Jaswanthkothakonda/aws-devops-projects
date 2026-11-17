#!/bin/bash

set -euo pipefail

echo "======================================"
echo "        SERVER HEALTH CHECK"
echo "======================================"

# Check disk usage
check_disk() {
    usage=$(df / | awk 'NR==2 {print $5}' | tr -d '%')

    echo ""
    echo "Disk Usage: $usage%"

    if [ "$usage" -ge 90 ]; then
        echo "CRITICAL: Disk usage is very high!"
        return 1
    elif [ "$usage" -ge 80 ]; then
        echo "WARNING: Disk usage is high."
    else
        echo "OK: Disk usage is normal."
    fi
}

# Check memory
check_memory() {
    memory=$(free | awk '/Mem:/ {printf "%.0f", ($3/$2)*100}')

    echo ""
    echo "Memory Usage: $memory%"

    if [ "$memory" -ge 90 ]; then
        echo "CRITICAL: Memory usage is very high!"
        return 1
    elif [ "$memory" -ge 80 ]; then
        echo "WARNING: Memory usage is high."
    else
        echo "OK: Memory usage is normal."
    fi
}

# Display system information
check_system() {
    echo ""
    echo "Hostname: $(hostname)"
    echo "Uptime: $(uptime -p)"
}

check_system
check_disk
check_memory

echo ""
echo "======================================"
echo "        HEALTH CHECK COMPLETE"
echo "======================================"
