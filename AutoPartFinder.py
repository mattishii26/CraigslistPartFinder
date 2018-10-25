from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import math
import time

#The part i'd like to find in AutoAndParts
print("Enter the location: ")
location = input()

print ("Enter the part you are looking for: ")
part = input()

driver = webdriver.Chrome('/Library/Python/2.7/site-packages/chromedriver')
driver.get("https://" + location + ".craigslist.org/search/pts")

#change to list view
elem = driver.find_element_by_class_name("dropdown-list")
elem.click()
elem = driver.find_element_by_id("listview")
elem.click()

#search the part
elem = driver.find_element_by_id("query")
elem.send_keys(part)
elem.submit()

print("Do you want to enter a price range? (Y/N) ")
priceRange = input()

if (priceRange.lower() == "y"):
    print("Enter the lower price: ")
    lowerPrice = input()
    print("Enter the upper price: ")
    upperPrice = input()
    driver.find_element_by_name('min_price').send_keys(lowerPrice)
    driver.find_element_by_name('max_price').send_keys(upperPrice)
    driver.find_element_by_xpath(
        '//*[@id="searchform"]/div[2]/div/div[7]/button')

filename = (part + ".csv")
f = open(filename, "w")
headers = "#, Date and Time Posted, Title, Link, Price\n"
f.write(headers)

TotalCount = 1

while(True):
    time.sleep(5)
    page = uReq(driver.current_url)
    pageHTML = page.read()
    page.close()
    page_soup = soup(pageHTML, "html.parser")

    postDates = page_soup.find_all('time', 'result-date')
    postTitles = page_soup.find_all('a', 'result-title hdrlnk')
    postLinks = page_soup.find_all('a', 'result-title hdrlnk')
    postPrice = page_soup.find_all('span', 'result-price')

    for j in range(0, len(postDates)):
        date = postDates[j].get('title')
        title = postTitles[j].text
        link = postLinks[j].get('href')
        price = postPrice[j].text

        line = str(TotalCount) + ',' + date + ',' + title.replace(',','|') + ',' + link + "," + price + "\n"
        TotalCount+=1
        f.write(line)

    try:
        #Clicking the next button
        driver.find_element_by_xpath(
            '//*[@id="searchform"]/div[5]/div[3]/span[2]/a[3]').click()

    except:
        print ("No more results for the item: " + part)
        break

f.close()
driver.quit()
