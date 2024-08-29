
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
from getpass import getpass

PORTAL_URL = "https://portal.gymnasium-oberstadt.de"

USERNAME = input("Username: ")
PASSWORD = getpass("Password: ")
MAX_LESSON_NUMBER = int(input("Max lesson number: "))

driver = webdriver.Firefox()
driver.get(PORTAL_URL)
assert "Portal" in driver.title
elem = driver.find_element(By.NAME, "username")
elem.send_keys(USERNAME)
elem = driver.find_element(By.NAME, "password")
elem.send_keys(PASSWORD)
elem.send_keys(Keys.RETURN)
time.sleep(3)
driver.get(f"{PORTAL_URL}/prnt/schueler_plan.php?id=1453")
script = 'document.styleSheets[0].insertRule("td:has(> .stdplan-eintrag) {background-color: #D9E3F0 !important;}", 0 )'
driver.execute_script(script)

elem = driver.find_element(By.CLASS_NAME, "stdplan-table")
script = "let children=document.getElementsByClassName('stdplan-table')[0].children[1].children;" + \
    "children[children.length-1].remove();"*(11-MAX_LESSON_NUMBER)
driver.execute_script(script)
elem.screenshot('images/lessons.png')
driver.close()

# optional: remove log file  # comment out if you want to keep it
os.remove("geckodriver.log")
