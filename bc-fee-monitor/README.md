# Quickies

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
