# fraud finder

fraudfinder is a simple web application / api which compares two input Persons and provides the probability that these two persons are the same & records the detection result in a database.

## Quick Start

Build local container
```bash
docker build docker/ -t fraud_finder:local 
```
Pull From Repo



### Determine local IP Address
Verify the local IP address of the Docker host, this is required to allow communication via the local authenticaiton server

```bash
ifconfig 

# Example
enp60s0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.18  netmask 255.255.255.0  broadcast 192.168.1.255
```

### Start Authenticaiton Server

mkdir -p $(pwd)/easyauth-vol

docker run --name easyauth \
    -e DB_TYPE=sqlite \
    -e DB_NAME=auth \
    -e DB_LOCAL_PATH=/mnt/easyauth \
    -e ISSUER=EasyAuth \
    -e SUBJECT=EasyAuthAuth \
    -e AUDIENCE=EasyAuthApis \
    -e KEY_PATH=/mnt/easyauth \
    -e KEY_NAME=test_key \
    -v $(pwd)/easyauth-vol:/mnt/easyauth \
    -p 8220:8220 \
    -d joshjamison/easyauth:v0.0.0

#### Pull Adminstrator Password from logs

```bash
$ docker logs easyauth[2021-04-23 15:36:07 +0000] [6] [INFO] Starting gunicorn 20.1.0[2021-04-23 15:36:07 +0000] [6] [INFO] Listening at: http://0.0.0.0:8220 (6)
[2021-04-23 15:36:07 +0000] [6] [INFO] Using worker: uvicorn.workers.UvicornWorker
[2021-04-23 15:36:07 +0000] [8] [INFO] Booting worker with pid: 8
[2021-04-23 15:36:07 +0000] [8] [INFO] Started server process [8]
[2021-04-23 15:36:07 +0000] [8] [INFO] Waiting for application startup.
04-23 15:36 EasyAuthServer ERROR    detected new EasyAuth server, created admin user with password: cwmykhzj
[2021-04-23 15:36:09 +0000] [8] [INFO] Application startup complete.
```

### Start Fraud Finder Service 

#### Prepare Container environment

```bash
mkdir -p $(pwd)/fraud-finder-vol

```
Copy public generated public RSA key from auth server into fraud-finder-vol

```bash
cp $(pwd)/easyauth-vol/test_key.pub $(pwd)/fraud-finder-vol
```

#### Start Fraud Finder Container
```bash

docker run --name fraud-finder \
     -v $(pwd)/fraud-finder-vol:/mnt/database/ \
     -e DB_LOCATION=/mnt/database \
     -e KEY_PATH=/mnt/database \
     -e KEY_NAME=test_key \
     -e TOKEN_SERVER_PATH='http://192.168.1.18:8220/auth/token' \
     -d fraud_finder:local
```

### Permissions 
- Fraud Finder will allow users within the 'administrators' group to the API / GUI. 
- Fraud Finder will communicate with the Authenticaiton server for login requests to pull valid tokens. 

### Stack
- FastAPI - Web Framework
- Gunicorn / Uvicorn - ASGI web server
- EasyAuth - JWT Authentication / Authorization framework
- EasyAdmin - GUI FrontEnd Generator 
- aiopyql - Database & Caching
