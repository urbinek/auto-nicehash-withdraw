#!/bin/sh

echo "Creating log files and directories..."
mkdir -p /var/log 
mkdir -p /run/nginx 
touch /var/log/rrd_monitor.log
touch /var/log/cron.log
touch /var/log/nginx_access.log
touch /var/log/nginx_error.log
touch /www/btc_exchange_fee.html
ln -s /www/btc_exchange_fee.html /var/log/auto-withdraw.log

echo "Starting nginx web-server..."
nginx -q 

echo "Starng crond scheduling daemon..."
crond -b -L /var/log/cron.log

echo "auto-withdraw logs:"
tail -f /var/log/auto-withdraw.log