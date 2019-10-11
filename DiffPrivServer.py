from flask import Flask, render_template, request

import Const
import os.path
import pandas as pd
from pyparsing import Word, alphas


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
    # Check if given file has numeric columns
    if hasNumericColumns(fileName) is False:
        return Const.NO_NUMERIC
    # Check if given file already exists
    if os.path.exists(Const.CSV_FILES_PATH + fileName):
        return Const.FILE_EXIST
    # Save file in csv files directory
    fileName.save(Const.CSV_FILES_PATH + fileName)
    return Const.OK


# FUNCTIONS TO HANDLE QUERY REQUEST

# Compute an anonymous count of data
def anon_count(data, epsilon):
    print 'Executing count on col', column
    return 'zero'


# Compute an anonymous sum of data
def anon_sum(data, epsilon):
    print 'Executing sum on col', column
    return 'one'


# Compute an anonymous mean of data
def anon_mean(data, epsilon):
    print 'Executing mean on col', column
    return 'two'


# Compute an anonymous variance of data
def anon_var(data, epsilon):
    print 'Executing variance on col', column
    return 'two'


# Compute an anonymous standard deviation of data
def anon_std_dev(data, epsilon):
    print 'Executing std_dev on col', column
    return 'two'


# Compute an anonymous max of data
def anon_max(data, epsilon):
    print 'Executing max on col', column
    return 'two'


# Compute an anonymous min of data
def anon_min(data, epsilon):
    print 'Executing min on col', column
    return 'two'


# Choose the proper function according to given operation string and execute it on the given data
def execQueryOperation(operation, data, epsilon):
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
    func = switcher.get(operation, lambda: "Invalid month")
    # Execute the function
    return func(data, epsilon)


# Parse query and execute it
def execQuery(file, query, epsilon):
    print 'Parsing query', query
    # Create query grammar
    statement = Word(alphas)
    operation = Word(alphas)
    column = Word(alphas)
    pattern = statement + operation + '(' + column + ')'
    # Parse query string
    items = pattern.parseString(query)
    print 'Parsing result:', items
    # Extract data according the given column
    fullData = pd.read_csv(file, header=0)
    data = fullData[items[2]]
    if isNumeric(data):
        # Execute query only if data is numeric
        return execQueryOperation(items[1], data, epsilon)
    return Const.NO_NUMERIC_QUERY


# Check if user can execute the query
def checkQuery(user, file, query, epsilon):
    # Check if users list file exists
    if os.path.exists(Const.USERS):
        data = pd.read_csv(Const.USERS, header=0)
        # Verify if the given user made previous queries and check its remaining budget
        if user in data.columns[Const.ID]:
            row = data.loc[data[Const.ID].isin(user)]
            # User has not enough remaining budget
            if data[row][1] < Const.QUERY_BUDGET:
                return Const.NO_BUDGET
            # User has enough budget, then decrease it
            data[row][1] -= Const.QUERY_BUDGET
        else:
            # User not found, then add a new one
            df = pd.DataFrame({Const.ID: [user], Const.BUDGET: [(Const.STARTING_BUDGET - Const.QUERY_BUDGET)]})
            data.append(df, ignore_index=True)
        # Overwrite users list file
        data.to_csv(Const.USERS)
    else:
        # File does not exist, create a new one
        df = pd.DataFrame({Const.ID: [Const.ID, user],
                           Const.BUDGET: [Const.BUDGET, Const.STARTING_BUDGET - Const.QUERY_BUDGET]})
        df.to_csv(Const.USERS)
    # Execute the query
    return execQuery(file, query, epsilon)


################# FLASK SERVER #################
app = Flask(__name__, root_path=Const.ROOT_PATH)  # Create a Flask WSGI application


@app.route('/' + Const.INDEX, methods=[Const.GET])
def index():
    if request.method is Const.GET:
        return render_template(Const.INDEX + '.html')
    else:
        return Const.NO_METHOD


@app.route('/' + Const.SEND_CSV, methods=[Const.POST])
def send_csv():
    if request.method is Const.POST:
        # Get file from request content
        fileName = request.files[Const.FILE+'[0]']
        # Store file
        return addFile(fileName)
    else:
        return Const.NO_METHOD


@app.route('/' + Const.QUERY, methods=[Const.POST])
def send_query():
    if request.method is Const.POST:
        # Decrypt data received from Cloud Provider
        content = request.get_json()
        user_id = content[Const.ID]
        file = content[Const.FILE]
        query = content[Const.QUERY]
        epsilon = content[Const.EPSILON]
        return checkQuery(user_id, file, query, epsilon)
    else:
        return Const.NO_METHOD


if __name__ == '__main__':
    app.run(host=Const.SERVER_ADDR, port=Const.SERVER_PORT)
