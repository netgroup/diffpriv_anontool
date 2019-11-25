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
        return anon_value, Const.OK
    # Execution failed
    fu.log(fu.get_current_time() + Const.NO_RESULT[0] + '\n')
    return Const.NO_RESULT


# Check if statement and operation are valid
def check_operation(statement, operation):
    if statement in Const.QUERY_STATEMENTS:
        valid_operations = [Const.COUNT, Const.SUM, Const.AVG, Const.VAR, Const.STD_DEV, Const.MIN, Const.MAX]
        if operation in valid_operations:
            return True
    return False


# Clamp values according limits
def clamp(lower, upper):
    if lower > upper:
        return Const.INVALID_BOUNDS
    # Clamp bounds if they are out of limits
    if lower < Const.LOWER_BOUND:
        lower = Const.LOWER_BOUND
    if lower > Const.UPPER_BOUND:
        return Const.INVALID_BOUNDS
    if upper > Const.UPPER_BOUND:
        upper = Const.UPPER_BOUND
    if upper < Const.LOWER_BOUND:
        return Const.INVALID_BOUNDS
    return lower, upper


# Try to execute the given query
def exec_query(file_name, query, epsilon, budget):
    # Parse the query
    statement, operation, column, lower, upper = fu.parse_query(query)
    operation = operation.lower()
    # Check if operation is valid
    if not check_operation(statement.upper(), operation):
        fu.log(fu.get_current_time() + Const.INVALID_OPERATION[0] + '\n')
        return Const.INVALID_OPERATION
    # Check given bounds and clamp if they are out of limits
    lower, upper = clamp(lower, upper)
    if lower == Const.INVALID_BOUNDS[0]:
        fu.log(fu.get_current_time() + Const.INVALID_BOUNDS[0] + '\n')
        return Const.INVALID_BOUNDS
    # Extract data according the given column
    full_data = pd.read_csv(Const.ROOT_PATH + Const.CSV_FILES_PATH + file_name, header=0)
    data = full_data[column]
    # Check if data to use is numeric
    if fu.is_numeric(data):
        df = full_data[[full_data.columns[0], column]]
        print 'pre-filter:', df
        df = df.loc[(df[column] >= lower) & (df[column] <= upper)]
        print 'post-filter:', df
        df.to_csv(Const.ROOT_PATH + Const.DIFF_PRIV_MASTER_PATH + Const.DIFF_PRIV_PATH + Const.OPERATIONS_PATH + '/'
                  + Const.TMP_FILE_PATH, header=False, index=False)
        # Execute query
        return exec_query_operation(operation, epsilon, budget, lower, upper)
    fu.log(fu.get_current_time() + Const.NO_NUMERIC_QUERY[0] + '\n')
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
