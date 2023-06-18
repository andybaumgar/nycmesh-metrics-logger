## Setup
- `docker build . -t nycmesh-metrics-logger`
- `docker run -d --name nycmesh-metrics-logger --restart unless-stopped nycmesh-metrics-logger`