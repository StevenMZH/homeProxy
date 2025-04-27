# Run Servers

## Frontend

## Backend
`daphne backend.asgi:application`

## Proxy

## PostgreSQL

## Redis
For windows, run on the WSL:

- Open Redis Config File: `sudo nano /etc/redis/redis.conf`
- Run server: `sudo service redis-server start`
- Restart server: `sudo service redis-server restart`
- Stop server: `shutdown` `sudo systemctl stop redis`