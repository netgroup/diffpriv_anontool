from datetime import datetime
from pyparsing import Word, alphas, alphanums, nums

import Const
import pandas as pd


# Return actual time
def get_current_time():
    return "["+str(datetime.now())+"] "


# Write message in log file
def log(message):
    with open(Const.ROOT_PATH + Const.LOG_FILES_PATH + Const.LOG + datetime.today().strftime('%Y%m%d') + '.txt', 'a') \
            as file_out:
        file_out.write(message)


# Check if data contains only numbers
def is_numeric(data):
    return pd.to_numeric(data, errors='coerce').notnull().all()


# Check if file has at least a numeric column
def has_numeric_columns(file_name):
    data = pd.read_csv(file_name, header=0)
    for column in data.columns:
        if is_numeric(data[column]):
            return True
    return False


# Check if IP address is valid
def is_valid_ip(ip):
    try:
        res = (ip.count('.') == 3 or ip.count('.') == 5) and \
              all(0 <= int(num) < 256 for num in ip.rstrip().split('.')) or ip == 'localhost'
        return res
    except ValueError:
        return False


# Parse the given query
def parse_query(query):
    # Create query grammar
    statement = Word(alphas)
    operation = Word(alphas)
    column = Word(alphanums)
    # Check if there is a WHERE clause to set bounds to values
    if 'where' in query or 'WHERE' in query:
        where = Word(alphas)
        if '>' in query:
            lower = Word(nums + '-')
            if '<' in query:
                and_op = Word(alphas)
                upper = Word(nums + '-')
                if query.find('>') < query.find('<'):
                    pattern = statement + operation + '(' + column + ')' + where + column + '>' + lower + and_op + \
                              column + '<' + upper
                else:
                    pattern = statement + operation + '(' + column + ')' + where + column + '<' + lower + and_op + \
                              column + '>' + upper
            else:
                pattern = statement + operation + '(' + column + ')' + where + column + '>' + lower
        else:
            if '<' in query:
                upper = Word(nums + '-')
                pattern = statement + operation + '(' + column + ')' + where + column + '<' + upper
            else:
                pattern = statement + operation + '(' + column + ')'
    else:
        pattern = statement + operation + '(' + column + ')'
    # Parse query string
    items = pattern.parseString(query)
    statement = items[0]
    operation = items[1]
    column = items[3]
    if len(items) == 9:
        if '>' in query:
            lower = items[8]
            upper = Const.UPPER_BOUND
        else:
            lower = Const.LOWER_BOUND
            upper = items[8]
    else:
        if len(items) == 13:
            if query.find('>') < query.find('<'):
                lower = items[8]
                upper = items[12]
            else:
                lower = items[12]
                upper = items[8]
        else:
            lower = Const.LOWER_BOUND
            upper = Const.UPPER_BOUND
    return statement, operation, column, float(lower), float(upper)
