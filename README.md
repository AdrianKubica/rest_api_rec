REST_API Project
================

REST API project is released to consume particular http://api.github.com endpoint.
Project is responsible for retrieve information about specified Github user repository.

You can simply run the project with docker-compose:
``` 
>>> docker-compose up --build -d
```

Installation
------------

To run REST_API you simply need:

- docker,
- docker-compose

installed and then: `docker-compose up --build -d` will build and run production ready service for you.
There is also possibility to build and run development version with `docker-compose up -f docker-compose.dev.yaml --build -d`.
Development version consists:
- testing environments, run `pytest` command
- linter to check project consistency with PEP8, run `flake8` command

There is also TravisCI configuration for Github which is able to make integrity tests after each commit to Github.
If integrity tests are correct, you can for example prepare production ready builds on http://hub.docker/hub. 

There is also much more options to run robust instances of this project.
You can use for example: `AWS EC2`, `AWS Elastic Beanstalk`, `Docker Swarm`, `Kubernetes` and so on.


Documentation
-------------

Documentation is available at: <https://rest-api-rec.readthedocs.io/en/latest>

Notes
-----

This project is able to make some trade-offs consider following:
- there is some security settings simply put in docker-compose.yaml files, its for example:
    - user accounts settings (one user Github account is created for support this project)
    - database settings
    - django security keys and so on
- keep in mind that its risky to send those information's to Github repository.
You should for example use host OS environment variables and load those variables to specific Dockerfiles with `ENV VARIABLE_NAME ${VARIABLE_NAME}` syntax.

Questions:
----------

If you have any questions, please send it to: <adrian.kubica.ak@gmail.com>
