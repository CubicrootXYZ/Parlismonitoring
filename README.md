# Parlismonitoring

Monitors files published in the PARLIS system from Baden-Württemberg.

View my [docker profile](https://hub.docker.com/u/cubicrootxyz) for containers. 

For more view the subfolders. 

## Installation

For more details on how to manually setup the single parts, visit the corresponding subfolders. 

I recommend using docker for the backend and api. You'll need 3 containers, use docker-compose to manage them. 

Here a sample `docker-compose.yml`:

```
version: '2'

services:
  parlismonitoring-backend:
    image: 'cubicrootxyz/parlismonitoring-backend'
    volumes:
      - /yourpath/config.ini:/opt/app/config.ini
    restart: always
  parlismonitoring-api:
    image: 'cubicrootxyz/parlismonitoring-api'
    volumes:
      - /yourpath/parlismonitoring/config.ini:/opt/app/config.ini
    restart: always
    ports:
      - "6021:8080"
  redis:
    image: 'redis'
    ports:
      - "6379:6379"
    restart: always
```

For more details on the docker containers visit my [docker profile](https://hub.docker.com/u/cubicrootxyz).
