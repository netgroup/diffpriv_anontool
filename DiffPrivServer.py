from flask import Flask, render_template, request
from subprocess import check_output

import Const
import CSVHandler as csvh
import FuncUtils as fu
import QueryHandler as qh

import os

################# FLASK SERVER #################
app = Flask(__name__, root_path=Const.ROOT_PATH)  # Create a Flask WSGI application


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
        return str(qh.check_query(user_id, file_name, query, epsilon)), Const.OK
    else:
        fu.log(fu.get_current_time() + '[' + Const.QUERY + ' ' + request.method +
               '] Received request with not allowed method\n')
        return Const.NO_METHOD


if __name__ == '__main__':
    os.chdir('differential-privacy-master/')
    print 'result:\n', check_output(['/root/bin/bazel run differential_privacy/example:report_the_carrots'], shell=True)
    #print 'result:\n', check_output(['cd', 'differential-privacy-master', '&&', 'bazel', 'run',
    #                             'differential_privacy/example:reports_the_carrots'], shell=True)
    # os.mkdir(Const.LOG_FILES_PATH)
    # os.mkdir(Const.CSV_FILES_PATH)
    # os.mkdir(Const.USERS_LIST_PATH)
    app.run(host=Const.SERVER_ADDR, port=Const.SERVER_PORT)
