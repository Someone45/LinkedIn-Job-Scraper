from ftplib import all_errors
from socket import timeout
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

# Uncomment the line below if you'd like to scrape without a new Chrome window every time.

def linkedin_main(JobName, n):
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(options=options)
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
    time.sleep(3)

    #Finds Job Page & Begins Search
    JNumber = 0                                    #Increases by 1 to change to the next job
    JobType = "?f_JT=I"                            #For Internships
    City = "&f_PP=102571732"                       #New York, NY
    JobName = f"&keywords={JobName}".replace(' ', '%20')   #Name of Search
    Country = "&location=United%20States"          #US as default country
    Sort = "&sortBy=DD"                            #Sort by date (Can change this)
    PageNumber = f"&start="                        #The job that is being viewed
    job_number = 0                                 #The number assigned to the job html file description

    #Data Scraping
    #n = 3
    while n > 0:
        driver.get(f"https://www.linkedin.com/jobs/search/{JobType}{City}{JobName}{Country}{Sort}{PageNumber}{JNumber}")
        job_src = driver.page_source
        soup = BeautifulSoup(job_src, 'lxml')
        JNumber += 1
        time.sleep(1.5)
        sucess = False
        while sucess is False:
            try:
                #Find Job Title
                job_title = driver.find_element(By.XPATH, "//h2[@class='t-24 t-bold jobs-unified-top-card__job-title']").text.replace("\n", "<br>" )

                #Find Job Description
                job_description = driver.find_element(By.XPATH, "//*[@id='job-details']").text.replace('\n','<br>')

                #Find Date Posted
                date_posted = driver.find_element(By.XPATH, "//span[@class='jobs-unified-top-card__subtitle-secondary-grouping t-black--light']").text.split("ago")[0] + "ago".replace("\n", "<br>" )

                #Find Company Name
                company_name = driver.find_element(By.XPATH, "//a[@class='ember-view t-black t-normal']").text.replace("\n", "<br>" )

                #Get LinkedIN  Link
                try:
                    driver.find_element(By.XPATH, "//span[text()[normalize-space()='Easy Apply']]")
                    url = driver.current_url
                    url = f"<a href={url} target='_blank'>LinkedIN Link</a>"
                except NoSuchElementException:
                    try:
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//span[text()[normalize-space()='Apply']]"))).click()
                    except NoSuchElementException:
                        pass
                    time.sleep(2)
                    try:
                        close_prompt = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class = 'artdeco-modal__dismiss artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view']")))
                        close_prompt.click()
                        time.sleep(1)
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//span[text()[normalize-space()='Apply']]"))).click()
                    except Exception as e:
                        pass
                    time.sleep(5)
                    window_before= driver.window_handles[0]
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    url = driver.current_url
                    url = f"<a href={url} target='_blank'> Link </a>"
                    driver.close()
                    driver.switch_to.window(window_before)

                sucess = True
            except:
                time.sleep(5)

        #Obtain Company Link
        job_descc = []
        job_descc.append({"Desc": job_description})
        job_linked = f"<a href='jobdesc{job_number}.html' target='_blank'> Job Description Here </a>"
        jobs.append({"CompanyName": company_name,"JobTitle": job_title, "JobLink": url, "JobDescription": job_linked, "DatePosted": date_posted})
        n -= 1
        time.sleep(1)

        #Export Job Descriptions
        dfdesc = pd.DataFrame(job_descc)
        dfdesc.to_html(f"jobdesc{job_number}.html", index=False, escape = False)
        html_file = dfdesc.to_html
        job_number += 1

        print(f"Jobs Completed ({job_number}/{n})")

    # Converts the dataframe into str object with formatting
    df = pd.DataFrame(jobs)

    #Exports data as HTML
    df.to_json("Table.json", orient = 'records', indent = 2)

    print("SUCCESS")

linkedin_main("Publishing", 3)
