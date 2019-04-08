Testing
^^^^^^^


- testing environments: simply run ``pytest`` command using rest container, so you can run tests with following commands:
        go to root project directory and run build command: docker build -t adriankubica/rest_api -f ./services/rest/Dockerfile.dev ./services/rest
        to check if tests are passing use run command: docker run adriankubica/rest_api sh -c "flake8 && pytest && pytest --cov" rest_api uses flake8 linter to check project consistency with PEP8: simply run flake8 command using rest container.

There is also TravisCI configuration for Github in .travis.yml file which is able to make integrity tests after each commit pushed to Github. If integrity tests passed, you can for example prepare production ready builds and push it to http://hub.docker/com. This repository contains also production ready flow configuration with:

    Github,
    TravisCI which looks for new commits pushed to Github repository,
    integration tests, if passed then docker builds images and push them to http://hub.docker/com.

You can find working application at: http://3.120.32.14/repositories/kennethreitz/requests

There is also much more options to run robust instances of this project. You can use for example: AWS EC2, AWS Elastic Beanstalk, Docker Swarm, Kubernetes and so on. If you need more resilience you should also consider load balancing for better UX and service reliability.

Simply put:

    docker-compose.yaml - stands for production ready service
    docker-compose.dev.yaml - stands for development ready service
