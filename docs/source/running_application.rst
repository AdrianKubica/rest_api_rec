Running application
^^^^^^^^^^^^^^^^^^^

Run ``docker-compose up --build -d`` command to build and run production ready service for you:
    - ``docker-compose up --build -d``
There is also possibility to build and run development environment with command:
    - ``docker-compose up -f docker-compose.dev.yaml --build -d``

Your application is running.

Development environment includes:
    - testing environment with ``flake8`` linter and ``pytest`` unit tests,
    - integration tests workflow with TravisCI and Github

There is also much more options to run robust instances of this project. You can use for example: AWS EC2, AWS Elastic Beanstalk, Docker Swarm, Kubernetes and so on. If you need more resilience you should also consider load balancing for better UX and service reliability.