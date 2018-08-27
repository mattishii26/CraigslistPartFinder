from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import math
import time

#The part i'd like to find in AutoAndParts
part = "subaru"
location = "sfbay"

#open webbrowser
driver = webdriver.Firefox()
driver.get("https://" + location + ".craigslist.org/search/pts")
elem = driver.find_element_by_class_name("dropdown-list")
elem.click()

#change to list view
elem = driver.find_element_by_id("listview")
elem.click()

#search the part
elem = driver.find_element_by_id("query")
elem.send_keys(part)
elem.submit()

filename = "CLPartFinder.csv"
f = open(filename, "w")
headers = "#, Date and Time, Title, Link\n"
f.write(headers)

noNextPage = 0 #true or false for nextPage
TotalCount = 1

while(noNextPage == 0):
    time.sleep(5)
    page = uReq(driver.current_url)
    pageHTML = page.read()
    page.close()
    page_soup = soup(pageHTML, "html.parser")

    postDates = page_soup.find_all('time', 'result-date')
    postTitles = page_soup.find_all('a', 'result-title hdrlnk')
    postLinks = page_soup.find_all('a', 'result-title hdrlnk')

    for j in range(0, len(postDates)):
        date = postDates[j].get('title')
        title = postTitles[j].text
        link = postLinks[j].get('href')

        line = str(TotalCount) + ',' + date + ',' + title.replace(',','|') + ',' + link + "\n"
        TotalCount+=1
        f.write(line)

    try:
        elem = driver.find_element_by_class_name('button.next')
        elem.click()

    except ElementNotInteractableException:
        noNextPage = 1

f.close()

driver.quit()



