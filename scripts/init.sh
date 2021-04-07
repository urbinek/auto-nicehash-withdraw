#!/bin/sh

echo "Creating log files and directories..."
mkdir -p /var/log 
mkdir -p /run/nginx 
touch /var/log/rrd_monitor.log
touch /var/log/cron.log
touch /www/btc_exchange_fee.html
ln -s /www/btc_exchange_fee.html /var/log/auto-withdraw.log

echo "Starting nginx web-server..."
nginx -q 

echo "Starng crond scheduling daemon..."
crond -b -L /var/log/cron.log

echo "Fetching initial logs..."
/bin/sh            /scripts/rrd_fee-monitor.sh >> /var/log/rrd_monitor.log
/usr/bin/python3   /scripts/auto-withdraw.py   >> /www/btc_exchange_fee.html

echo "auto-withdraw logs:"
tail -f /var/log/auto-withdraw.log