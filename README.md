# auto-nicehash-withdraw

Simple python3 script for automated withdraws from NiceHash wallet

## API

### API key requirements

In order to provide scurity API key should be restricted with minimal access containing:

- aaa
- bbb
- ccc

### API rest-client

API rest-client is fetched from <https://github.com/nicehash/rest-clients-demo>

## Build

```Bash
cd auto-nicehash-withdraw/fee-monitor
docker build --no-cache -t urbinek/bc-fee-monitor:latest .
docker push urbinek/bc-fee-monitor:latest
```

## Deploy

```Bash
docker stack deploy --compose-file docker-compose.yml btc-monitor
```

## NiceHash fees

### Service details

<https://www.nicehash.com/support/general-help/nicehash-service/fees>

### Life Blockchain fees demo

<https://nginx.urbinek.eu/auto-nicehash-withdraw/fee-monitor/>

![Daily](https://nginx.urbinek.eu/auto-nicehash-withdraw/fee-monitor/bc_btc_fee-day.png)
![Weekly](https://nginx.urbinek.eu/auto-nicehash-withdraw/fee-monitor/bc_btc_fee-week.png)
![Monthly](https://nginx.urbinek.eu/auto-nicehash-withdraw/fee-monitor/bc_btc_fee-month.png)

