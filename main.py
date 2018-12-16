from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import sys
import util.util as util
import util.var as var
import util.decorators as dec
import util.selUtil as sel

def main():
    argDic, needHelp = util.get_args_dict(sys.argv)
    needHelp and util.printHelp()

    redoLog = argDic.get(var.FLAG_REDO, None)
    pageUrl = argDic.get(var.FLAG_URL, util.default_pageurl())
    password = argDic.get(var.FLAG_PASS, util.default_password())
    username = argDic.get(var.FLAG_USER, util.default_username())

    print(f'user: {username}, pass: {password}')
    print(f"REDO: {redoLog}")
    print(f"pageUrl: {pageUrl}")
    
    logfile = f"log_{util.timestamp()}.csv"
    redoNames = util.getDownloadFailed(logfile=redoLog, target_column=var.HEADER_FULLNAME)

    cycle(
        logfile=logfile,
        match_fullnames=redoNames,
        pageUrl=pageUrl,
        username=username,
        password=password,
        retry_on_errors_when_finished=var.RETRY_ON_ERRORS_AFTER_DOWNLOAD_FINISHED)

def cycle(logfile, pageUrl, username, password, match_fullnames, retry_on_errors_when_finished):
    print(f"[C] VERSION-{var.VERSION} \nSTART... \n{pageUrl}")
    # init driver
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("media.volume_scale", "0.0")
    driver = webdriver.Firefox(firefox_profile=firefox_profile)

    driver.implicitly_wait(var.BROWSER_IMPLICITLY_WAIT) 

    driver.get(pageUrl)
    sel.login(driver=driver, username=username, password=password)
    time.sleep(var.MID_SLEEP)
    
    downloadAll(
        driver=driver, 
        logfile=logfile,
        xpath=var.XPATH_DOWNLOAD, 
        desiredNumOfDigits=var.INDEX_DIGITS,
        start_index=None, 
        end_index=None,
        match_fullnames=None,
        exclude_fullnames=None,
        match_indices=None)

    # always try again
    print(f"[C] Download 1st try finshied!")

    failedFullNames = util.getDownloadFailed(logfile=logfile, target_column=var.HEADER_FULLNAME)
    
    if isinstance(failedFullNames, list):
        failedFullNamesCount=len(failedFullNames)
        prevLog = logfile
        logfile = f'{prevLog.replace(".csv", "")}-{util.timestamp()}.csv'

        if failedFullNamesCount > 0:
            print(f"[C] Download again for {failedFullNamesCount} failedFullNames...")

            downloadAll(
                driver=driver, 
                xpath=var.XPATH_DOWNLOAD, 
                desiredNumOfDigits=var.INDEX_DIGITS,
                logfile=logfile,
                match_fullnames=failedFullNames,
                match_indices=None, 
                start_index=None, 
                end_index=None, 
                exclude_fullnames=None)

    var.CLOSE_BROWSER_ON_FINISHED and driver.quit()    # .close()
        

    print(f"[C] VERSION-{var.VERSION} ALL DONE!")

def downloadAll(
    driver, 
    xpath, 
    match_fullnames,
    match_indices,
    exclude_fullnames, 
    start_index,        # include
    end_index,          # include
    desiredNumOfDigits, 
    logfile):

    total = len(driver.find_elements_by_xpath(xpath))
    failed_indices = []
    failed = 0
    oks = 0
    skips=0
    srcSet = set() # save src to it, and use it to determine if src duplicated (sometimes it happens due to network speed, and ...)
    
    print(f"[D]Total: {total}")
    for i in range(total):
        index_shortname=''
        fullname=''
        videoSrc=''

        try:
            print(f"[D]>>>>#: {i} / {total}")

            if start_index is not None and i < start_index:
                print("[D]---skipped by start_index ---")
                skips += 1
                continue
            if end_index is not None and i > end_index:
                print("[D]---skipped by end_index ---")
                skips += 1
                continue

            if match_indices and isinstance(match_indices, list) and len(match_indices) > 0:
                if i not in match_indices:
                    print("[D]---skipped by match_indices ---")
                    skips += 1
                    continue

            time.sleep(var.SHORT_SLEEP)
            item=driver.find_elements_by_xpath(var.XPATH_DOWNLOAD)[i]

            shortname, fullname = sel.short_full_element_text(element=item)
            var.SHOW_MSG and print(f"[D] shortname fullname: {shortname}, {fullname}")

            if exclude_fullnames and fullname in exclude_fullnames:
                print("[D]---skipped by exclude_fullnames ---")
                skips += 1
                continue
            if isinstance(match_fullnames, list) and fullname not in match_fullnames:
                print("[D]---skipped by match_fullnames ---")
                skips += 1
                continue

            srcAttempts = 0
            sel.scrollDown(driver, var.SCROLL_HEIGHT)
            while True:
                srcAttempts += 1
                item=driver.find_elements_by_xpath(var.XPATH_DOWNLOAD)[i]
                item.click()
                time.sleep(var.SHORT_SLEEP)
                videoSrc = sel.getVideoSrc(driver=driver)
                if not videoSrc or videoSrc == "" or videoSrc in srcSet:
                    if srcAttempts > var.GET_SRC_TRY_MAX:
                        raise Exception(f"[D] Bad src: {videoSrc}; tried {srcAttempts}")
                    else:
                        print(f'[D] Bad src [{srcAttempts}], scroll down {var.SCROLL_HEIGHT} & try again ...')
                        sel.scrollDown(driver, var.SCROLL_HEIGHT)
                else:
                    # now src is valid
                    srcSet.add(videoSrc)
                    break

            index_padded=util.leftpad_zeros(num=i, desiredNumOfDigits=desiredNumOfDigits)
            index_shortname="{}_{}.mp4".format(index_padded, shortname)  # like 001_name, 010_name, 101_name
            var.SHOW_MSG and print(f"[D] index_shortname: {index_shortname}")

            if not var.DEBUG_WITHOUT_DOWNLOAD:
                hasDownloadError = util.download(driver=driver, url=videoSrc, name=index_shortname)
                raise Exception("[D] Raise download error") if hasDownloadError else None
            oks += 1
            print(f"[D] Downloaded: {index_shortname}")
            hasLoggerError = util.logger(
                logfile=logfile, 
                index=i, 
                status=var.STATUS_OK, 
                index_shortname=index_shortname, 
                fullname=fullname,
                src=videoSrc, 
                error='')
            hasLoggerError and print(f"[D] Logger error at index: {i}")
            time.sleep(var.SHORT_SLEEP)
        except Exception as e:
            failed += 1
            failed_indices.append(i)
            print(f"[D] Fail #{i} Cause:{e}")
            shortError, fullError = util.proper_short_full_text(str(e), maxLen=var.TEXT_MAX_LENGTH)
            util.logger(
                logfile=logfile,
                index=i, 
                status=var.STATUS_ERROR, 
                index_shortname=index_shortname, 
                fullname=fullname,
                src=videoSrc, 
                error=shortError)
    
    summary = f'DONE - Total: {total}; \nOks: {oks}; \nmatch_indices: {match_indices}; \nskippedCount: {skips}; \nFailedCount: {failed}; \nFailedIndices: {failed_indices}'
    print(summary)

    hasLoggerSummaryError = util.loggerSummary(
        logfile=logfile,
        totalCount=total, 
        okCount=oks, 
        match_indices=match_indices,
        skipCount=skips,
        failCount=failed,
        failed_indices=failed_indices)

    hasLoggerSummaryError and print('[D] Logger summary error!')

if __name__ == "__main__":
    main()
    # cycle()
    # cycleBaseOnLog('../log_2018-12-13-14-01-46.csv')
