import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


import urllib.request
import csv
import datetime
import sys


os.chdir(r'C:\Users\markp\Desktop\DailyUpdate')

class bloombergTesla3Scraper(object):
    def __init__(self):
        self.url = f"https://www.bloomberg.com/graphics/2018-tesla-tracker/#"
        self.driver = webdriver.Chrome()
        self.delay = 3 # of seconds to wait

    
    def load_bloomberg(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_all_elements_located((By.ID,"bb-that")))
            print("page is ready")
        except TimeoutException:
            print("loading took too much time")
            
    def extract_cumus(self):
        cumu_prod = self.driver.find_elements_by_class_name("cumulative")
        data_list = []
        for post in cumu_prod:
            data_list.append(post.text)
        return data_list
        
    def extract_rate(self):
        prod_rate = self.driver.find_elements_by_class_name("prod-rate")
        data_list2 = []
        for post in prod_rate:
            data_list2.append(post.text)
        return data_list2
        
    def close_driver(self):
        self.driver.quit()
        
            
scraper = bloombergTesla3Scraper()
scraper.load_bloomberg()
x1=scraper.extract_cumus()
x2=scraper.extract_rate()
scraper.close_driver()

thedate=datetime.date.today().strftime ("%Y%m%d")
newrow=thedate+','+str(x1[0].replace(",",""))+','+str(x2[0].replace(",",""))+"\n"

with open('tesla3.csv','a') as csv:
    csv.write(newrow)
    
    
import smtplib

import config


def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_ADDRESS, message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")
        
        
subject = "Tesla Daily Update"
msg = 'Tesla 3 Weekly production at ' +str(x2[0]) + " and cumulative production at " + str(x1[0])+"!!"

send_email(subject, msg)
print('all jobs done')





