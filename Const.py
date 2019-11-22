# BAZEL
BAZEL_RUN = '/root/bin/bazel run'
#BAZEL_RUN = 'bazel run'

# DIRECTORY PATHS
ROOT_PATH = '/diffpriv/'
#ROOT_PATH = './'
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
LIST = 'list'
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
OK = 200
BAD_REQ = ['Bad request', 400]
NO_METHOD = ['Method not allowed', 405]
INVALID_IP = ['[ERROR] Invalid IP address!', 500]
INVALID_FILE = ['[ERROR] Invalid file: expected csv file!', 500]
FILE_NOT_EXIST = ['[ERROR] File does not exist!', 500]
NO_NUMERIC = ['[ERROR] In csv file there are no numeric columns!', 500]
FILE_EXIST = ['[ERROR] File already uploaded!', 500]
NO_BUDGET = ['[ERROR] This user has not enough remaining budget!', 500]
NO_NUMERIC_QUERY = ['[ERROR] Given query is on non-numeric data!', 500]
INVALID_OPERATION = ['[ERROR] Invalid operation!', 500]
INVALID_BOUNDS = ['[ERROR] Invalid bounds!', 500]
NO_RESULT = ['[ERROR] Invalid operation result!', 500]
NO_CSV_DIR = ['[ERROR] Directory of .csv files does not exist', 500]

# BUDGET
STARTING_BUDGET = 1
QUERY_BUDGET = .25

LOWER_BOUND = -100000000
UPPER_BOUND = 100000000

SUPPORTED_FILE_FORMAT = {'csv'}
