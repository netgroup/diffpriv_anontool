from flask import Flask, render_template, request

import Const
import csv
import os.path
from pyparsing import Word, alphas


# Class to choose operation to execute on data
class Switcher(object):

    def indirect(self, i):
        method_name = str(i)
        method = getattr(self, method_name, lambda: 'Invalid')
        return method()

    @staticmethod
    def count(self, column):
        print 'Executing count on col', column
        return 'zero'

    @staticmethod
    def sum(self, column):
        print 'Executing sum on col', column
        return 'one'

    @staticmethod
    def avg(self, column):
        print 'Executing mean on col', column
        return 'two'

    @staticmethod
    def variance(self, column):
        print 'Executing variance on col', column
        return 'two'

    @staticmethod
    def std_dev(self, column):
        print 'Executing std_dev on col', column
        return 'two'

    @staticmethod
    def max(self, column):
        print 'Executing max on col', column
        return 'two'

    @staticmethod
    def min(self, column):
        print 'Executing min on col', column
        return 'two'


#
def isNumerical(file):

    pass


# If file entry does not exist, add it to list of csv files
def addFileToList(fileName, epsilon):
    isNumerical(fileName)
    if os.path.exists('./' + Const.CSV_LIST):
        with open(Const.CSV_LIST, 'r') as fin:
            filesList = [line.split(',')[0] for line in fin]  # Create a list of already existing files
            if fileName in filesList:
                return Const.FILE_EXIST
    with open(Const.CSV_LIST, 'a') as fout:
        fout.write(fileName + ',' + epsilon)
    return Const.OK


# Parse query and execute it
def execQuery(query):
    print 'Parsing query', query
    statement = Word(alphas)
    operation = Word(alphas)
    column = Word(alphas)
    pattern = statement + operation + '(' + column + ')'
    items = pattern.parseString(query)
    print 'Parsing result:', items
    result = Switcher.indirect(items[1])(items[2])
    return result


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
        return addFileToList(fileName, epsilon)
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
