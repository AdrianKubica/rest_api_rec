Welcome to REST API documentation
---------------------------------

Quick start
^^^^^^^^^^^

REST API project is released to consume particular endpoint from http://api.github.com.
This project is responsible for retrieve information about specified Github user repository.

You can simply run this project with docker-compose:

>>> docker-compose up --build -d

All you need is simply docker and docker-compose installed.

Then go to your HOST IP Address and retrieve user repository information using following endpoint: /repositories/{owner}/{repository-name}.
Replace {owner} and {repository-name} with appropriate values for truly existing user repository.
Dont forget to fill ALLOWED_HOSTS in services/rest/app/settings.py file according to security reasons, otherwise at production environment you will get Bad Request (400) Error).


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
