import os 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(chrome_options=options)
data_file_path = os.path.join(os.path.dirname(__file__), "Table.html")
driver.get(data_file_path)
time.sleep(999999)
