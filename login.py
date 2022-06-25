from asyncore import close_all
from ftplib import all_errors
from socket import timeout
import click
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import json
from tabulate import tabulate

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
n = 3 
while n > 0:
    driver.get(f"https://www.linkedin.com/jobs/search/{JobType}{City}{JobName}{Country}{Sort}{PageNumber}{JNumber}")
    job_src = driver.page_source
    soup = BeautifulSoup(job_src, 'lxml')
    JNumber += 1
    # f = open("info.txt", "a")
    # f.write(str(soup))
    # f.close()

    #Find Job Title


    job_title = soup.find_all('h2', {'class': 't-24 t-bold jobs-unified-top-card__job-title'})
    job_titles = []
    for title in job_title:
        job_titles.append(title.text.strip())

    # f = open("jobtitle.txt", "a")
    # f.write(str(job_titles[0]) + "\n" )
    # f.close()
    #Find Job Description
    job_description = driver.find_element(By.XPATH, "//*[@id='job-details']").text
    timeout(1)
    # print(job_description)
    # f = open("jobdesc.txt", "a")
    # f.write(job_description + "\n @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ \n @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # f.close()

    jobs.append({"Job Title": job_titles[0], "Job Description": job_description})
    n -= 1
    time.sleep(1)

# Converts the dataframe into str object with formatting

df = pd.DataFrame(jobs)
df.to_html("Table.htm", index=False)
html_gile = df.to_html
# df.to_csv("datafile.csv", index=False)

#apply_click = driver.find_element(By.XPATH,"//button[@class='jobs-apply-button artdeco-button artdeco-button--icon-right artdeco-button--3 artdeco-button--primary ember-view']").click()


#Click Exit Prompt 

# time.sleep(2)
# try:
#     close_prompt = driver.find_element(By.XPATH, "//button[@class = 'artdeco-modal__dismiss artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view']")
#     close_prompt.click()
# except Exception as e:
#     pass

#DONT FORGET TO ADD
