from flask import Flask, render_template, request
from pyparsing import Word, alphas
from datetime import datetime
import Const
import DiffPrivUtils as dpu
import os.path
import pandas as pd


# Return actual time
def getCurrentTime():
    return "["+str(datetime.now())+"] "


# Write message in log file
def log(message):
    with open(Const.LOG+".txt", 'a') as fout:
        fout.write(message)


# FUNCTIONS TO HANDLE CSV FILE REQUEST

# Check if col contains only numbers
def isNumeric(col):
    return pd.to_numeric(col, errors='coerce').notnull().all()


# Check if file has at least a numeric column
def hasNumericColumns(file):
    data = pd.read_csv(file, header=0)
    for column in data.columns:
        if isNumeric(data[column]) is True:
            return True
    return False


# If file does not exist, store it in csv files directory
def addFile(fileName):
    # Check if given file already exists
    if os.path.exists(Const.CSV_FILES_PATH + fileName):
        log(getCurrentTime() + 'File already exists in directory ' + Const.CSV_FILES_PATH + ' and it can\'t be stored')
        return Const.FILE_EXIST
    # Check if given file has numeric columns
    if hasNumericColumns(fileName) is False:
        log(getCurrentTime() + 'File has no numeric columns and it can\'t be stored')
        return Const.NO_NUMERIC
    # Save file in csv files directory
    fileName.save(Const.CSV_FILES_PATH + fileName)
    log(getCurrentTime() + 'File stored in directory ' + Const.CSV_FILES_PATH)
    return Const.OK


# FUNCTIONS TO HANDLE QUERY REQUEST

# Compute an anonymous count of data
def anon_count(data, epsilon, budget):
    noisedResult = int(round(dpu.addNoise(result=data.size, budget=budget, sensitivity=1.0, epsilon=epsilon)))
    log(getCurrentTime() + 'Executed anon_count with epsilon = ' + epsilon + ' and budget = ' + budget +
        ', resulting in anon_count = ' + str(max(noisedResult, 0)) + ' where real count = ' + data.size)
    print 'data size:', data.size, '\nnoisedResult:', noisedResult, '\nanon_count:', max(noisedResult, 0)
    return max(noisedResult, 0)


# Compute an anonymous sum of data
def anon_sum(data, epsilon, budget):
    print 'Executing sum on col', column
    return 'one'


# Compute an anonymous mean of data
def anon_mean(data, epsilon, budget):
    print 'Executing mean on col', column
    return 'two'


# Compute an anonymous variance of data
def anon_var(data, epsilon, budget):
    print 'Executing variance on col', column
    return 'two'


# Compute an anonymous standard deviation of data
def anon_std_dev(data, epsilon, budget):
    print 'Executing std_dev on col', column
    return 'two'


# Compute an anonymous max of data
def anon_max(data, epsilon, budget):
    print 'Executing max on col', column
    return 'two'


# Compute an anonymous min of data
def anon_min(data, epsilon, budget):
    print 'Executing min on col', column
    return 'two'


def error_operation(data, epsilon, budget):
    log(getCurrentTime() + Const.INVALID_OPERATION)
    return Const.INVALID_OPERATION


# Choose the proper function according to given operation string and execute it on the given data
def execQueryOperation(operation, data, epsilon, budget):
    switcher = {
        Const.COUNT: anon_count,
        Const.SUM: anon_sum,
        Const.AVG: anon_mean,
        Const.VAR: anon_var,
        Const.STD_DEV: anon_std_dev,
        Const.MAX: anon_max,
        Const.MIN: anon_min
    }
    # Get the function from switcher dictionary
    func = switcher.get(operation, error_operation)
    # Execute the function
    return func(data, epsilon, budget)


# Parse query and execute it
def execQuery(file, query, epsilon, budget, limit=0):
    print 'Parsing query:', query
    # Create query grammar
    statement = Word(alphas)
    operation = Word(alphas)
    column = Word(alphas)
    pattern = statement + operation + '(' + column + ')'
    # Parse query string
    items = pattern.parseString(query)
    print 'Parsing result:', items
    file = 'data.csv'
    items[2] = 'age'
    # Extract data according the given column
    fullData = pd.read_csv(file, header=0)
    data = fullData[items[2]]
    if isNumeric(data):
        # Select data greater than limit
        data = data[data.iloc[:] >= limit]
        # Execute query only if data is numeric
        return execQueryOperation(items[1], data.values, epsilon, budget)
    log(getCurrentTime() + Const.NO_NUMERIC_QUERY)
    return Const.NO_NUMERIC_QUERY


# Check if user can execute the query
def checkQuery(user, file, query, epsilon):
    # Check if users list file exists
    if os.path.exists(Const.USERS):
        data = pd.read_csv(Const.USERS, header=0)
        # Verify if the given user made previous queries and check its remaining budget
        if user in data[[Const.ID]].values:
            row = data[data[Const.ID] == user].index.tolist()[0]
            # User has not enough remaining budget
            if data.iloc[row][1] < Const.QUERY_BUDGET:
                log(getCurrentTime() + 'User ' + user + ' has not enough budget (' + data.iloc[row][1] +
                    ') to compute query')
                print 'user has not enough budget'
                return Const.NO_BUDGET
            log(getCurrentTime() + 'User ' + user + ' found with budget ' + data.iloc[row][1] +
                ', enough to compute query')
            print 'user found with budget', data.iloc[row][1]
            # User has enough budget, then decrease it
            data.iat[row, 1] -= Const.QUERY_BUDGET
            budget = data.iloc[row][1]
            log(getCurrentTime() + 'User ' + user + ' budget updated to ' + budget)
            print 'budget updated', budget
        else:
            # User not found, then add a new one
            df = pd.DataFrame({Const.ID: [user], Const.BUDGET: [(Const.STARTING_BUDGET - Const.QUERY_BUDGET)]},
                              columns=[Const.ID, Const.BUDGET])
            data = data.append(df, ignore_index=True)
            budget = Const.STARTING_BUDGET - Const.QUERY_BUDGET
            log(getCurrentTime() + 'User ' + user + ' not found. Created a new one with budget ' + budget)
            print 'user not found, new with budget', budget
        # Overwrite users list file
        data.to_csv(Const.USERS, index=False)
    else:
        # File does not exist, create a new one
        df = pd.DataFrame({Const.ID: [user], Const.BUDGET: [Const.STARTING_BUDGET - Const.QUERY_BUDGET]},
                          columns=[Const.ID, Const.BUDGET])
        df.to_csv(Const.USERS, index=False)
        budget = Const.STARTING_BUDGET - Const.QUERY_BUDGET
        log(getCurrentTime() + 'File ' + Const.USERS + ' not found. Created a new one and added user ' + user +
            ' with budget ' + budget)
        print 'file not found, new file and user with budget', budget
    # Execute the query
    return execQuery(file, query, epsilon, budget)


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
        fileName = request.files[Const.FILE+'[0]']
        log(getCurrentTime() + '[' + Const.SEND_CSV + ' ' + request.method + '] Received request to store csv file:' +
            fileName)
        # Store file
        return addFile(fileName)
    else:
        log(getCurrentTime() + '[' + Const.SEND_CSV + ' ' + request.method +
            '] Received request with not allowed method')
        return Const.NO_METHOD


@app.route('/' + Const.QUERY, methods=[Const.POST])
def send_query():
    if request.method == Const.POST:
        # Decrypt data received from Cloud Provider
        content = request.get_json()
        user_id = content[Const.ID]
        file = content[Const.FILE]
        query = content[Const.QUERY]
        epsilon = float(content[Const.EPSILON])
        log(getCurrentTime() + '[' + Const.QUERY + ' ' + request.method + '] Received from ' + user_id +
            ' request for query:' + query + ' from ' + file + ' with epsilon = ' + epsilon)
        return checkQuery(user_id, file, query, epsilon)
    else:
        log(getCurrentTime() + '[' + Const.QUERY + ' ' + request.method + '] Received request with not allowed method')
        return Const.NO_METHOD


if __name__ == '__main__':
    app.run(host=Const.SERVER_ADDR, port=Const.SERVER_PORT)
