This project implements a Web service to provide anonymized queries on statistical data. In particular, when deployed,
it allows to upload files on which users can make queries. It provides a Web interface to make use of Google C++ library
"differential-privacy" (https://github.com/google/differential-privacy).

SYSTEM REQUIREMENTS:
- Architecture: 64-bit host or virtual machine
- OS:           Linux

FILE REQUIREMENTS:
- file extension MUST be .csv
- each entry MUST have a UNIQUE ID (multiple occurences of the same ID are not allowed)
- there MUST be AT LEAST a numeric column on which it is possible to compute queries
- numeric values and bounds MUST be in range [-100000000, 100000000]
An example can be found in "differential-privacy-master/differential-privacy/operations/data.csv"

QUERIES REQUIREMENTS:
- only SELECT queries are supported with single statistical operations. Allowed operations are the followings:
    - COUNT
    - SUM
    - AVG
    - VAR
    - STDEV
    - MAX
    - MIN
- only operations on a single column are permitted and the choosen column must contain only numbers
- it is possible to set lower and upper bounds in WHERE clause
Some examples can be found in "queries_examples.json"


################ BUILD ################

Follow these steps to launch docker containers for simulate application:

1) Install docker

2) Install docker-compose

3) Open terminal and place in project folder

3.1) (OPTIONAL) In order to change server IP address and port in the container, modify "diff_priv_server" fields in
    docker-compose.yml
    - in DiffPrivServer.py defaults are set to 172.25.0.2:5002

4) To create containers with docker-compose use command:
	- docker-compose up -d --build                          (ONLY FOR FIRST RUN)
	- docker-compose up -d --build --force-recreate -t 0

5) To shutdown containers with docker-compose use command:
	- docker-compose down


POSSIBLE ERRORS

1. ERROR: for diffprivtool_diff_priv_server_1
   Cannot start service diff_priv_server: driver failed programming external connectivity on endpoint
   diffprivtool_diff_priv_server_1 (...):
   Error starting userland proxy: listen tcp 0.0.0.0:5002: bind: address already in use

   SOLUTION: - on host command line, type "lsof -i :5002"
                - if some process is using the port, type "kill [PID]" to kill it

2. EXISTING FILES
   In order to remove existing files (.csv, logs, users_list) from host machine, delete "diffpriv_server" folder in
   /var/lib/docker/volumes/