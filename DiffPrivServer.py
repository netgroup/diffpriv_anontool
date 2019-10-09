from flask import Flask, render_template, request

import Const
import csv
import os.path


# If file entry does not exist, add it to list of csv files
def addFileToList(fileName, epsilon, permitCols):
    if os.path.exists('./' + Const.CSV_LIST):
        with open(Const.CSV_LIST, 'r') as fin:
            filesList = [line.split(',')[0] for line in fin]  # Create a list of already existing files
            if fileName in filesList:
                return Const.FILE_EXIST
    with open(Const.CSV_LIST, 'a') as fout:
        fout.write(fileName + ',' + epsilon + ',' + permitCols)
    return Const.OK


# Parse query and execute it
def execQuery(query):

    pass


# Check if user can execute the query
def checkQuery(user, query):
    if os.path.exists('./' + Const.USERS):
        fin = csv.reader(open('./' + Const.USERS))
        lines = list(fin)
        # Verify if user made previous queries and check its remaining budget
        for line in lines:
            elem = line.split(',')
            if user is elem[0]:
                # User has not enough remaining budget
                if elem[1] < Const.QUERY_BUDGET:
                    return Const.NO_BUDGET
                # User has enough budget, then decrease it
                lines[lines.index(line)][1] -= Const.QUERY_BUDGET
                # Overwrite users list file
                writer = csv.writer(open('./' + Const.USERS, 'w'))
                writer.writerows(lines)
                return execQuery(query)
        # User not found, then add a new one
        lines.append(user + ',' + (Const.STARTING_BUDGET - Const.QUERY_BUDGET))
        # Overwrite users list file
        writer = csv.writer(open('./' + Const.USERS, 'w'))
        writer.writerows(lines)
        return execQuery(query)


################# FLASK SERVER #################
app = Flask(__name__, root_path='/app/web')  # Create a Flask WSGI application


@app.route('/index', methods=['GET'])
def index():
    if request.method is 'GET':
        return render_template('index.html')
    else:
        return Const.NO_METHOD


@app.route('/'+Const.SEND_CSV, methods=['POST'])
def send_csv():
    if request.method is 'POST':
        # Get JSON data
        content = request.get_json()
        fileName = request.files[Const.FILE+'[0]']
        epsilon = content[Const.EPSILON]
        permitCols = content[Const.PERMIT_COLS]
        return addFileToList(fileName, epsilon, permitCols.replace(',', '-'))
    else:
        return Const.NO_METHOD


@app.route('/'+Const.QUERY, methods=['POST'])
def query():
    if request.method is 'POST':
        # Decrypt data received from Cloud Provider
        content = request.get_json()
        id = content[Const.ID]
        query = content[Const.QUERY]
        return checkQuery(id, query)
    else:
        return Const.NO_METHOD

if __name__ == '__main__':
    app.run(host=Const.CLIENT_ADDR, port=Const.CLIENT_PORT)
