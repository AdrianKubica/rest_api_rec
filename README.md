REST_API
========

Quick start
-----------

REST API project is released to consume particular endpoint from http://api.github.com.
This project is responsible for retrieve information about specified Github user repository.

REST API includes:
- Production ready environment including dedicated docker and docker-compose,
- Development environment including dedicated docker and docker-compose,
- Easy to run tests with `flake8` linter and `pytest` for units testing,
- Integration test with Github and TravisCI configuration - if tests are passed docker images are pushed to docker hub,
- Caching abilities with Redis,
- Gunicorn configuration.

You can run this project with `docker-compose`:
``` 
>>> docker-compose up --build -d
```

Then go to your HOST IP address and retrieve user repository information using following endpoint:

- `/repositories/{owner}/{repository-name}`

Replace `{owner}` and `{respository-name}` with appropriate values for truly existing user repository.
Dont forget to fill ALLOWED_HOSTS setting in `services/rest/app/settings.py` file according to security reasons, otherwise at production environment you will get `Bad Request (400) Error`).


You can find working application at: http://3.120.32.14/repositories/kennethreitz/requests


Simply put:
- `docker-compose.yaml` - stands for production ready service
- `docker-compose.dev.yaml` - stands for development ready service

Installation
------------

To run REST_API you simply need to install (check documentation for more details at <https://rest-api-rec.readthedocs.io/en/latest>):

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


You can also use your IDE ability to run automated tests.

There is also TravisCI configuration for Github in `.travis.yml` file which is able to make integrity tests after each commit pushed to Github.
If integrity tests passed, you can for example prepare production ready builds and push it to http://hub.docker/com.
Production ready flow configuration cooperate with:
- Github,
- TravisCI which looks for new commits pushed to Github repository,
- integration tests, if passed then docker builds images and push them to http://hub.docker/com.

There is also much more options to run robust instances of this project.
You can use for example: `AWS EC2`, `AWS Elastic Beanstalk`, `Docker Swarm`, `Kubernetes` and so on.
If you need more resilience you should also consider load balancing for better UX and service reliability.


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

Repository also includes some static files which looks like unnecessary files.
Those files can be used to switch API versions in Django REST Framework to `Browsable API` and for the sake of consistency are included in repository.


Questions:
----------

If you have any questions, please send it to: <adrian.kubica.ak@gmail.com>
