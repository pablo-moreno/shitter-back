# Shitter :poop:

![pic](https://gitlab.com/pablo-moreno/shitter-back/badges/master/coverage.svg)
![pic](https://gitlab.com/pablo-moreno/shitter-back/badges/master/pipeline.svg)


This is a Django setup project, configured with CI/CD for testing and auto-deployment.

## Gitlab Environment Variables

Setup CI/CD variables on Settings > CI / CD > Variables.


```sh
CI_PROJECT_BASE_IMAGE=<project base image name>
CI_PROJECT_NAME=<project name>

CI_POSTGRES_DATABASE=<my internal postgres database name>
CI_POSTGRES_PASSWORD=<postgres password>
CI_POSTGRES_USER=<postgres password *>

CI_DOCKER_REGISTRY=<my.docker.registry.domain>
CI_REGISTRY_USER=<docker registry user*>
CI_REGISTRY_PASSWORD=<docker registry password *>
```

Those marked with asterisk (*) require to be masked and protected.

To do so, just run the command:

`echo -n <variable_value> | base64`
