from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
url = 'https://sfbay.craigslist.org/search/cto?'
driver.get(url)

MINPRICE = "1000"
MAXPRICE = "3000"
MINYEAR = "2006"
MINMILES = "1000"
MAXMILES = "120000"
# Set filters
inputMinPrice = driver.find_element_by_name("min_price")
inputMinPrice.send_keys(MINPRICE)

# inputMaxPrice = driver.find_element_by_css_selector("input.flatinput.max")
inputMaxPrice = driver.find_element_by_name("max_price")
inputMaxPrice.send_keys(MAXPRICE)

inputMinAutoYear = driver.find_element_by_name("min_auto_year")
inputMinAutoYear.send_keys(MINYEAR)

inputMinMiles = driver.find_element_by_name("min_auto_miles")
inputMinMiles.send_keys(MINMILES)

inputMaxMiles = driver.find_element_by_name("max_auto_miles")
inputMaxMiles.send_keys(MAXMILES)

bundleDuplicates = driver.find_element_by_name("bundleDuplicates")
bundleDuplicates.send_keys(Keys.SPACE)

# wait until page loads
# loop through all the result rows
# for each result, click on it grab the details of the car and pass it to another function which will search the car and determine if it is worth
# click back
links = []
linksToEmail = []
try:
    rows = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "rows"))
    )

    results = rows.find_elements_by_tag_name("li")
    count = 0
    for li in results:
        image = li.find_element_by_tag_name("a")
        link = image.get_attribute('href')
        links.append(link)

    count = 0
    for link in links:
        driver.get(link)
        if count > 5:
            break
        count += 1
        carInfoDiv = driver.find_element_by_class_name("attrgroup")
        carInfo = carInfoDiv.text
        carPriceDiv = driver.find_element_by_class_name("price")
        carPrice = carPriceDiv.text
        print(carPrice)
        driver.get('https://sfbay.craigslist.org/search/cto?')
        search = driver.find_element_by_id("query")
        search.send_keys(carInfo)
        searchBtn = driver.find_element_by_class_name("searchbtn")
        searchBtn.click()
        # loop through pages and compare price
        try:
            rows = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "rows"))
            )

            resultPriceSpans = rows.find_elements_by_class_name("result-price")
            print('1')
            for span in resultPriceSpans:
                print('2')
                print(span.text)
        finally:
            print('done with car')
finally:
    print('done')
