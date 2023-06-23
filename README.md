## Setup
- `docker stop nycmesh-metrics-logger`
- `docker remove nycmesh-metrics-logger`
- `docker build . -t nycmesh-metrics-logger`
- `docker run -d --name nycmesh-metrics-logger --restart unless-stopped nycmesh-metrics-logger`

## Reload Single Service
`docker compose up --force-recreate -d --no-deps --build grafana`
`docker compose down grafana`


## Grafana
- uses Mosaic plugin
- need to group by name as well as interval: `SELECT max("outage") FROM "autogen"."devices" WHERE $timeFilter GROUP BY time($__interval), "name"`