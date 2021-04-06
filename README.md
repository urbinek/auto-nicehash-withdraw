# auto-nicehash-withdraw

Simple python3 script for automated withdraws from NiceHash wallet

## API permissions


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

