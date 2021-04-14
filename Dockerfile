FROM    alpine:latest
LABEL   maintainer=urbinek@gmail.com

RUN     apk add --update --no-cache  curl jq nginx build-base rrdtool-dev python3-dev python3 py-pip font-noto fontconfig logrotate bash 
RUN     fc-cache --force --verbose

RUN     pip install --upgrade pip && \
        pip install --upgrade requests datetime rrdtool

COPY    scripts/       /scripts/
COPY    nginx/conf.d   /etc/nginx/conf.d/
COPY    cron/          /etc/crontabs/
COPY    config.json    /etc/anw/
COPY    www/index.html /etc/anw/index.html
COPY    logrotate.d/   /etc/logrotate.d/
COPY    init.sh        /

EXPOSE  80/tcp

CMD     /init.sh