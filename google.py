from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tkinter import messagebox
from urllib.parse import quote_plus    # Korean support
from bs4 import BeautifulSoup as BS    # Essential module
from selenium import webdriver         # Google crolling
import time
import urllib.request
import os

# Open Chrome webdriver & Find keyword
keyword = input("Input keyword: ")
i_URL = f'https://www.google.com/search?q={quote_plus(keyword)}&sxsrf=ALeKk00OQamJ34t56QSInnMzwcC5gC344w:1594968011157&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjXs-7t1tPqAhVF7GEKHfM4DqsQ_AUoAXoECBoQAw&biw=1536&bih=754'
driver= webdriver.Chrome('C:/YJun_Python/web_crawling/chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver.get(i_URL)

print("Searching...")

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

print("File making...")

# Find or make file
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

# Collect image's Url
images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
count = 1

for image in images:
    try:
        image.click()
        time.sleep(1)
        imgUrl = driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img").get_attribute("src")

        # Download images
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(imgUrl, file_path + keyword + str(count) + ".jpg")
        count += 1
        if count == int(Num_file) + 1:
            break
        elif Num_file == "all":
            pass
    except:
        pass

# Close Chrome driver
driver.close()

print("FINISH")
messagebox.showinfo("Complete", "The files download is complete.")