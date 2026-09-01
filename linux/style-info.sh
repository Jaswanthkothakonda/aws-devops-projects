#!/bin/bash
check_disk()
{
    echo "===== DISK ====="
    df -h /
}

check_memory()
{
    echo "===== MEMORY ====="
    free -h
}

check_uptime()
{
    echo "===== UPTIME ====="
    uptime
}

check_disk
check_memory
check_uptime
