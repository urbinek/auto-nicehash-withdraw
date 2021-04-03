FROM    ubuntu:20.04
LABEL   maintainer=urbinek@gmail.com 

COPY    ./scripts/rrd_fee-monitor.sh /rrd_fee-monitor.sh
COPY    ./cron/fee-monitor /etc/cron.d/fee-monitor

RUN     apt update && \
        apt --assume-yes --quiet install rrdtool curl jq cron && \
        apt clean && apt autoclean

RUN     chmod 0644 /etc/cron.d/fee-monitor && crontab /etc/cron.d/fee-monitor

CMD     ["cron", "-f"]
