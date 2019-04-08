Notes
-----

This project is able to make some trade-offs, consider following:
    - there is some security settings vulnerabilities which are simply put in Dockerfile.yaml / docker-compose.yaml files, its for example:
        - user accounts credentials (some user Github account is created for support this project and all credentials are typed in plain text in docker-compose.yaml),
        - django ALLOWED_HOSTS (you need to fill that value in ``services/rest/app/settings.py`` file according to security reasons, otherwise at production you will get ``Bad Request (400) Error``),
        - django security keys, django DEBUG MODE and so on
    - keep in mind that its risky to keep and send those information's to Github repository.

You should consider to use Host OS environment variables and load those variables to specific Dockerfile's with:
``ENV VARIABLE_NAME ${VARIABLE_NAME}`` syntax. In more complex project you should also consider to split your settings.py files for production and development environments.
