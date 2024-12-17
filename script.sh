#!/bin/bash

# Path to the JSON file
PARAM_FILE="turnover.json"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Install it with 'sudo apt-get install jq'."
    exit 1
fi

# Extract the list of stocks
STOCKS=$(jq -r '.[]' "$PARAM_FILE")  # Extract stocks directly from the array

# Loop through each stock in the list and run the Python script
for STOCK in $STOCKS; do
    echo "Running script for stock: $STOCK"
    python psql.py --stock "$STOCK"
    if [ $? -ne 0 ]; then
        echo "Error: Script failed for stock: $STOCK" >&2
    fi
done
