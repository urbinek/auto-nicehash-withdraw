FROM    ubuntu:20.04
LABEL   maintainer=urbinek@gmail.com 

RUN     apt update && \
        apt --assume-yes --quiet install rrdtool curl jq cron nginx && \
        apt clean && apt autoclean 

COPY    ./scripts/rrd_fee-monitor.sh  /usr/bin/rrd_fee-monitor.sh
COPY    ./cron/fee-monitor            /etc/cron.d/fee-monitor
COPY    ./www/index.html              /www/index.html
COPY    ./nginx/btc-fee-monitor.conf  /etc/nginx/sites-available/default

RUN     service nginx configtest

RUN     chmod 0644 /etc/cron.d/* && crontab /etc/cron.d/fee-monitor

EXPOSE  8321/tcp
CMD     nginx -q && \
        cron -f

