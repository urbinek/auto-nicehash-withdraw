FROM    alpine:latest
LABEL   maintainer=urbinek@gmail.com

RUN     apk add rrdtool curl jq nginx

COPY    scripts/        /scripts/
COPY    cron/           /cron/
COPY    www/            /www/
COPY    nginx/          /etc/nginx/conf.d/
COPY    config.json     /config.json

RUN     service nginx configtest
RUN     cat /cron/* >> /etc/crontabs/root

EXPOSE  80/tcp

CMD     nginx -q && \
        crond -f

