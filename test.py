from asyncore import close_all
from ftplib import all_errors
from socket import timeout
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

#options = webdriver.ChromeOptions()

# Uncomment the line below if you'd like to scrape without a new Chrome window every time.
#options.add_argument('headless')

driver = webdriver.Chrome()
driver.maximize_window() 
driver.get("https://linkedin.com/login")
wait = WebDriverWait(driver, 5)

jobs = []

time.sleep(2) #Time allotted for the website to load 

#Logs in with username
username = driver.find_element(By.ID, "username")
username.send_keys("clashingminis1@gmail.com")

#Logs in with password 
password = driver.find_element(By.ID,"password")
password.send_keys("8Kbyf9g]V8nH7PdU")

#Clicks Login Button
driver.find_element(By.XPATH,"//button[@type='submit']").click()

#Finds Job Page & Begins Search
JNumber = 0                                    #Increases by 1 to change to the next job
JobType = "?f_JT=I"                            #For Internships
City = "&f_PP=102571732"                       #New York, NY
JobName = "&keywords=Publishing"               #Name of Search
Country = "&location=United%20States"          #US as default country
Sort = "&sortBy=DD"                            #Sort by date (Can change this)
PageNumber = f"&start="                        #The job that is being viewed

#Data Scraping
n = 1 
while n > 0:
    driver.get(f"https://www.linkedin.com/jobs/search/{JobType}{City}{JobName}{Country}{Sort}{PageNumber}{JNumber}")
    job_src = driver.page_source
    soup = BeautifulSoup(job_src, 'lxml')
    JNumber += 1
    time.sleep(1.5)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//span[text()[normalize-space()='Apply']]"))).click()
    time.sleep(2)
    try:
        close_prompt = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class = 'artdeco-modal__dismiss artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view']")))
        close_prompt.click()
        time.sleep(1)
    except Exception as e:
        pass
    time.sleep(3)
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//span[text()[normalize-space()='Apply']]"))).click()
    except NoSuchElementException:
        pass
    time.sleep(5)
    url = driver.current_url
    n-= 1
print(url)
time.sleep(1000)

# jobs = [{"Link" = }]
# # Converts the dataframe into str object with formatting
# df = pd.DataFrame(jobs)

# #Exports data as HTML
# df.to_html("Table.html", index=False, escape = False)
# html_file = df.to_html
