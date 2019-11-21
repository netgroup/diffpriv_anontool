import Const
import FuncUtils as fu
import os.path


# If file does not exist, store it in csv files directory
def add_file(fin, file_name):
    # Check if file is a csv
    if not file_name.split('.')[1] in Const.SUPPORTED_FILE_FORMAT:
        fu.log(fu.get_current_time() + 'File ' + file_name + ' is not supported\n')
        return Const.INVALID_FILE
    # Check if given file already exists
    if os.path.exists(Const.ROOT_PATH + Const.CSV_FILES_PATH + file_name):
        fu.log(fu.get_current_time() + 'File already exists in directory ' + Const.ROOT_PATH + Const.CSV_FILES_PATH +
               ' and it can\'t be stored\n')
        return Const.FILE_EXIST
    # Save file in csv files directory
    fin.save(Const.ROOT_PATH + Const.CSV_FILES_PATH + file_name)
    # Check if given file has numeric columns
    if not fu.has_numeric_columns(Const.ROOT_PATH + Const.CSV_FILES_PATH + file_name):
        os.remove(Const.ROOT_PATH + Const.CSV_FILES_PATH + file_name)
        fu.log(fu.get_current_time() + 'File has no numeric columns and it can\'t be stored\n')
        return Const.NO_NUMERIC
    fu.log(fu.get_current_time() + 'File stored in directory ' + Const.ROOT_PATH + Const.CSV_FILES_PATH + '\n')
    return 'File stored!', Const.OK
