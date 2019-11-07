import Const
import FuncUtils as fu
import os.path


# If file does not exist, store it in csv files directory
def add_file(file_name):
    f = str(file_name).split('\'')[1].split('\'')[0]
    # Check if given file already exists
    if os.path.exists(Const.ROOT_PATH + Const.CSV_FILES_PATH + f):
        fu.log(fu.get_current_time() + 'File already exists in directory ' + Const.ROOT_PATH + Const.CSV_FILES_PATH +
               ' and it can\'t be stored\n')
        return Const.FILE_EXIST
    # Save file in csv files directory
    file_name.save(Const.ROOT_PATH + Const.CSV_FILES_PATH + f)
    # Check if given file has numeric columns
    if not fu.has_numeric_columns(Const.ROOT_PATH + Const.CSV_FILES_PATH + f):
        os.remove(Const.ROOT_PATH + Const.CSV_FILES_PATH + f)
        fu.log(fu.get_current_time() + 'File has no numeric columns and it can\'t be stored\n')
        return Const.NO_NUMERIC
    fu.log(fu.get_current_time() + 'File stored in directory ' + Const.ROOT_PATH + Const.CSV_FILES_PATH + '\n')
    return Const.OK
