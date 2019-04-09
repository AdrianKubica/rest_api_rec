Notes
-----

This project is able to make some trade-offs, consider following:
    - there is some security settings vulnerabilities which are simply put in Dockerfile.yaml / docker-compose.yaml files, its for example:
        - user accounts credentials (some user Github account is created for support this project and all credentials are typed in plain text in docker-compose.yaml),
        - django ALLOWED_HOSTS (you need to fill that value in ``services/rest/app/settings.py`` file according to security reasons, otherwise at production you will get ``Bad Request (400) Error``),
        - django security key and so on.
    - keep in mind that its risky to keep and send those information's to Github repository.

You should consider to use Host OS environment variables and load those variables to specific Dockerfile's with:
``ENV VARIABLE_NAME ${VARIABLE_NAME}`` syntax. In more complex project you should also consider to split your settings.py files for production and development environments.

Repository also includes some static files which looks like unnecessary files.
Those files can be used to switch API versions in Django REST Framework to ``Browsable API`` and for the sake of consistency are included in repository.

If for some reasons advanced features of nginx are unnecessary you can also consider WhiteNoise for serving ``Browsable API`` static files.

Also if you are bitbucket user you should consider to change TravisCI for Bitbucket Pipelines or CircleCI.