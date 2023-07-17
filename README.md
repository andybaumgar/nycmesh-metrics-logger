## Influx and Grafana Setup
- customize `docker-compose-example.yml`
- `docker compose up -d`

## Logger Setup
- add .env file
- `sudo ./ci.sh` 

## Reload Single Docker Service
`docker compose up --force-recreate -d --no-deps --build grafana`
`docker compose down grafana`

## Grafana
- uses Mosaic plugin
- need to group by name as well as interval: `SELECT max("outage") FROM "autogen"."devices" WHERE $timeFilter GROUP BY time($__interval), "name"`
