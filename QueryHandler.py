from operations import AnonMean as amean
from operations import AnonVar as avar
from operations import AnonCount as acount
from operations import AnonSum as asum
from operations import AnonStdDev as adev
from operations import AnonMax as amax
from operations import AnonMin as amin
from pyparsing import Word, alphas

import Const
import FuncUtils as fu
import pandas as pd
import os.path


# Default execution if operation is not handled
def error_operation(data, epsilon, budget):
    fu.log(fu.get_current_time() + Const.INVALID_OPERATION + '\n')
    return Const.INVALID_OPERATION


# Choose the proper function according to given operation string and execute it on the given data
def exec_query_operation(operation, epsilon, budget, lower, upper):
    switcher = {
        Const.COUNT: acount.compute,
        Const.SUM: asum.compute,
        Const.AVG: amean.compute,
        Const.VAR: avar.compute,
        Const.STD_DEV: adev.compute,
        Const.MAX: amax.compute,
        Const.MIN: amin.compute
    }
    # Get the function from switcher dictionary
    func = switcher.get(operation, error_operation)
    # Execute the function
    if func(epsilon, budget, lower, upper) is 0:
        data = pd.read_csv('result.csv', header=None)
        true_value = data[0]
        anon_value = data[1]
        fu.log(fu.get_current_time() + 'Result of ' + operation + ' has true value = ' + true_value +
               'and anonymized value = ' + anon_value + '\n')
        return anon_value
    else:
        fu.log(fu.get_current_time() + Const.NO_RESULT + '\n')
        return Const.NO_RESULT


# Parse query and execute it
def exec_query(file_name, query, epsilon, budget):
    # Create query grammar
    statement = Word(alphas)
    operation = Word(alphas)
    column = Word(alphas)
    pattern = statement + operation + '(' + column + ')'
    # Parse query string
    items = pattern.parseString(query)
    print 'Parsing result:', items
    items[2] = 'age'
    lower = -1000000
    upper = 1000000
    # Extract data according the given column
    full_data = pd.read_csv(Const.CSV_FILES_PATH + file_name, header=0)
    data = full_data[items[2]]
    if fu.is_numeric(data):
        # Select data greater than limit
        # data = data[data.iloc[:] >= limit]
        df = full_data[[full_data.columns[0], items[2]]]
        print 'reduced data:\n', df
        df.to_csv(Const.TMP_FILE_PATH, header=False, index=False)
        # Execute query only if data is numeric
        return exec_query_operation(items[1], epsilon, budget, lower, upper)
    fu.log(fu.get_current_time() + Const.NO_NUMERIC_QUERY + '\n')
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
                fu.log(fu.get_current_time() + 'User ' + user + ' has not enough budget (' + str(data.iloc[row][1]) +
                       ') to compute query\n')
                return Const.NO_BUDGET
            fu.log(fu.get_current_time() + 'User ' + user + ' found with budget ' + str(data.iloc[row][1]) +
                   ', enough to compute query\n')
            # User has enough budget, then decrease it
            budget = data.iloc[row][1]
            data.iat[row, 1] -= Const.QUERY_BUDGET
            fu.log(fu.get_current_time() + 'User ' + user + ' budget updated to ' + str(data.iloc[row][1]) + '\n')
        else:
            # User not found, then add a new one
            df = pd.DataFrame({Const.ID: [user], Const.BUDGET: [(Const.STARTING_BUDGET - Const.QUERY_BUDGET)]},
                              columns=[Const.ID, Const.BUDGET])
            data = data.append(df, ignore_index=True)
            budget = Const.STARTING_BUDGET
            fu.log(fu.get_current_time() + 'User ' + user + ' not found. Created a new one with budget ' + str(budget) +
                   '\n')
            fu.log(fu.get_current_time() + 'User ' + user + ' budget updated to ' + str(budget - Const.QUERY_BUDGET) +
                   '\n')
        # Overwrite users list file
        data.to_csv(Const.USERS_LIST_PATH + Const.USERS, index=False)
    else:
        # File does not exist, create a new one
        df = pd.DataFrame({Const.ID: [user], Const.BUDGET: [Const.STARTING_BUDGET - Const.QUERY_BUDGET]},
                          columns=[Const.ID, Const.BUDGET])
        df.to_csv(Const.USERS_LIST_PATH + Const.USERS, index=False)
        budget = Const.STARTING_BUDGET
        fu.log(fu.get_current_time() + 'File ' + Const.USERS_LIST_PATH + Const.USERS +
               ' not found. Created a new one and added user ' + user + ' with budget ' + str(budget) + '\n')
        fu.log(fu.get_current_time() + 'User ' + user + ' budget updated to ' + str(budget - Const.QUERY_BUDGET) + '\n')
    # Execute the query
    return exec_query(file_name, query, epsilon, budget)
