#!/bin/sh

echo "Creating log files and directories..."
mkdir -p /var/log 
mkdir -p /var/log/anw
mkdir -p /run/nginx 
touch /var/log/rrd_monitor.log
touch /var/log/cron.log

echo "Fetching initial data..."
/bin/sh            /scripts/rrd_fee-monitor.sh  >> /var/log/rrd_monitor.log
/usr/bin/python3   /scripts/auto-fee-logs.py

echo "Starting nginx web-server daemon..."
cat /etc/anw/index.html > /www/index.html
nginx -q 

echo "Starng crond scheduling daemon..."
crond -b -L /var/log/cron.log

if [ -z "$PS1" ]; then
    echo "Press [CTRL+C] to stop.."
fi 

while true; do
    sleep 60
done

