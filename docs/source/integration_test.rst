Integration tests
-----------------

There is also TravisCI configuration for Github in .travis.yml file which is able to make integrity tests after each commit pushed to Github. If integrity tests passed, you can for example prepare production ready builds and push it to http://hub.docker/com.
Production ready flow configuration cooperate with:
    - Github,
    - TravisCI which looks for new commits pushed to Github repository,
    - integration tests, if passed then docker builds images and push them to http://hub.docker/com.