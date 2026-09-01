#!/bin/bash

if command -v docker > /dev/null 2>&1; then
    echo "Docker is installed"
    exit 0
else
    echo "Docker is NOT installed"
    exit 1
fi
