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


Installation
------------

To run REST_API you simply need:

- docker,
- docker-compose

installed and then: `docker-compose up --build -d` will build and run production ready service for you.
There is also possibility to build and run development version with `docker-compose up -f docker-compose.dev.yaml --build -d`.
Development version consists:
- testing environments: simply run `pytest` command using `rest` container,
- linter to check project consistency with PEP8: simply run `flake8` command using `rest` container.

There is also TravisCI configuration for Github which is able to make integrity tests after each commit pushed to Github.
If integrity tests are correct, you can for example prepare production ready builds and send it to http://hub.docker/hub. 

There is also much more options to run robust instances of this project.
You can use for example: `AWS EC2`, `AWS Elastic Beanstalk`, `Docker Swarm`, `Kubernetes` and so on.
If you need more resilience you should also consider load balancing for better UX and service reliability.


Documentation
-------------

Documentation is available at: <https://rest-api-rec.readthedocs.io/en/latest>

Notes
-----

This project is able to make some trade-offs, consider following:
- there is some security settings vulnerabilities which are simply put in docker-compose.yaml files, its for example:
    - user accounts credentials (some user Github account is created for support this project and all credentials are typed in plain text in docker-compose.yaml)
    - database settings
    - django security keys and so on
- keep in mind that its risky to keep and send those information's to Github repository.

You should consider to use Host OS environment variables and load those variables to specific Dockerfiles with:
`ENV VARIABLE_NAME ${VARIABLE_NAME}` syntax.

Questions:
----------

If you have any questions, please send it to: <adrian.kubica.ak@gmail.com>
