# AnonTool

## Introduction
In database systems one of the possible solutions to protect our data is to anonymize it; but performing a proper 
anonymization is a really complex process. The majority of existing solutions uses the common techniques to "sanitize" 
the data: detecting identifiers and quasi-identifiers, properly aggregating and/or removing them. These solutions do not 
guarantee complete anonymization, so they cannot be the best choise.
Recently, a new mechanism to anonymize data, the *Differential Privacy*, has becoming the dominant way to perform 
data anonymization, because it provides a quantified privacy level with a rigorous mathematical foundation.
Our tool is based on this technique. With this tool we target to simplify the technical details and provide an 
easy-to-use and easy-to-deploy system to anonymously release your data.

## Description
This project implements a Web service to provide anonymized queries on statistical data. In particular, when deployed,
through HTTP requests, it allows to upload files on which users can make queries. It provides a Web interface to make
use of Google C++ library [differential-privacy][google_diff_priv].

### System requirements:
- Architecture: 64-bit host or virtual machine
- OS:           Linux

### File requirements:
- file extension **_must_** be .csv,
- each entry **_must_** have a **_unique_** ID (multiple occurences of the same ID are not allowed),
- there **_must_** be **_at least_** a numeric column on which it is possible to compute queries,
- numeric values **_must_** be in range \[0, 150\].

An example can be found in *differential-privacy-master/differential-privacy/operations/data.csv*.

### Query requirements:
- only **_SELECT_** queries are supported with single statistical operations. Allowed operations are the followings:
    - **_COUNT_**,
    - **_SUM_**,
    - **_AVG_**,
    - **_VAR_**,
    - **_STDEV_**,
    - **_MAX_**,
    - **_MIN_**,
- only operations on a single column are permitted and the choosen column must contain only numbers,
- queries **_cannot_** contain **_WHERE_**, **_HAVING_**, **_ORDER BY_** clauses.

Some examples can be found in *queries_examples.json*.

### Working features:
- If you want to change the IP addresses or ports, you have to modify the file *docker-compose.yml*.
- In the file *Const.py*, you can find all the system parameters, such as HTTP routes, etc.
  \[*WARNING: Be careful when changing differential privacy parameters*\]
  
## Build

Follow these steps to launch docker containers for simulate application:
1. Install docker
2. Install docker-compose
3. Open terminal and place in project folder
    1. (*OPTIONAL*) In order to change server IP address and port in the container, modify *diff_priv_server* fields in
    *docker-compose.yml*
    2. in *DiffPrivServer.py* defaults are set to *172.25.0.2:5002*
4. To create containers with docker-compose use command:
	- *docker-compose up -d --build                          (ONLY FOR FIRST RUN)*
	- *docker-compose up -d --build --force-recreate -t 0*
    - [*NOTE*] If docker raises some errors:
        - retry command using **_sudo_**
        - type on terminal *sudo service docker start* and retry command
5. Open the browser and choose to go to:
    - [172.25.0.2:5002] to see all the available HTTP routes
    - [172.25.0.2:5002/index] to use the tool

6) To shutdown containers with docker-compose use command:
	- *docker-compose down*

### Possible errors

1. *ERROR: for diffprivtool_diff_priv_server_1
   Cannot start service diff_priv_server: driver failed programming external connectivity on endpoint
   diffprivtool_diff_priv_server_1 (...):
   Error starting userland proxy: listen tcp 0.0.0.0:5002: bind: address already in use*
   
   **_Solution_**:
   - on host command line, type *lsof -i :5002*
   - if some process is using the port, type *kill \[PID\]* to kill it

2. *EXISTING FILES*
   - In order to remove existing files (*.csv*, *logs*, *users_list*) from the host machine, delete **_diffpriv_server_** folder in
   */var/lib/docker/volumes/*


   
[google_diff_priv]: https://github.com/google/differential-privacy
[172.25.0.2:5002]: http://172.25.0.2:5002
[172.25.0.2:5002/index]: http://172.25.0.2:5002/index