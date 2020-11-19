# Parlismonitoring

Monitors files published in the PARLIS system from Baden-Württemberg.

View my [docker profile](https://hub.docker.com/u/cubicrootxyz) for containers. 

For more view the subfolders. 

## Installation

### Backend, API, Frontend via Docker

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

### Notifier 

**Requirements:** Python 3.6 or newer, Orator (`pip install orator`)

The notifier emails you all new and interesting files via mail. Run it with a cronjob, your cron file (open with `crontab -e`) should look like this if you want a mail every saturday at 10 am:
```
...
0 10 * * 6 /usr/bin/python3 /storage/scripts/parlis-notifier/run.py
...
```

0. Make sure all requirements are installed
1. copy the `run.py` and the `config.ini` to a local folder
2. edit the config file according to your needs (more in the documentation in the notifier folder)
3. add the `run.py` to your cron file
