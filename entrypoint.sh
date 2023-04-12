#!/bin/sh

echo "Starting telepinger..."

echo "Current environment variables:"

env | grep MINUTES_
env | grep PING_
env | grep INFLUXDB_
env | grep NOTIFY_

# force setup of InfluxDB Vars
export INFLUXDB_BUCKET=${INFLUXDB_BUCKET:-telepinger-no-bucket}
export INFLUXDB_ORG=${INFLUXDB_ORG:-telepinger}
export INFLUXDB_TOKEN=${INFLUXDB_TOKEN:-telepinger}
export INFLUXDB_URL=${INFLUXDB_URL:-http://localhost:8086}

# Set up the cron job
echo "*/$MINUTES_INTERVAL * * * * /usr/local/bin/python /app/telepinger.py -c $PING_PACKETS -i $PING_INTERVAL $PING_HOST > /proc/1/fd/1 2>&1" | crontab -
crontab -l

# Start cron in the foreground
exec cron -f