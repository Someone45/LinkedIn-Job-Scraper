import os 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def displaylist():
    driver = webdriver.Chrome()
    data_file_path = os.path.join(os.path.dirname(__file__), "Table.html")
    driver.get(data_file_path)
    time.sleep(999999)
