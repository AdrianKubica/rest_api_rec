Testing
^^^^^^^

To run units test go to project root directory and simply put in development environment following command:
    - ``$ docker build -t adriankubica/rest_api -f ./services/rest/Dockerfile.dev ./services/rest``
Next to check if tests are passing, use command:
    - ``docker run adriankubica/rest_api sh -c "flake8 && pytest && pytest --cov"``

This application uses ``flake8`` linter to check project consistency with PEP8 and ``pytest`` for units tests.
You can simply run ``flake8`` command and ``pytest`` command inside development ``rest`` container.

You can also use your IDE ability to run automated tests.
