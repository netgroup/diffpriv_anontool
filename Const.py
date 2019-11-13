# BAZEL
#BAZEL_RUN = '/root/bin/bazel run'
BAZEL_RUN = 'bazel run'

# ADDRESS AND PORT
#SERVER_ADDR = '172.17.0.2'
#SERVER_ADDR = '172.25.0.2'
#SERVER_ADDR = 'localhost'
#SERVER_PORT = '5002'

# DIRECTORY PATHS
#ROOT_PATH = '/diffpriv/'
ROOT_PATH = './'
PARENT_DIR = '../'
FLASK_ROOT_PATH = 'web/'
CSV_FILES_PATH = 'csv_files/'
USERS_LIST_PATH = 'users/'
LOG_FILES_PATH = 'logs/'
DIFF_PRIV_MASTER_PATH = 'differential-privacy-master/'
DIFF_PRIV_PATH = 'differential_privacy/'
OPERATIONS_PATH = 'operations'

# FILES
USERS = 'users_list.csv'
LOG = 'log'
TMP_FILE_PATH = 'data.csv'
RESULT_PATH = '/tmp/result.csv'

# ROUTES AND FIELDS
GET = 'GET'
POST = 'POST'
INDEX = 'index'
SEND_CSV = 'send_csv'
LIST = 'get_list'
QUERY = 'query'
FILE = 'file'
EPSILON = 'epsilon'
ID = 'id'
BUDGET = 'budget'

# QUERY OPERATIONS
QUERY_STATEMENTS = {'SELECT'}

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
INVALID_IP = '[ERROR] Invalid IP address!'
INVALID_FILE = '[ERROR] Invalid file: expected csv file!'
FILE_NOT_EXIST = '[ERROR] File does not exist!'
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

SUPPORTED_FILE_FORMAT = {'csv'}
