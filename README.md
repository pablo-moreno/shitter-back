# Shitter :poop:

![pic](https://gitlab.com/pablo-moreno/shitter-back/badges/master/coverage.svg)
![pic](https://gitlab.com/pablo-moreno/shitter-back/badges/master/pipeline.svg)

## :computer: Development

```sh
docker-compose up
```

You can create or apply migrations from the Django container:

```sh
docker exec -it <container_name> bash
python manage.py makemigrations
python manage.py migrate
```

## :cactus: Environment variables

`VERSION (string)` Application version.

`SECRET_KEY (string)` Project secret key.

`DEBUG: (TRUE|FALSE)` Whether the project is running in DEBUG mode or not. 

`DATABASE_URL (string)` Full database URL in the following format: `postgres://username:password@host:port/dbname`

`REDIS_HOST (IP|URL)` IP or URL address of the Redis instance.

`REDIS_PORT (numeric)` Port of the Redis instance.

`PAGE_SIZE (numeric)` Number of items to paginate by default in the API responses.

## :hammer_and_wrench: Build project

You can build the project image running:

```sh
docker build -t shitter_backend:<version> .
```

## :rocket: Run built project

To run the built project you can run this command:

```sh
docker run -d \
    -p 8000:8000 \
    -v /var/www/shitter_backend/static:/app/static \
    -v /var/www/shitter_backend/media:/app/media \
    -e DEBUG=FALSE \
    -e <environment variable name>=<value> \
    --entrypoint "./runserver.sh" \
    shitter_backend:<version>
```

You must setup as much environment variables as you need.


## :zap: Deploy in Docker Swarm

To deploy in the Docker Swarm all you need to do is to run 

```sh 
sh /deploy/create_services.sh
```

This script creates all the infrastructure you need and expose the port 8000 for nginx to proxy pass.

Then, once you have checked that the project is running as expected, you can configure your nginx.

```sh
sudo sh /deploy/setup_nginx.conf
```

This script will copy all the nginx configuration required, restart your nginx server 
and ask you to update or create your Lets Encrypt certificates.

## :gear: Gitlab CI/CD

Setup CI/CD variables on Settings > CI / CD > Variables.

```sh
CI_PROJECT_BASE_IMAGE=<project base image name>
CI_PROJECT_NAME=<project name>

CI_POSTGRES_DATABASE=<my internal postgres database name>
CI_POSTGRES_PASSWORD=<postgres password>
CI_POSTGRES_USER=<postgres password>

CI_DOCKER_REGISTRY=<my.docker.registry.domain>
CI_REGISTRY_USER=<docker registry user>
CI_REGISTRY_PASSWORD=<docker registry password>
```

There are defined three stages:

- `Test` Runs everytime that any developer pushes code to the repo. 
Runs all the platform tests to ensure that the project works as expected.

- `Build` Runs everytime the code is merged into master, develop, or a tag is created.
Builds the project as a docker image and uploads it to the remote docker registry.

- `Deploy` Runs everytime a tag is created and once test and build stage have been completed.
Notifies the server that an update is available and that needs to set the latest available image.
