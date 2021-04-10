#!/bin/bash
# load common functions
. scripts/common/methods.sh

script_log="/var/log/init.log"

# Create/clear log gile
if [ ! -f script_log ]; then
    mkdir -p $(dirname $script_log)
    truncate -s 0 $script_log
fi

# Redirect stdout ( > ) into a named pipe ( >() ) running "tee"
echo_date "Output of this script will be saved under $script_log"
exec > >(tee -i $script_log)
exec 2> >(tee -ia $script_log >&2)
exec 2>&1


echo_date "Creating log files and directories..."
mkdir -p /var/log 
mkdir -p /var/log/anw
mkdir -p /run/nginx 
touch /var/log/rrd_monitor.log
touch /var/log/cron.log
touch /var/log/messages

echo_date "Fetching initial data..."
/bin/sh            /scripts/rrd_fee-monitor.sh  >> /var/log/rrd_monitor.log
/usr/bin/python3   /scripts/auto-fee-logs.py

echo_date "Starting nginx web-server daemon..."
cat /etc/anw/index.html > /www/index.html
nginx -q 

echo_date "Starng crond scheduling daemon..."
crond -b -L /var/log/cron.log

echo_date "Displaying all logs redirected to '/proc/1/fd/1':"
while true; do
    sleep 1h
done

