Welcome to REST API documentation
---------------------------------

Quick start
^^^^^^^^^^^

REST API project is released to consume particular endpoint from http://api.github.com.
This project is responsible for retrieve information about specified Github user repository.

REST API includes:
    - Production ready environment including dedicated docker and docker-compose,
    - Development environment including dedicated docker and docker-compose,
    - Easy to run tests with ``flake8`` linter and ``pytest`` for units testing,
    - Integration test with Github and TravisCI configuration - if tests are passed docker images are pushed to docker hub,
    - Caching abilities with Redis,
    - Gunicorn configuration.

Clone project from bitbucket:

``$ git clone -b development git@bitbucket.org:AdrianKubica/rest_api.git .``

You can run this project with docker-compose:

``$ docker-compose up --build -d``

All you need is docker and docker-compose installed.

Then go to your HOST IP Address and retrieve user repository information using following endpoint:

``/repositories/{owner}/{repository-name}``

Replace {owner} and {repository-name} with appropriate values for truly existing user repository.
Dont forget to fill ALLOWED_HOSTS in services/rest/app/settings.py file according to security reasons, otherwise at production environment you will get Bad Request (400) Error).

You can find working application at: http://3.120.32.14/repositories/kennethreitz/requests

Simply put:
    - ``docker-compose.yaml`` - stands for production ready service
    - ``docker-compose.dev.yaml`` - stands for development ready service


.. toctree::
   :maxdepth: 5
   :caption: Contents:

   contents
   license
   help

Indices and tables
^^^^^^^^^^^^^^^^^^

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
