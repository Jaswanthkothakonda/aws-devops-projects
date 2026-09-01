#!/bin/bash
for tool in git aws docker terraform kubectl
do
    if command -v "$tool" > /dev/null 2>&1; then
        echo "$tool: INSTALLED"
    else
        echo "$tool: NOT INSTALLED"
    fi
done
