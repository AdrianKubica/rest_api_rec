Installation
============

This part of documentation includes information's about installation process.


To run REST API you simply need to install:
    - git (to fetch rest_api repository files),
    - docker,
    - docker-compose (to spawn containers).

Debian based installation steps
--------------------------------

OS preparation
^^^^^^^^^^^^^^

Simply put in terminal command to update packages:
    - ``$ sudo apt-get update``

Git
^^^

Install git with command:
    - ``$ sudo apt-get install git``
Verify your installation with following command:
    - ``$ git --version``
Go to a directory where you would like to run application and check directory permissions.
Clone git repository to this application.
    - ``$ git clone -b development git@bitbucket.org:AdrianKubica/rest_api.git .``
    or
    - ``$ git clone https://github.com/AdrianKubica/rest_api_rec.git .``
Dont forget to fill ALLOWED_HOSTS setting in services/rest/app/settings.py file according to security reasons, otherwise at production environment you will get Bad Request (400) Error).
    - ``$ vim services/rest/app/settings.py``
Save your changes.

Docker
^^^^^^

The very first step is to remove any default Docker packages from the system before installation Docker on a Linux VPS. Execute commands to remove unnecessary Docker versions.
    - ``$ sudo apt-get purge docker lxc-docker docker-engine docker.io``
Now install some required packages on your system for installing Docker on Ubuntu system. Run the below commands to do this:
    - ``$ sudo apt-get install  curl  apt-transport-https ca-certificates software-properties-common``
Now import dockers official GPG key to verify packages signature before installing them with apt-get. Run the below command on terminal.
    - ``$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add``
After that add the Docker repository on your Ubuntu system which contains Docker packages including its dependencies. You must have to enable this repository to install Docker on Ubuntu.
    - ``$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"``
System is now ready for Docker installation. Run the following command to install Docker community edition on your system.
    - ``$ sudo apt-get install docker-ce``
After successful installation of Docker community edition, the service will start automatically. Use below command to verify service status.
    - ``$ docker --version``
    - ``$ sudo systemctl status docker``
Add the docker group if it doesn't already exist:
    - ``$ sudo groupadd docker``
Add user to docker group:
    - ``$ sudo usermod -aG docker $USER``
Now logout and login again.


Docker-compose
^^^^^^^^^^^^^^

Download the Docker Compose binary into the /usr/local/bin directory with the following curl command:
    - ``$ sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose``
Once the download is complete, apply executable permissions to the Compose binary
    - ``sudo chmod +x /usr/local/bin/docker-compose``
Verify the installation by running the following command which will display the Compose version:
    - ``docker-compose --version``
