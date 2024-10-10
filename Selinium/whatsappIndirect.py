from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import threading
import re
from time import sleep

# suggestions[0].click()
# assert re.search(query, browser.current_url)

# page_heading = browser.find_element(By.ID, "firstHeading")
# assert re.search(query, page_heading.text)

class Message():

    phone_no = None
    message = None
    phone_no_range = { min: 6000000000, max: 9999999999}

    def __init__(self, msg, phone_no):
        if (len(phone_no) < 10 or len(phone_no) > 12):
            return None
        if (msg == None or msg == ""):
            return None
        if (int(phone_no) < self.phone_no_range[min] or int(phone_no) > self.phone_no_range[max]):
            return None
        self.phone_no = phone_no
        self.message = msg

class Whatsapp():
    
    isLogged = False
    msg_stack = []
    qr = None # get qr data from data-ref attribute
    QR_CHANGE_LISTENER = None
    STATUS_LISTENER = None

    WHATSAPP_SENDER_URL = 'https://web.whatsapp.com/send/?phone=<phone-no>&text=<msg>&type=phone_number&app_absent=0'

    # CONFIG VARIABLES 
    WHATSAPP_ELEMENTS_XPATH = {
        'SEARCH_BAR': '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div/p',
        'SENDER': '//*[@id="pane-side"]/div[1]/div/div/div[13]',
        'SENDER_MSG_BOX': '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p',
        'SEND_BTN': '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[2]/button',
        'QR': '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div'
    }
    SLEEP_SECONDS = {
        'NO_MSG': 5,
        'AFTER_SENDER_SEARCH': 1,
        'AFTER_SENDER_CLICKED': 1,
        'NEXT_ACTION': 2,
        'MSG_TYPE': 1
    }

    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        # options.add_argument("--no-sandbox") # linux only
        # options.add_argument("--headless=new") # for Chrome >= 109
        options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
        # options.add_argument("--window-size=1920,1080")
        # options.add_argument('--headless')
        # options.add_argument("user-data-dir=whatsapp_session")
        # options.add_argument('lang=pt-br')  
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options= options)
        self.browser.implicitly_wait(5)
        self.browser.get("https://web.whatsapp.com/")
        # self.loadCookie()
        self.event = threading.Event()
        k = ThreadJob(self.checkLogged,self.event,2)
        k.start()
        self.startMSGThread()

    def fetchQR(self):
        try:
            self.qr_div = self.browser.find_element(By.XPATH, self.WHATSAPP_ELEMENTS_XPATH['QR'])
            qr_attr = self.qr_div.get_attribute('data-ref')
            if (self.qr != qr_attr and self.QR_CHANGE_LISTENER):
                self.QR_CHANGE_LISTENER(qr = qr_attr)
            self.qr = qr_attr
            if (self.isLogged == True): 
                print('Whatsapp Log-out')
            self.isLogged = False
        except NoSuchElementException:
            return

    def checkLogged(self):
        try:
            self.search_bar = self.browser.find_element(By.XPATH, self.WHATSAPP_ELEMENTS_XPATH['SEARCH_BAR'])
            if (self.isLogged == False): 
                print('Whatsapp Logged')
                # print(self.browser.get_cookies())
            self.isLogged = True
            self.qr = None
        except NoSuchElementException:
            self.fetchQR()
            return

    def loadCookie(self):
        for cookie in self.COOKIES:
            self.browser.add_cookie(cookie)
        self.browser.refresh()

    def addMSG(self, message):
        if (message == None):
            return 
        self.msg_stack.append(message)

    def startMSGThread(self):
        self.msg_loop_thread = threading.Thread(target= self.sendMSG)
        self.msg_loop_thread.start()

    def sendMSG(self):
        try:
            if (self.isLogged and len(self.msg_stack) > 0):
                msg = self.msg_stack[0]
                print(f'ACTION : SENDING MSG TO {msg.phone_no}')
                sender_url = self.WHATSAPP_SENDER_URL.replace('<phone-no>', msg.phone_no).replace('<msg>', msg.message)
                self.browser.get(sender_url)
                print('LOADED')
                # actions = ActionChains(driver)
                # actions.send_keys(Keys.ENTER)
                # actions.perform()
                self.msg_stack.pop(0)
                print(f'ACTION : SENT MSG')
                sleep(self.SLEEP_SECONDS['NEXT_ACTION'])
                self.startMSGThread()
            else:
                sleep(self.SLEEP_SECONDS['NO_MSG'])
                self.startMSGThread()
        except NoSuchElementException:
            print("NOT FOUND ELEMENT WHILE SENDING MSG")

    def quit(self):
        browser.quit()
        # exit()

class ThreadJob(threading.Thread):
    def __init__(self,callback,event,interval):
        '''runs the callback function after interval seconds

        :param callback:  callback function to invoke
        :param event: external event for controlling the update operation
        :param interval: time in seconds after which are required to fire the callback
        :type callback: function
        :type interval: int
        '''
        self.callback = callback
        self.event = event
        self.interval = interval
        super(ThreadJob,self).__init__()

    def run(self):
        while not self.event.wait(self.interval):
            self.callback()


if __name__ == '__main__':
    whatsapp = Whatsapp()
    message = Message(msg = 'HI', phone_no='7977023515')
    print(f'MESSAGE : {message}')
    whatsapp.addMSG(message = message)
