#   config var, put here for now
VERSION = 1.9
DEBUG_WITHOUT_DOWNLOAD = False

GET_SRC_TRY_MAX = 7
SCROLL_HEIGHT = 100  # 30
SHOW_MSG = True
CLOSE_BROWSER_ON_FINISHED = True
RETRY_ON_ERRORS_AFTER_DOWNLOAD_FINISHED = True

INDEX_DIGITS = 3
SHORT_SLEEP = 1
MID_SLEEP = 3
BROWSER_IMPLICITLY_WAIT = 5
LONG_SLEEP = 10

# in the log file, summary begins with it, at the end of log
SUMMARY_MARK = '[SUMMARY]'
HEADER_FULLNAME = 'FULLNAME'  # HEADER OF THE COLUMN
HEADER_INDEX = 'INDEX'
HEADER_STATUS = 'STATUS'
HEADER_INDEXED_SHORTNAME = 'INDEXED_SHORTNAME'
HEADER_SRC = 'SRC'
HEADER_ERROR_MESSAGE = 'ERROR_MESSAGE'

STATUS_OK = 'OK'
STATUS_ERROR = 'ER'

# FOR shortname  000_<shortname>.mp4, be careful for windows max length of file path 255
NAME_MAX_LENGTH = 150
NAME_CHAR_REPLACEMENT = ''  # ILLEGAL CHAR
NAME_SUFIX = '_'
TEXT_MAX_LENGTH = 300  # for error msg
TEXT_CHAR_REPLACEMENT = ' '
TEXT_SUFIX = '...'
# when no content of the cell, use it to write to the cell
LOGGER_EMPTY_PLACEHOLDER = '-'

FLAG_URL = '-u'
FLAG_PASS = '-P'
FLAG_USER = '-U'
FLAG_REDO = '-r'
FLAG_HELP = '-h'
FLAG_HELPS = ['-h', '-help', '--help', '--h']

FLAG_ENTRYWEB = '-e'  # entryweb, where content providers were presented

FLAG_START_INDEX = '-si'
FLAG_END_INDEX = '-ei'
