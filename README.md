REST_API
========

REST API project is released to consume particular endpoint from http://api.github.com.
This project is responsible for retrieve information about specified Github user repository.

You can simply run this project with `docker-compose`:
``` 
>>> docker-compose up --build -d
```

Then go to your HOST IP address and retrieve user repository information using following endpoint:
`/repositories/{owner}/{repository-name}`. Replace `{owner}` and `{respository-name}` with appropriate values for truly existing user repository.
Dont forget to fill ALLOWED_HOSTS setting in `services/rest/app/settings.py` file according to security reasons, otherwise at production environment you will get `Bad Request (400) Error`).


Installation
------------

To run REST_API you simply need to install:

- git (to get `rest_api` repository files),
- docker,
- docker-compose (to spawn containers).

Then run `docker-compose up --build -d` command to build and run production ready service for you.
There is also possibility to build and run development environment with `docker-compose up -f docker-compose.dev.yaml --build -d`.
Development environment consists:
- testing environments: simply run `pytest` command using `rest` container, so you can run tests with following commands:
    - go to root project directory and run `build` command: `docker build -t adriankubica/rest_api -f ./services/rest/Dockerfile.dev ./services/rest`
    - to check if tests are passing use `run` command: `docker run adriankubica/rest_api sh -c "flake8 && pytest && pytest --cov"`
`rest_api` uses `flake8` linter to check project consistency with PEP8: simply run `flake8` command using `rest` container.

There is also TravisCI configuration for Github in `.travis.yml` file which is able to make integrity tests after each commit pushed to Github.
If integrity tests passed, you can for example prepare production ready builds and push it to http://hub.docker/com.
This repository contains also production ready flow configuration with:
- Github,
- TravisCI which looks for new commits pushed to Github repository,
- integration tests, if passed then docker builds images and push them to http://hub.docker/com.

You can find working application at: <http://3.120.32.14/repositories/kennethreitz/requests>   

There is also much more options to run robust instances of this project.
You can use for example: `AWS EC2`, `AWS Elastic Beanstalk`, `Docker Swarm`, `Kubernetes` and so on.
If you need more resilience you should also consider load balancing for better UX and service reliability.

Simply put:
- docker-compose.yaml - stands for production ready service
- docker-compose.dev.yaml - stands for development ready service


Documentation
-------------

Documentation is available at: <https://rest-api-rec.readthedocs.io/en/latest>

Notes
-----

This project is able to make some trade-offs, consider following:
- there is some security settings vulnerabilities which are simply put in Dockerfile.yaml / docker-compose.yaml files, its for example:
    - user accounts credentials (some user Github account is created for support this project and all credentials are typed in plain text in docker-compose.yaml),
    - django ALLOWED_HOSTS (you need to fill that value in `services/rest/app/settings.py` file according to security reasons, otherwise at production you will get `Bad Request (400) Error`),
    - django security keys, django DEBUG MODE and so on
- keep in mind that its risky to keep and send those information's to Github repository.

You should consider to use Host OS environment variables and load those variables to specific Dockerfile's with:
`ENV VARIABLE_NAME ${VARIABLE_NAME}` syntax. In more complex project you should also consider to split your settings.py files for production and development environments.


Questions:
----------

If you have any questions, please send it to: <adrian.kubica.ak@gmail.com>
