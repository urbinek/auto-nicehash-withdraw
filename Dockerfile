FROM    alpine:latest
LABEL   maintainer=urbinek@gmail.com

RUN     apk add --update rrdtool curl jq nginx python3 py-pip
RUN     pip install --upgrade requests datetime 

COPY    scripts/        /scripts/
COPY    www/            /www/
COPY    nginx/          /etc/nginx/conf.d/
COPY    cron/           /etc/crontabs/
COPY    config.json     /


EXPOSE  80/tcp

CMD     /scripts/init.sh
