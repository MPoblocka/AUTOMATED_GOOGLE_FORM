#Import of required packages
from bs4 import BeautifulSoup
import requests
import lxml
import selenium
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

CHROME_DRIVER_PATH = "DRIVER_PATH"

GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfEg662rnWayscE1d-RMwULMnF62t6byWsCKjDO-q8rqMJRnQ/viewform?usp=sf_link"
#Essential informations needed to scrape the data found using http://myhttpheader.com/
header = {
    "User-Agent": "INFORMATION",
    "Accept-Language": "INFORMATION"
}

#Searching for houses to rent in New York
response= requests.get("https://www.zillow.com/homes/New-York,-NY_rb/",headers=header)
contents= response.text

#Use BeautifulSoup to get the data we need
soup= BeautifulSoup(contents,"html.parser")

#Navigate to the links representing listed properties
all_link_elements = soup.select(".list-card-top a")

#Create list of links to properties
links = []
for link in all_link_elements:
    proper_link= link.get("href")
    if "http" not in proper_link:
        links.append(f"https:/www.zillow.com{proper_link}")
    else:
        links.append(proper_link)

#Create list of matching prices
prices= []
all_price_elements = soup.find_all("div",class_="list-card-price")
for price in all_price_elements:
    new_price = price.getText()
    if "+ 1 bd" in new_price:
        new_price2 = new_price.strip("+ 1 bd")
        prices.append(new_price2)
    elif "+/mo" in new_price:
        new_price3 = new_price.strip("+/mo")
        prices.append(new_price3)
    elif "/mo" in new_price:
        new_price4 = new_price.strip("+/mo")
        prices.append(new_price4)
    else:
        prices.append(new_price)

#Create a list of matching addresses using list comprehension
all_address_elements = soup.select(".list-card-addr")
addresses= [addresses.append(address.getText()) for address in all_address_elements]

#Selenium to open and fill the google_form
s = Service(CHROME_DRIVER_PATH)

#Prevent chrome from closing

chrome_options = Options()
chrome_options.add_experimental_option("detach",True)
driver = webdriver.Chrome(service=s,options=chrome_options)


def fill_the_form():

    for number in range(len(links)):
        driver.get(GOOGLE_FORM_URL)
        time.sleep(5)

        address_question = driver.find_element(By.XPATH,"//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
        address_question.send_keys(f"{addresses[number]}")
        time.sleep(2)

        price_question = driver.find_element(By.XPATH,"//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
        price_question.send_keys(f"{prices[number]}")
        time.sleep(2)

        link_question = driver.find_element(By.XPATH,"//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
        link_question.send_keys(f"{links[number]}")
        time.sleep(2)

        send_button = driver.find_element(By.XPATH,"//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span/span")
        send_button.click()
        time.sleep(2)

        another_answer_button = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
        another_answer_button.click()



fill_the_form()




