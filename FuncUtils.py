from datetime import datetime

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
