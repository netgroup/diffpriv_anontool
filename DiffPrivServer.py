from flask import Flask, render_template, request
from pyparsing import Word, alphas
from datetime import datetime
import Const
import DiffPrivUtils as dpu
import os.path
import pandas as pd


# Return actual time
def get_current_time():
    return "["+str(datetime.now())+"] "


# Write message in log file
def log(message):
    with open(Const.LOG_FILES_PATH + Const.LOG + datetime.today().strftime('%Y%m%d') + '.txt', 'a') as file_out:
        file_out.write(message)


# FUNCTIONS TO HANDLE CSV FILE REQUEST

# Check if col contains only numbers
def is_numeric(col):
    return pd.to_numeric(col, errors='coerce').notnull().all()


# Check if file has at least a numeric column
def has_numeric_columns(file_name):
    data = pd.read_csv(file_name, header=0)
    for column in data.columns:
        if is_numeric(data[column]):
            return True
    return False


# If file does not exist, store it in csv files directory
def add_file(file_name):
    f = str(file_name).split('\'')[1].split('\'')[0]
    # Check if given file already exists
    if os.path.exists(Const.CSV_FILES_PATH + f):
        log(get_current_time() + 'File already exists in directory ' + Const.CSV_FILES_PATH +
            ' and it can\'t be stored\n')
        return Const.FILE_EXIST
    # Save file in csv files directory
    file_name.save(Const.CSV_FILES_PATH + f)
    # Check if given file has numeric columns
    if not has_numeric_columns(Const.CSV_FILES_PATH + f):
        os.remove(Const.CSV_FILES_PATH + f)
        log(get_current_time() + 'File has no numeric columns and it can\'t be stored\n')
        return Const.NO_NUMERIC
    log(get_current_time() + 'File stored in directory ' + Const.CSV_FILES_PATH + '\n')
    return Const.OK


# FUNCTIONS TO HANDLE QUERY REQUEST

# Compute an anonymous count of data
def anon_count(data, epsilon, budget):
    noised_result = int(round(dpu.add_noise(result=data.size, budget=budget, sensitivity=1.0, epsilon=epsilon)))
    log(get_current_time() + 'Executed anon_count with epsilon = ' + str(epsilon) + ' and budget = ' + str(budget) +
        ', resulting in anon_count = ' + str(max(noised_result, 0)) + ' where real count = ' + str(data.size) + '\n')
    return max(noised_result, 0)


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
    log(get_current_time() + Const.INVALID_OPERATION + '\n')
    return Const.INVALID_OPERATION


# Choose the proper function according to given operation string and execute it on the given data
def exec_query_operation(operation, data, epsilon, budget):
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
def exec_query(file_name, query, epsilon, budget, limit=0):
    # Create query grammar
    statement = Word(alphas)
    operation = Word(alphas)
    column = Word(alphas)
    pattern = statement + operation + '(' + column + ')'
    # Parse query string
    items = pattern.parseString(query)
    print 'Parsing result:', items
    items[2] = 'age'
    # Extract data according the given column
    full_data = pd.read_csv(Const.CSV_FILES_PATH + file_name, header=0)
    data = full_data[items[2]]
    if is_numeric(data):
        # Select data greater than limit
        data = data[data.iloc[:] >= limit]
        # Execute query only if data is numeric
        return exec_query_operation(items[1], data.values, epsilon, budget)
    log(get_current_time() + Const.NO_NUMERIC_QUERY + '\n')
    return Const.NO_NUMERIC_QUERY


# Check if user can execute the query
def check_query(user, file_name, query, epsilon):
    # Check if users list file exists
    if os.path.exists(Const.USERS_LIST_PATH + Const.USERS):
        data = pd.read_csv(Const.USERS_LIST_PATH + Const.USERS, header=0)
        # Verify if the given user made previous queries and check its remaining budget
        if user in data[[Const.ID]].values:
            row = data[data[Const.ID] == user].index.tolist()[0]
            # User has not enough remaining budget
            if data.iloc[row][1] < Const.QUERY_BUDGET:
                log(get_current_time() + 'User ' + user + ' has not enough budget (' + str(data.iloc[row][1]) +
                    ') to compute query\n')
                return Const.NO_BUDGET
            log(get_current_time() + 'User ' + user + ' found with budget ' + str(data.iloc[row][1]) +
                ', enough to compute query\n')
            # User has enough budget, then decrease it
            budget = data.iloc[row][1]
            data.iat[row, 1] -= Const.QUERY_BUDGET
            log(get_current_time() + 'User ' + user + ' budget updated to ' + str(data.iloc[row][1]) + '\n')
        else:
            # User not found, then add a new one
            df = pd.DataFrame({Const.ID: [user], Const.BUDGET: [(Const.STARTING_BUDGET - Const.QUERY_BUDGET)]},
                              columns=[Const.ID, Const.BUDGET])
            data = data.append(df, ignore_index=True)
            budget = Const.STARTING_BUDGET
            log(get_current_time() + 'User ' + user + ' not found. Created a new one with budget ' + str(budget) + '\n')
            log(get_current_time() + 'User ' + user + ' budget updated to ' + str(budget - Const.QUERY_BUDGET) + '\n')
        # Overwrite users list file
        data.to_csv(Const.USERS_LIST_PATH + Const.USERS, index=False)
    else:
        # File does not exist, create a new one
        df = pd.DataFrame({Const.ID: [user], Const.BUDGET: [Const.STARTING_BUDGET - Const.QUERY_BUDGET]},
                          columns=[Const.ID, Const.BUDGET])
        df.to_csv(Const.USERS_LIST_PATH + Const.USERS, index=False)
        budget = Const.STARTING_BUDGET
        log(get_current_time() + 'File ' + Const.USERS_LIST_PATH + Const.USERS +
            ' not found. Created a new one and added user ' + user + ' with budget ' + str(budget) + '\n')
        log(get_current_time() + 'User ' + user + ' budget updated to ' + str(budget - Const.QUERY_BUDGET) + '\n')
    # Execute the query
    return exec_query(file_name, query, epsilon, budget)


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
        log(get_current_time() + '[' + Const.SEND_CSV + ' ' + request.method + '] Received request to store csv file:' +
            str(file_name) + '\n')
        # Store file
        return add_file(file_name), Const.OK
    else:
        log(get_current_time() + '[' + Const.SEND_CSV + ' ' + request.method +
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
        log(get_current_time() + '[' + Const.QUERY + ' ' + request.method + '] Received from ' + user_id +
            ' request for query:' + query + ' from ' + file_name + ' with epsilon = ' + str(epsilon) + '\n')
        return str(check_query(user_id, file_name, query, epsilon)), Const.OK
    else:
        log(get_current_time() + '[' + Const.QUERY + ' ' + request.method +
            '] Received request with not allowed method\n')
        return Const.NO_METHOD


if __name__ == '__main__':
    #os.mkdir(Const.LOG_FILES_PATH)
    #os.mkdir(Const.CSV_FILES_PATH)
    app.run(host=Const.SERVER_ADDR, port=Const.SERVER_PORT)
