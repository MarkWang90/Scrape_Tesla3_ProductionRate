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


os.chdir(r'C:\Users\markp\Desktop\DailyUpdate\Scrape_Tesla3_ProductionRate')
source = f"https://www.bloomberg.com/graphics/2018-tesla-tracker/#"

class bloombergTesla3Scraper(object):
    def __init__(self):
        self.url = source
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

from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def main():
    names, emails = get_contacts('contacts.txt') # read contacts
    message_template = read_template('message.txt')

    # set up the SMTP server
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.login(config.EMAIL_ADDRESS, config.PASSWORD)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        msg2 = f"Tesla 3 Weekly production at {x2[0]} and cumulative production at {x1[0]} ! See details at {source}"

        message = message_template.substitute(PERSON_NAME=name.title(),Msg_context=msg2)
        
        # Prints out the message body for our sake
#        print(message)

        # setup the parameters of the message
        msg['From']=config.EMAIL_ADDRESS
        msg['To']=email
        msg['Subject']="Tesla 3 Weekly Production"
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
    
if __name__ == '__main__':
    print('sending messages')
    main()
    
print('all jobs done')

