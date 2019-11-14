from flask import Blueprint, Flask, render_template, request
from flask_restplus import Resource, Api

import Const
import CSVHandler as csvh
import FuncUtils as fu
import QueryHandler as qh

import os
import argparse
import json

################# FLASK SERVER #################
app = Flask(__name__, root_path=Const.ROOT_PATH + Const.FLASK_ROOT_PATH)  # Create a Flask WSGI application
api = Api(app)

ns = api.namespace('', description='APIs to communicate with server')

csv_parser = api.parser()
csv_parser.add_argument(Const.FILE, type=file, location=Const.FILE)

query_parser = api.parser()
query_parser.add_argument(Const.ID, type=str)
query_parser.add_argument(Const.FILE, type=str)
query_parser.add_argument(Const.EPSILON, type=float)
query_parser.add_argument(Const.QUERY, type=str)


@ns.route('/index')
class Index(Resource):

    def get(self):
        """
        Show index page
        :return: Index page
        """
        return render_template(Const.INDEX + '.html')


@ns.route('/' + Const.SEND_CSV)
class SendCSV(Resource):

    @api.expect(csv_parser)
    @api.response(Const.OK, 'File successfully stored')
    @api.response(Const.INVALID_FILE[1], Const.INVALID_FILE[0])
    @api.response(Const.FILE_EXIST[1], Const.FILE_EXIST[0])
    @api.response(Const.NO_NUMERIC[1], Const.NO_NUMERIC[0])
    def post(self):
        """
        Store sent file
        :return: Success or fail
        """
        # Get file from request content
        file_name = request.files[Const.FILE]
        fu.log(fu.get_current_time() + '[' + Const.SEND_CSV + ' ' + request.method +
               '] Received request to store csv file:' + str(file_name) + '\n')
        # Store file
        result = csvh.add_file(file_name)
        return result[0], result[1]


@ns.route('/' + Const.LIST)
class GetList(Resource):

    @api.response(Const.OK, 'File successfully stored')
    @api.response(Const.NO_CSV_DIR[1], Const.NO_CSV_DIR[0])
    def get(self):
        """
        Send the list of csv files stored into the server
        :return: The list of stored csv files
        """
        # Check if there are csv files
        if os.path.isdir(Const.ROOT_PATH + Const.CSV_FILES_PATH):
            return json.dumps({Const.LIST: os.listdir(Const.ROOT_PATH + Const.CSV_FILES_PATH)}), Const.OK
        else:
            return Const.NO_CSV_DIR[0], Const.NO_CSV_DIR[1]


@ns.route('/' + Const.QUERY)
class Query(Resource):

    @api.expect(query_parser)
    @api.response(Const.OK, 'Query result as a float number')
    @api.response(Const.FILE_NOT_EXIST[1], Const.FILE_NOT_EXIST[0])
    @api.response(Const.NO_BUDGET[1], Const.NO_BUDGET[0])
    @api.response(Const.INVALID_OPERATION[1], Const.INVALID_OPERATION[0])
    @api.response(Const.NO_NUMERIC_QUERY[1], Const.NO_NUMERIC_QUERY[0])
    @api.response(Const.NO_RESULT[1], Const.NO_RESULT[0])
    def post(self):
        """
        Try to execute the given query
        :return: A float number representing the query result or an error message
        """
        # Decrypt data received from Cloud Provider
        content = request.get_json()
        user_id = content[Const.ID]
        file_name = content[Const.FILE]
        query = content[Const.QUERY]
        epsilon = float(content[Const.EPSILON])
        fu.log(fu.get_current_time() + '[' + Const.QUERY + ' ' + request.method + '] Received from ' + user_id +
               ' request for query:' + query + ' from ' + file_name + ' with epsilon = ' + str(epsilon) + '\n')
        result = qh.check_query(user_id, file_name, query, epsilon)
        return result[0], result[1]


def initialize_app(flask_app):
    #os.mkdir(Const.ROOT_PATH + Const.LOG_FILES_PATH)
    #os.mkdir(Const.ROOT_PATH + Const.CSV_FILES_PATH)
    #os.mkdir(Const.ROOT_PATH + Const.USERS_LIST_PATH)
    api_blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(api_blueprint)
    api.add_namespace(ns)
    flask_app.register_blueprint(api_blueprint)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Flask server for differential privacy queries',
                                     usage='DiffPrivServer.py -a [IPADDR] -p [PORT] (default: -a 17.25.0.2 -p 5002)')
    parser.add_argument('-a', type=str, help='The IP address of the server', default='172.25.0.2')
    parser.add_argument('-p', type=int, help='The port of the server', default=5002)
    args = parser.parse_args()
    if fu.is_valid_ip(args.a):
        initialize_app(app)
        app.run(host=args.a, port=str(args.p))
    else:
        print Const.INVALID_IP
