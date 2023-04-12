#!/bin/sh

echo "==================== Starting telepinger..."

echo "Current ping variables:"
env | grep MINUTES_
env | grep PING_

echo "==================== Setting up cron..."

# Set up the cron job
echo "*/$MINUTES_INTERVAL * * * * /usr/local/bin/python /app/telepinger.py -c $PING_PACKETS -i $PING_INTERVAL $PING_HOST > /proc/1/fd/1 2>&1" | crontab -
crontab -l

echo "==================== Starting cron..."

# Start cron in the foreground
exec cron -f