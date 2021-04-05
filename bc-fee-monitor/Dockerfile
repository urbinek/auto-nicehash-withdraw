FROM    ubuntu:20.04
LABEL   maintainer=urbinek@gmail.com 

COPY    ./scripts/rrd_fee-monitor.sh           /usr/bin/rrd_fee-monitor.sh
COPY    ./cron/fee-monitor                     /etc/cron.d/fee-monitor
COPY    ./cron/nginx                           /etc/cron.d/nginx
COPY    ./bc-fee-monitor/www/index.html        /www/index.html
COPY    ./nginx/sites-enabled/btc-fee-monitor  /etc/nginx/sites-available/default

RUN     apt update && \
        apt --assume-yes --quiet install rrdtool curl jq cron nginx && \
        apt clean && apt autoclean

RUN     chmod 0644 /etc/cron.d/* && crontab /etc/cron.d/*

EXPOSE  8321/tcp
CMD     ["cron", "-f"]
