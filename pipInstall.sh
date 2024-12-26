#!/bin/bash

if [ -n "$1" ]; then
    pip install "$@"
    pip freeze > requirements.txt
else
    echo -e "\n\nYou need to add the items to install\n\n"
fi 