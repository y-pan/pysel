import sys
import os, ssl
import datetime
import time
import re
import urllib.request
import pandas as pd
import util.var as var
import util.decorators as dec

LOG_ERROR_TEXT_REGEX=re.compile('[^0-9a-zA-Z:;.]')
NAME_REGEX=re.compile('[^0-9a-zA-Z]+')

def contentProvider(url):
    from protected.config import CONTENT_PROVIDERS
    for k,v in CONTENT_PROVIDERS.items():
        if v in url:
            return k
    return ''

@dec.SuppressExceptionReturnEmptyString
def default_pageurl():
    from protected.config import PAGEURL
    return PAGEURL

@dec.SuppressExceptionReturnEmptyString
def default_password():
    from protected.cred import PASSWORD
    return PASSWORD

@dec.SuppressExceptionReturnEmptyString
def default_entryweb():
    from protected.config import ENTRYWEB
    return ENTRYWEB

@dec.SuppressExceptionReturnEmptyString
def default_username():
    from protected.cred import USERNAME
    return USERNAME

@dec.SuppressExceptionReturnEmptyStringTuple
def proper_short_full_name(name='', maxLen=var.NAME_MAX_LENGTH): # shortname, fullname
    fullname=NAME_REGEX.sub(var.NAME_CHAR_REPLACEMENT, name)
    return fullname[:maxLen] + (fullname[maxLen:] and var.NAME_SUFIX), fullname

@dec.SuppressExceptionReturnEmptyStringTuple
def proper_short_full_text(text='', maxLen=var.TEXT_MAX_LENGTH): # shortText, fullText
    fullText = LOG_ERROR_TEXT_REGEX.sub(var.TEXT_CHAR_REPLACEMENT, str(text))
    return fullText[:maxLen] + (fullText[maxLen:] and var.TEXT_SUFIX), fullText

def leftpad_zeros(num, desiredNumOfDigits=3):
    try:
        snum = str(num)
        olen = len(snum)
        paddingLen = desiredNumOfDigits - olen
        if paddingLen > 0:
            snum = '0' * paddingLen + snum
        return snum
    except:
        t = int(time.time())  # seconds
        return f"{'0'*desiredNumOfDigits}_{t}"

def isHelp(flag):
    _flag = str(flag).lower()
    return _flag in var.FLAG_HELPS
    
def get_args_dict(parasList):
    # -key1 value1 -key2 value2
    key_value_dict = dict()
    prevKey=""
    hasHelp = False
    for p in parasList:
        if isHelp(p):
            hasHelp = True
        if p.startswith('-'):
            prevKey = p
        else:
            if prevKey:
                key_value_dict[prevKey] = p
    return key_value_dict, hasHelp

def printHelp():
    print('-------- options ----------')
    print('{}       - for username'.format(var.FLAG_USER))
    print('{}       - for password'.format(var.FLAG_PASS))
    print('{}       - for page url (listing videos)'.format(var.FLAG_URL))
    print('{}       - for redo log'.format(var.FLAG_REDO))
    print('{}       - for entryweb (entry to content providers)'.format(var.FLAG_ENTRYWEB))
    print('---------------------------')
    exit()

def noQuotations(text):
    return str(text).replace('"','').replace("'",'')

def camalCase(text):
    ws = str(text).split(' ')
    cws = list()
    for w in ws:
        cws.append(w[0].upper() + w[1:])
    return ''.join(cws)

def mask(text, keepDigits=2):
    return '*' * (len(text) - keepDigits) + text[-keepDigits:]

def timestamp():
    now = datetime.datetime.now()
    month = leftpad_zeros(num=now.month, desiredNumOfDigits=2)
    day = leftpad_zeros(num=now.day, desiredNumOfDigits=2)
    hour = leftpad_zeros(num=now.hour, desiredNumOfDigits=2)
    minute = leftpad_zeros(num=now.minute, desiredNumOfDigits=2)
    second = leftpad_zeros(num=now.second, desiredNumOfDigits=2)
    return f'{now.year}-{month}-{day}-{hour}-{minute}-{second}'

def getDownloadFailed(logfile, target_column=var.HEADER_FULLNAME): # target_column=var.HEADER_FULLNAME
    if not logfile:
        return None
    df = pd.read_csv(logfile, names=[var.HEADER_INDEX, var.HEADER_STATUS, var.HEADER_INDEXED_SHORTNAME, var.HEADER_FULLNAME, var.HEADER_SRC, var.HEADER_ERROR_MESSAGE], usecols=[var.HEADER_INDEX, var.HEADER_STATUS, var.HEADER_FULLNAME]) #,
    dfErr = df[ df[var.HEADER_STATUS] == var.STATUS_ERROR ]
    
    fullnamesOfFailed = dfErr[var.HEADER_FULLNAME].tolist()
    print(f'From log, failed: {len(fullnamesOfFailed)}')
    return fullnamesOfFailed

@dec.SuppressExceptionReturnTrue
def download(driver, url, name):
    urllib.request.urlretrieve(url, name)
    return False

@dec.SuppressExceptionReturnTrue
def ssl_unverified():
    # PYTHONHTTPSVERIFY = 0 
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): 
        ssl._create_default_https_context = ssl._create_unverified_context

@dec.SuppressExceptionReturnTrue
def loggerSummary(logfile, totalCount, okCount, match_indices, skipCount, failCount, failed_indices):
    failed_indices_str = str(failed_indices).replace(',', ';')
    match_indices_str = str(match_indices).replace(',', ';')
    with open(logfile, mode='a') as log:
        log.write(f'{var.SUMMARY_MARK}\nTotalCount: {totalCount}\nOKCount: {okCount}\nSkipCount: {skipCount}\nFailCount: {failCount}\nMatch_indices(only matched get downloaded): {match_indices_str}\nFailedIndices: {failed_indices_str}')
    return False

@dec.SuppressExceptionReturnTrue
def logger(logfile, index=0, status=var.STATUS_OK, index_shortname=var.LOGGER_EMPTY_PLACEHOLDER, fullname=var.LOGGER_EMPTY_PLACEHOLDER, src=var.LOGGER_EMPTY_PLACEHOLDER, error=var.LOGGER_EMPTY_PLACEHOLDER):
    if not index_shortname: 
        index_shortname = var.LOGGER_EMPTY_PLACEHOLDER
    if not fullname:
        fullname = var.LOGGER_EMPTY_PLACEHOLDER
    if not src:
        src = var.LOGGER_EMPTY_PLACEHOLDER
    if not error:
        error = var.LOGGER_EMPTY_PLACEHOLDER
    if not status:
        status=var.STATUS_OK

    line=f'{index},{status},{index_shortname},{fullname},{src},{error}\n'

    if not (os.path.isfile(logfile)):
        with open(logfile, mode='a') as log:
            log.write(f'{var.HEADER_INDEX},{var.HEADER_STATUS},{var.HEADER_INDEXED_SHORTNAME},{var.HEADER_FULLNAME},{var.HEADER_SRC},{var.HEADER_ERROR_MESSAGE}\n')
            log.write(line)
    else:
        with open(logfile, mode='a') as log:
            log.write(line)
    return False
