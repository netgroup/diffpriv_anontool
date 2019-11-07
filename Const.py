# ADDRESS
#SERVER_ADDR = '172.17.0.2'
#SERVER_ADDR = '172.25.0.2'
SERVER_ADDR = 'localhost'
SERVER_PORT = '5002'

# ROUTES AND FIELDS
#FLASK_ROOT_PATH = '/diffpriv/web'
FLASK_ROOT_PATH = './web/'
GET = 'GET'
POST = 'POST'
INDEX = 'index'
SEND_CSV = 'send_csv'
QUERY = 'query'
FILE = 'file'
EPSILON = 'epsilon'
ID = 'id'
BUDGET = 'budget'

# DIR_PATH AND FILES
CSV_FILES_PATH = './csv_files/'
#CSV_FILES_PATH = '/diffpriv/csv_files/'
USERS_LIST_PATH = './users/'
#USERS_LIST_PATH = '/diffpriv/users/'
USERS = 'users_list.csv'
LOG_FILES_PATH = './logs/'
#LOG_FILES_PATH = '/diffpriv/logs/'
LOG = 'log'
TMP_FILE_PATH = 'operations/data.csv'
#TMP_FILE_PATH = '/diffpriv/differential-privacy-master/differential_privacy/operations/data.csv'
DIFF_PRIV_MASTER_PATH = './differential-privacy-master/'
DIFF_PRIV_PATH = 'differential_privacy/'
PARENT_DIR = '../'
RESULT = 'result.csv'


# QUERY FUNCTIONS
COUNT = 'count'
SUM = 'sum'
AVG = 'avg'
VAR = 'var'
STD_DEV = 'stdev'
MIN = 'min'
MAX = 'max'

# STATUS AND ERROR
OK = '200'
BAD_REQ = '400'
NO_METHOD = '405'
NO_NUMERIC = '[ERROR] In csv file there are no numeric columns!'
FILE_EXIST = '[ERROR] File already uploaded!'
NO_BUDGET = '[ERROR] This user has not enough remaining budget!'
NO_NUMERIC_QUERY = '[ERROR] Given query is on non-numeric data!'
INVALID_OPERATION = '[ERROR] Invalid operation!'
NO_RESULT = '[ERROR] Invalid operation result!'

# BUDGET
STARTING_BUDGET = 1
QUERY_BUDGET = .25

INFINITY = 'inf'
