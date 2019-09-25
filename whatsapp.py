from urllib.parse import quote
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import datetime
import mysql.connector

mydb = mysql.connector.connect(host="HOST", user="USER", passwd="PASS", database="whatsapp") #<-- Change with your values
TARGET = 'TARGET NAME' #<-- Insert TARGET NAME
SCANNED = False

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920x1080')
chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'
)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-impl-side-painting')
chrome_options.add_argument('--disable-accelerated-2d-canvas')
chrome_options.add_argument('--disable-accelerated-jpeg-decoding')
chrome_options.add_argument('--test-type=ui')
browser = webdriver.Chrome("PATH") #<-- Insert the path chromedriver es. "C:\chromedriver.exe"
browser.get('https://web.whatsapp.com')
while SCANNED is False:
    print('Waiting QR Scanning...')
    sleep(5)
    try:
        notice = browser.find_element_by_class_name('_1cDWi')
        if notice.text == 'Mantieni il telefono connesso': #<-- Change according to your language es. "Keep the phone connected"
            SCANNED = True
            print('Success!')
            print (browser.service.process.pid)
    except NoSuchElementException:
        pass
search = browser.find_element_by_class_name('_2HS9r')
search.send_keys(TARGET)
chats = browser.find_elements_by_class_name('_19RFN')
for chat in chats:
    name = chat.get_attribute('title')
    if TARGET in name:
        chat.click()
        while True:
            try:
                sql = "INSERT INTO accessi (nome, data) VALUES (%s, %s)"
                mycursor = mydb.cursor()
                nome = TARGET
                a = str(datetime.datetime.now())
                b = a[:-7]
                data = b
                val = (nome, data)
                online = browser.find_element_by_class_name('_3fs0K').text
                online2 = online[-6:]
                if online2 == 'online':
                    a = str(datetime.datetime.now())
                    print(TARGET + ' is online!')
                    print(a[:-7])
                    mycursor.execute(sql, val)
                    mydb.commit()
                    sleep(1)
            except NoSuchElementException:
                pass
        sleep(2)
