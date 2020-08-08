#!/bin/bash

docker network create -d overlay shitter

docker volume create shitter_db -d local-persist -o mountpoint=/var/www/shitter/db
docker volume create shitter_static -d local-persist -o mountpoint=/var/www/shitter/static
docker volume create shitter_media -d local-persist -o mountpoint=/var/www/shitter/media

docker service create \
  --name shitter_postgres \
  --replicas 1 \
  --env "POSTGRES_USER=${SHITTER_DB_USER}" \
  --env "POSTGRES_PASSWORD=${SHITTER_DB_PASSWORD}" \
  --env "POSTGRES_DB=shitter_backend" \
  --mount src=shitter_db,dst=/var/lib/postgresql/data \
  --network shitter \
  postgres:latest


docker service create \
  --name shitter_redis \
  --replicas 1 \
  --mount src=shitter_db,dst=/var/lib/postgresql/data \
  --network shitter \
  redis:latest


docker service create \
  --name shitter_backend \
  --replicas 3 \
  --env "DATABASE_URL=postgres://$SHITTER_DB_USER:$SHITTER_DB_PASSWORD@shitter_postgres:5432/shitter_backend" \
  --publish "8000:8000" \
  --network shitter \
  --mount src=shitter_media,dst=/app/media \
  --mount src=shitter_static,dst=/app/static \
  --entrypoint "./runserver.sh" \
  --with-registry-auth \
  registry.gitlab.com/pablo-moreno/shitter-back:1.0.0


docker service create \
  --name shitter_frontend \
  --replicas 3 \
  --publish "8282:80" \
  --with-registry-auth \
  registry.gitlab.com/pablo-moreno/shitter-front:0.1.0-rc1
