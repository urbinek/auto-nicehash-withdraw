# Why

This is completly redundand to have generation done in Docker, but my current sever is running on CentOS 7 wihout which cannot run rrdtool 1.7+

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