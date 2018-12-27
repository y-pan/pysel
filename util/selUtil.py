import util.util as util
import util.var as var
import util.decorators as dec
import time

@dec.SuppressExceptionReturnZero
def getTotal(driver, content_provider):
    return len(driver.find_elements_by_xpath(getItemXPath(content_provider)))

@dec.SuppressExceptionReturnNone
def getVedioTriggerItem(driver, content_provider, index):
    return driver.find_elements_by_xpath(getItemXPath(content_provider))[index]

def getItemXPath(content_provider):
    if content_provider == 's':
        return "//a[@data-clip-position and contains(@id, 'lnk')]"
    elif content_provider == 'l':
        return "//div[@id='toc-content']//li[@class='toc-video-item']//a[contains(@class, 'item-name video-name')]"
    
@dec.SuppressExceptionReturnVoid
def safeClick(driver, xpath):
    driver.find_element_by_xpath(xpath).click()

@dec.SuppressExceptionReturnVoid
def safeClickIf(driver, xpath, shouldClick):
    driver.find_element_by_xpath(xpath).click()

@dec.SuppressExceptionReturnEmptyStringTuple
def short_full_element_text(element, content_provider): # short, full
    if content_provider == 's':
        return short_full_element_text_S(element)
    elif content_provider == 'l':
        return short_full_element_text_L(element)

def short_full_element_text_S(element): # short, full
    oText = util.camalCase(element.get_attribute('innerHTML')) #title
    return util.proper_short_full_name(name=oText, maxLen=var.NAME_MAX_LENGTH)
    
def short_full_element_text_L(element): # short, full
    oText = util.camalCase(element.text)
    return util.proper_short_full_name(name=oText, maxLen=var.NAME_MAX_LENGTH)
    
def login(driver, username, password, content_provider, entryweb, downloadpage): # False for no error
    if str(content_provider).lower() == 's':
        return loginS(driver, username, password, downloadpage)
    elif str(content_provider).lower() == 'l':
        return loginL(driver, username, password, entryweb)
    return True

def loginS(driver, username, password, downloadpage): # s
    driver.get(downloadpage)
    driver.find_element_by_name("user").send_keys(username)
    driver.find_element_by_name("pass").send_keys(password)
    driver.find_element_by_xpath("//input[@value='Sign in']").click()

def loginL(driver, username, password, entryweb): # l
    driver.get(entryweb)
    driver.find_element_by_xpath("//section[@id='find-your-way']//a[contains(text(),'eLearning')]").click()
    driver.find_element_by_xpath("//a[contains(@class, 'promo-card')][1]").click()
    driver.find_element_by_xpath("//div[@class='record-detail']//a[contains(@class, 'access-online')]").click()
    driver.find_element_by_xpath("//input[@id='card-number']").send_keys(username)
    driver.find_element_by_xpath("//input[@id='card-pin']").send_keys(password)
    driver.find_element_by_xpath("//span[@id='library-login-login']").click()

def gotoDownloadPage(driver, pageUrl, content_provider):
    if content_provider == 'l':
        driver.get(pageUrl)
        time.sleep(var.MID_SLEEP)
    else:
        pass

@dec.SuppressExceptionReturnVoid
def scrollDown(driver, num, content_provider):
    if content_provider == 's':
        scrollDownS(driver, num)
    elif content_provider == 'l':
        scrollDownL(driver, num)

def scrollDownL(driver, num):
    ys = driver.execute_script(f"var ele=document.getElementsByClassName('course-toc toc-container')[0]; y0=ele.scrollTop; ele.scrollBy(0,{num}); y1=ele.scrollTop; return [y0, y1];")
    var.SHOW_MSG and print(f"Scroll down [from, to]: {ys}")

def scrollDownS(driver, num):
    ys = driver.execute_script(f"var y0=window.pageYOffset; window.window.scrollTo(0, (window.pageYOffset + {num})); return [y0, window.pageYOffset];")
    var.SHOW_MSG and print(f"Scroll down [from, to]: {ys}")

@dec.SuppressExceptionReturnEmptyString
def getVideoSrc(driver, content_provider):
    if content_provider == 's':
        return getVideoSrcS(driver)
    elif content_provider == 'l':
        return getVideoSrcL(driver)

def getVideoSrcS(driver):
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    time.sleep(var.SHORT_SLEEP)
    video = driver.find_element_by_xpath("//div[@class='videoDisplay']/video")
    src = video.get_attribute("src")
    driver.switch_to.default_content()
    time.sleep(var.SHORT_SLEEP)
    var.SHOW_MSG and print(f"src: {src}")
    return src

def getVideoSrcL(driver):
    vedio = driver.find_element_by_xpath("//div[@id='courseplayer']//video[@class='player']")
    src = vedio.get_attribute('src')
    var.SHOW_MSG and print(f"src: {src}")
    return src
