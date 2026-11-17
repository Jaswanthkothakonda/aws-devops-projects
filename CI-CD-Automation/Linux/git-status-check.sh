#!/bin/bash

if command -v git > /dev/null 2>&1; then
    echo "Git is installed"
    exit 0
else
    echo "Git is NOT installed"
    exit 1
fi
