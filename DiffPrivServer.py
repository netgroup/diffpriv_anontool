from flask import Flask, render_template, request

import Const
import CSVHandler as csvh
import FuncUtils as fu
import QueryHandler as qh

import os
import argparse
import json

################# FLASK SERVER #################
app = Flask(__name__, root_path=Const.ROOT_PATH + Const.FLASK_ROOT_PATH)  # Create a Flask WSGI application


@app.route('/', methods=[Const.GET])
def index():
    if request.method == Const.GET:
        return render_template(Const.INDEX + '.html')
    else:
        return Const.NO_METHOD


@app.route('/' + Const.SEND_CSV, methods=[Const.POST])
def send_csv():
    if request.method == Const.POST:
        # Get file from request content
        file_name = request.files['file']
        fu.log(fu.get_current_time() + '[' + Const.SEND_CSV + ' ' + request.method +
               '] Received request to store csv file:' + str(file_name) + '\n')
        # Store file
        return csvh.add_file(file_name), Const.OK
    else:
        fu.log(fu.get_current_time() + '[' + Const.SEND_CSV + ' ' + request.method +
               '] Received request with not allowed method\n')
        return Const.NO_METHOD


@app.route('/' + Const.LIST, methods=[Const.GET])
def get_csv_list():
    if request.method == Const.GET:
        if os.path.isdir(Const.ROOT_PATH + Const.CSV_FILES_PATH):
            return json.dumps({Const.LIST: os.listdir(Const.ROOT_PATH + Const.CSV_FILES_PATH)}), Const.OK
    else:
        fu.log(fu.get_current_time() + '[' + Const.LIST + ' ' + request.method +
               '] Received request with not allowed method\n')
        return Const.NO_METHOD


@app.route('/' + Const.QUERY, methods=[Const.POST])
def send_query():
    if request.method == Const.POST:
        # Decrypt data received from Cloud Provider
        content = request.get_json()
        user_id = content[Const.ID]
        file_name = content[Const.FILE]
        query = content[Const.QUERY]
        epsilon = float(content[Const.EPSILON])
        fu.log(fu.get_current_time() + '[' + Const.QUERY + ' ' + request.method + '] Received from ' + user_id +
               ' request for query:' + query + ' from ' + file_name + ' with epsilon = ' + str(epsilon) + '\n')
        return qh.check_query(user_id, file_name, query, epsilon), Const.OK
    else:
        fu.log(fu.get_current_time() + '[' + Const.QUERY + ' ' + request.method +
               '] Received request with not allowed method\n')
        return Const.NO_METHOD


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Flask server for differential privacy queries',
                                     usage='DiffPrivServer.py -a [IPADDR] -p [PORT] (default: -a 17.25.0.2 -p 5002)')
    parser.add_argument('-a', type=str, help='The IP address of the server', default='172.25.0.2')
    parser.add_argument('-p', type=int, help='The port of the server', default=5002)
    args = parser.parse_args()
    if fu.is_valid_ip(args.a):
        os.mkdir(Const.ROOT_PATH + Const.LOG_FILES_PATH)
        os.mkdir(Const.ROOT_PATH + Const.CSV_FILES_PATH)
        os.mkdir(Const.ROOT_PATH + Const.USERS_LIST_PATH)
        app.run(host=args.a, port=str(args.p))
    else:
        print Const.INVALID_IP
