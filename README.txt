Follow these steps to launch docker containers for simulate application:

1) Install docker

2) Install docker-compose

3) Open terminal and place in project folder

3.1) (OPTIONAL) In order to change server IP address and port in the container, modify "diff_priv_server" fields in docker-compose.yml
    - in DiffPrivServer.py defaults are set to 172.25.0.2:5002

4) To create containers with docker-compose use command:
	- docker-compose up -d --build                          (ONLY FOR FIRST RUN)
	- docker-compose up -d --build --force-recreate -t 0

5) To shutdown containers with docker-compose use command:
	- docker-compose down

Possible Errors

1. ERROR: for diffprivtool_diff_priv_server_1
   Cannot start service diff_priv_server: driver failed programming external connectivity on endpoint
   diffprivtool_diff_priv_server_1 (...):
   Error starting userland proxy: listen tcp 0.0.0.0:5002: bind: address already in use

   SOLUTION: - on host command line, type "lsof -i :5002"
                - if some process is using the port, type "kill [PID]" to kill it