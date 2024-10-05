#!/bin/bash

while true; do
    echo "Executing supabase_client.py..."
    python3 supabase_client.py 2>&1 | tee -a supabase_client.log

    if [ $? -eq 0 ]; then
        echo "supabase_client.py executed successfully."
        break
    else
        echo "Error occurred while executing supabase_client.py. Retrying..."
        sleep 5  # Wait for 5 seconds before retrying
    fi
done

echo "Process completed."
exit 0
