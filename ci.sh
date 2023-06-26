git pull
docker build . -t nycmesh-metrics-logger
docker stop nycmesh-metrics-logger
docker remove nycmesh-metrics-logger
docker run -d --name nycmesh-metrics-logger --restart unless-stopped nycmesh-metrics-logger