# ADDRESS
#SERVER_ADDR = '172.25.0.2'
SERVER_ADDR = 'localhost'
SERVER_PORT = '5002'

# ROUTES AND FIELDS
#ROOT_PATH = '/app/web'
ROOT_PATH = './'
GET = 'GET'
POST = 'POST'
INDEX = 'index'
SEND_CSV = 'send_csv'
QUERY = 'query'
FILE = 'file'
EPSILON = 'epsilon'
ID = 'id'
BUDGET = 'budget'
CSV_FILES_PATH = './csv_files/'
USERS = 'users.csv'
LOG = 'log.txt'

# QUERY FUNCTIONS
COUNT = 'count'
SUM = 'sum'
AVG = 'avg'
VAR = 'var'
STD_DEV = 'std_dev'
MIN = 'min'
MAX = 'max'

# STATUS AND ERROR
OK = '200'
BAD_REQ = '400'
NO_METHOD = '405'
ERROR = 'ERROR'
NO_NUMERIC = '[ERROR] In csv file there are no numeric columns!'
FILE_EXIST = '[ERROR] File already uploaded!'
NO_BUDGET = '[ERROR] This user has not enough remaining budget!'
NO_NUMERIC_QUERY = '[ERROR] Given query is on non-numeric data!'
INVALID_OPERATION = '[ERROR] Invalid operation!'

# BUDGET
STARTING_BUDGET = 1
QUERY_BUDGET = .25