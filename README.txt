Follow these steps to launch docker containers for simulate application:

1) Install docker

2) Install docker-compose

3) Open terminal and place in project folder

# 4) Create docker images with command:
#	- docker build -f CloudProvider_Dockerfile -t cloud_provider . && docker build -f Company_Dockerfile -t company . && docker build -f Client_Dockerfile -t client .

4) To create containers with docker-compose use command:
	- docker-compose up -d --build                          (ONLY FOR FIRST RUN)
	- docker-compose up -d --build --force-recreate -t 0
   Otherwise create containers with command:
	docker run -ti --name cloud_provider cloud_provider && docker run -ti --name company company && docker run -ti -p 5002:5002 --name client client

5) To shutdown containers with docker-compose use command:
	- docker-compose down
   Otherwise use Ctrl+C to stop each container
