#!/bin/sh

# Set up the cron job
echo "*/$MINUTES_INTERVAL * * * * /usr/local/bin/python /app/telepinger.py -c $PING_PACKETS -i $PING_INTERVAL $PING_HOST > /proc/1/fd/1 2>&1" | crontab -
crontab -l

# Start cron in the foreground
exec cron -f