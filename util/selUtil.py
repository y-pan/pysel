
import util.util as util
import util.var as var
import util.decorators as dec
import time

@dec.SuppressExceptionVoid
def safeClick(driver, xpath):
    driver.find_element_by_xpath(xpath).click()

@dec.SuppressExceptionVoid
def safeClickIf(driver, xpath, shouldClick):
    driver.find_element_by_xpath(xpath).click()

@dec.SuppressExceptionEmptyStringTuple
def short_full_element_text(element): # short, full
    oText = element.get_attribute('innerHTML')
    # oTitle = element.get_attribute('title')
    shortText, fullText = util.proper_short_full_name(name=oText, maxLen=var.NAME_MAX_LENGTH)
    # shortTitle, fullTitle = util.proper_short_full_name(name=oTitle, maxLen=var.NAME_MAX_LENGTH)
    
    if shortText:
        var.SHOW_MSG and print(f"short_full_element_text: {shortText}, {fullText}")
        return shortText, fullText
    # if shortTitle:
        # return shortTitle, fullTitle
    raise Exception(f"No text from element: {str(element)}")

@dec.SuppressExceptionTrue
def login(driver, username, password):
    driver.find_element_by_name("user").send_keys(username)
    driver.find_element_by_name("pass").send_keys(password)
    driver.find_element_by_xpath("//input[@value='Sign in']").click()
    var.SHOW_MSG and print(f'Login clicked')

@dec.SuppressExceptionVoid
def scrollDown(driver, num):
    ys = driver.execute_script(f"var y0=window.pageYOffset; window.window.scrollTo(0, (window.pageYOffset + {num})); return [y0, window.pageYOffset];")
    var.SHOW_MSG and print(f"Scroll down [from, to]: {ys}")

@dec.SuppressExceptionEmptyString
def getVideoSrc(driver):
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    time.sleep(var.SHORT_SLEEP)
    video = driver.find_element_by_xpath("//div[@class='videoDisplay']/video")
    src = video.get_attribute("src")
    driver.switch_to.default_content()
    time.sleep(var.SHORT_SLEEP)
    var.SHOW_MSG and print(f"src: {src}")
    return src
