FROM    alpine:latest
LABEL   maintainer=urbinek@gmail.com

RUN     apk add --update --no-cache rrdtool curl jq nginx python3 py-pip font-noto fontconfig logrotate
RUN     fc-cache --force --verbose

RUN     pip install --upgrade requests datetime 

COPY    scripts/       /scripts/
COPY    nginx/conf.d   /etc/nginx/conf.d/
COPY    cron/          /etc/crontabs/
COPY    config.json    /etc/anw/
COPY    www/index.html /etc/anw/index.html
COPY    logrotate.d/   /etc/logrotate.d/
COPY    init.sh        /

EXPOSE  80/tcp

CMD     /init.sh