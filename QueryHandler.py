from pyparsing import Word, alphas

import Const
import FuncUtils as fu
import pandas as pd
import os
import subprocess


# Choose the proper function according to given operation string and execute it on the given data
def exec_query_operation(operation, epsilon, budget, lower, upper):
    os.chdir(Const.ROOT_PATH + Const.DIFF_PRIV_MASTER_PATH)
    subprocess.check_output(['%s %s%s:priv_%s -- %f %f %f %f' % (Const.BAZEL_RUN, Const.DIFF_PRIV_PATH,
                                                                 Const.OPERATIONS_PATH, operation, epsilon, budget,
                                                                 lower, upper)], shell=True)
    os.chdir(Const.PARENT_DIR)
    if os.path.exists(Const.RESULT_PATH):
        data = pd.read_csv(Const.RESULT_PATH, header=None)
        # Extract results
        true_value = str(data[0].values[0])
        anon_value = str(data[1].values[0])
        fu.log(fu.get_current_time() + 'Result of ' + operation + ' has true value = ' + true_value +
               ' and anonymized value = ' + anon_value + '\n')
        # Remove result file
        os.remove(Const.RESULT_PATH)
        return anon_value
    # Execution failed
    fu.log(fu.get_current_time() + Const.NO_RESULT + '\n')
    return Const.NO_RESULT


# Check if statement and operation are valid
def check_operation(statement, operation):
    if statement in Const.QUERY_STATEMENTS:
        valid_operations = [Const.COUNT, Const.SUM, Const.AVG, Const.VAR, Const.STD_DEV, Const.MIN, Const.MAX]
        if operation in valid_operations:
            return True
    return False


# Parse query and execute it
def exec_query(file_name, query, epsilon, budget):
    # Create query grammar
    statement = Word(alphas)
    operation = Word(alphas)
    column = Word(alphas)
    pattern = statement + operation + '(' + column + ')'
    # Parse query string
    items = pattern.parseString(query)
    items[1] = items[1].lower()
    if not check_operation(items[0].upper(), items[1]):
        fu.log(fu.get_current_time() + Const.INVALID_OPERATION + '\n')
        return Const.INVALID_OPERATION
    lower = -1000000    # TO REMOVE
    upper = 1000000     # TO REMOVE
    # Extract data according the given column
    full_data = pd.read_csv(Const.ROOT_PATH + Const.CSV_FILES_PATH + file_name, header=0)
    data = full_data[items[3]]
    if fu.is_numeric(data):
        df = full_data[[full_data.columns[0], items[3]]]
        df.to_csv(Const.ROOT_PATH + Const.DIFF_PRIV_MASTER_PATH + Const.DIFF_PRIV_PATH + Const.OPERATIONS_PATH + '/'
                  + Const.TMP_FILE_PATH, header=False, index=False)
        # Execute query only if data is numeric
        return exec_query_operation(items[1], epsilon, budget, lower, upper)
    fu.log(fu.get_current_time() + Const.NO_NUMERIC_QUERY + '\n')
    return Const.NO_NUMERIC_QUERY


# Check if user can execute the query
def check_query(user, file_name, query, epsilon):
    # Check if file for query exists
    if not os.path.exists(Const.ROOT_PATH + Const.CSV_FILES_PATH + file_name):
        fu.log(fu.get_current_time() + 'User ' + user + ' made a query on ' + file_name + ' that does not exist\n')
        return Const.FILE_NOT_EXIST
    # Check if users list file exists
    if os.path.exists(Const.ROOT_PATH + Const.USERS_LIST_PATH + Const.USERS):
        data = pd.read_csv(Const.ROOT_PATH + Const.USERS_LIST_PATH + Const.USERS, header=0)
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
        data.to_csv(Const.ROOT_PATH + Const.USERS_LIST_PATH + Const.USERS, index=False)
    else:
        # File does not exist, create a new one
        df = pd.DataFrame({Const.ID: [user], Const.BUDGET: [Const.STARTING_BUDGET - Const.QUERY_BUDGET]},
                          columns=[Const.ID, Const.BUDGET])
        df.to_csv(Const.ROOT_PATH + Const.USERS_LIST_PATH + Const.USERS, index=False)
        budget = Const.STARTING_BUDGET
        fu.log(fu.get_current_time() + 'File ' + Const.ROOT_PATH + Const.USERS_LIST_PATH + Const.USERS +
               ' not found. Created a new one and added user ' + user + ' with budget ' + str(budget) + '\n')
        fu.log(fu.get_current_time() + 'User ' + user + ' budget updated to ' + str(budget - Const.QUERY_BUDGET) + '\n')
    # Execute the query
    return exec_query(file_name, query, epsilon, budget)
