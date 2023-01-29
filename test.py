from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib import request
from time import sleep
from bs4 import BeautifulSoup, NavigableString, Tag

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("http://rhymethai.com")
driver.find_element(By.NAME, 'inputword').send_keys("กัน")#พิมขื่อ
driver.find_element(By.CSS_SELECTOR, '.btn:not(:disabled):not(.disabled)').click()#กดค้นหา
#a = driver.find_element(By.CLASS_NAME, "card-body")

"""
soup = BeautifulSoup(driver.page_source)#ดึงหน้าwebมา
element = soup.find(class_="text-center")#ตัดชื่อเว็บ
element.decompose()
element2 = soup.find(class_="form-inline justify-content-center")#ตัดปุ่มค้นหาของเว็บ
element2.decompose()
print(soup.get_text())
#soup2 = soup.find(class_="card-body")#เอาแค่ส่วนเนื้อหา
"""
#soup3 = BeautifulSoup(soup2)
soup = BeautifulSoup(driver.page_source)#ดึงหน้าwebมา
element = soup.find(class_="text-center")#ตัดชื่อเว็บ
element.decompose()
element2 = soup.find(class_="form-inline justify-content-center")#ตัดปุ่มค้นหาของเว็บ
element2.decompose()
soup = soup.find(class_="card-body")#เอาแค่ส่วนเนื้อหา
#soup = soup.prettify()
print(soup.getText("\n"))

