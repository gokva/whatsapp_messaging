'''DAILY TICKETS SENDING TO A WHATSAPP GROUP'''

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from datetime import datetime
from time import sleep
import socket

def is_connected():
    try:  
        socket.create_connection(("Google", 80))
        return True
    except :
        is_connected()

def getWeather(url):
    resp = requests.get(url)
    data = resp.json()
    desc = data["weather"][0]["description"]
    return desc

def getGoldRate(driver, url):
    driver.get(url)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    #get the gold price
    td_tags = soup.findAll("td")
    count = -1
    for tag in td_tags:
        count += 1
        if tag.text == "22K-916 Jewellery":
            gold_price = td_tags[count + 1].text
    return gold_price

def getCurrencyRate(driver, url):
    driver.get(url)
    rupee_rate = driver.find_element_by_xpath("//input[@class = 'a61j6 vk_gy vk_sh Hg3mWc']").text
    return rupee_rate  

def sendMessage(driver, group_name, d, w, g, c):
    try:

        find_user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(group_name))
        sleep(15)
        find_user.click()
        text_box = driver.find_element_by_xpath("//div[@class = '_3u328 copyable-text selectable-text']")
        text_box.click()
        message = ("*Daily Tickets*" + 
            "~*********************************~TODAY~" + d.strftime("%a, %b %d, %Y") +
            "~-------------------------------------~WEATHER~" + w +
            "~-------------------------------------~GOLD PRICE PER GRAM~22K-916@Mustafa: " + g +
            "~-------------------------------------~CURRENCY EXCHANGE RATE~1 Singapore Dollar = " +c+ " Indian rupees" +
            "~-------------------------------------~SPICE UP~There are 149 secondary schools in Singapore.")
        sleep(3)
        #typing message into the whatsapp message box
        for line in message.split("~"):
            text_box.send_keys(line)
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
            text_box.send_keys(Keys.BACKSPACE)
        sleep(2)
        text_box.send_keys(Keys.ENTER)      
        sleep(2)
       
    except Exception as e:
        print("{} Group doesn't exist!".format(group_name))     

# MAIN MODULE STARTS HERE  
group_name = "**Enter your group name here"
urls = ["http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}".format("Singapore","0822b961597ff8fe4e300e208e4aaee6"),
        "https://www.mustafa.com.sg/", 
        "https://www.google.com/search?q=singapore+to+india+currency+exchange+rate&oq=singapore+to+india+currency+exchange+rate&aqs=chrome..69i57.9300j0j9&sourceid=chrome&ie=UTF-8",
        "https://web.whatsapp.com/"]

driver = webdriver.Chrome('c:/users/user/desktop/tcs/chromedriver')
driver.maximize_window()
d = datetime.now()
w = getWeather(urls[0])                                                                    
g = getGoldRate(driver, urls[1])
c = getCurrencyRate(driver, urls[2])
driver.get(urls[3])
sleep(5)
sendMessage(driver, group_name, d, w, g, c)    
driver.quit()