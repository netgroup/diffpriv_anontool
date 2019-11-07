Follow these steps to launch docker containers for simulate application:

1) Install docker

2) Install docker-compose

3) Open terminal and place in project folder

4) To create containers with docker-compose use command:
	- docker-compose up -d --build                          (ONLY FOR FIRST RUN)
	- docker-compose up -d --build --force-recreate -t 0

5) To shutdown containers with docker-compose use command:
	- docker-compose down
