#!/bin/bash

./scripts/wait-for-it.sh -t 15 $POSTGRES_HOST:$POSTGRES_PORT
status=$?
if [ $status -ne 0 ]; then
    echo "Failed to connect to database: $status"
    exit $status
fi

cd app

echo "RUN DEV SERVER"
fastapi dev ../app/main.py --host $HOST --port $PORT
