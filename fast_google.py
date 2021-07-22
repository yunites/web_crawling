from urllib.request import urlretrieve
from urllib.parse import quote_plus    # Korean support
from bs4 import BeautifulSoup as BS    # Essential module
from selenium import webdriver         # Google crolling
from tkinter import messagebox
import time
import os

keyword = input("Input keyword: ")
i_URL = f'https://www.google.com/search?q={quote_plus(keyword)}&sxsrf=ALeKk00OQamJ34t56QSInnMzwcC5gC344w:1594968011157&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjXs-7t1tPqAhVF7GEKHfM4DqsQ_AUoAXoECBoQAw&biw=1536&bih=754'

driver= webdriver.Chrome('C:/YJun_Python/web_crawling/chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver.get(i_URL)

# Scroll down
SCROLL_PAUSE_TIME = 1

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element_by_css_selector(".mye4qd").click()
        except:
            break
    last_height = new_height

html = driver.page_source
soup = BS(html, features = "html.parser")

img = soup.select('img')

i_list = []
count = 1

print("Searching...")
for i in img:
   try:
        i_list.append(i.attrs["src"])
   except KeyError:
        i_list.append(i.attrs["data-src"])


directory = input("File Name : ")

try:
    if not os.path.isdir("C:/YJun_Python/web_crawling/" + directory):
        os.makedirs("C:/YJun_Python/web_crawling/" + directory)
        time.sleep(1)
    else:
        pass
except:
    pass

file_path = f"C:/YJun_Python/web_crawling/{directory}/"

Num_file = input("The number of file : ")

print("Downloading...")
for i in i_list:
    urlretrieve(i, file_path + keyword + str(count) + ".jpg")
    count += 1
    if count == int(Num_file) + 1:
        break

driver.close()
print("FINISH")
messagebox.showinfo("Complete", "The files download is complete.")