from datetime import datetime

import Const
import pandas as pd
import math


# Return actual time
def get_current_time():
    return "["+str(datetime.now())+"] "


# Write message in log file
def log(message):
    with open(Const.LOG_FILES_PATH + Const.LOG + datetime.today().strftime('%Y%m%d') + '.txt', 'a') as file_out:
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


kClampFactor = 2 ** 39


# Set lower bound to the bigger between infinity float representation and -kClampFactor
def lower_bound():
    return max(-float(Const.INFINITY), -kClampFactor)


# Set upper bound to the smaller between infinity float representation and -kClampFactor
def upper_bound():
    return min(float(Const.INFINITY), kClampFactor)


# Bind value in the range [lower, upper]
def clamp(lower, upper, value):
    if value > upper:
        return upper
    if value < lower:
        return lower
    return value


# Compute the power of 2 and nearest integer to log2(n)
def next_power_of_two(n):
    return 2**math.ceil(math.log(n, 2))
