from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from re import sub
from decimal import Decimal
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import password

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
url = 'https://sfbay.craigslist.org/search/cto?'
driver.get(url)
RATE = .4


def calcAveragePrice(prices):
    total = 0
    for price in prices:
        total += price
    return total / len(prices)


def composeMail(sender_email, receiver_email, html, text):
    message = MIMEMultipart("alternative")
    message["Subject"] = "BARGAIN ALERT"
    message["From"] = sender_email
    message["To"] = receiver_email

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    return message


def sendMail(smtp_server, sender_email, password, message, port):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        # send email
        server.sendmail(sender_email, receiver_email, message.as_string())


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
        # print(link)
        carInfoDiv = driver.find_element_by_class_name("attrgroup")
        carInfo = carInfoDiv.text
        carPriceDiv = driver.find_element_by_class_name("price")
        carPrice = carPriceDiv.text
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

            resultPriceSpans = rows.find_elements_by_xpath(
                "//li[@class='result-row']//div[@class='result-info']//span[@class='result-meta']//span[@class='result-price']")
            resultPrices = []
            for span in resultPriceSpans:
                resultPrices.append(float(sub(r'[^\d.]', '', span.text)))
            averagePrice = calcAveragePrice(resultPrices)

            if Decimal(sub(r'[^\d.]', '', carPrice)) <= Decimal((averagePrice * RATE)):
                linksToEmail.append(link)

        except:
            print('Error Processing Car')

    if len(linksToEmail) > 0:
        port = 465
        smtp_server = "smtp.gmail.com"
        password = password.email_password
        sender_email = "craigslist.deals21@gmail.com"
        receiver_email = "phamtony21@gmail.com"

        text = f"""\
            Review the following deals:
            
            {linksToEmail}
            This message is sent from Python. """
        html = f"""\
            <html>
                <body>
                    <p>Review the following deals: </p>
                    {linksToEmail}
                    <p>This message is sent from Python.</p>
                </body>
            </html> """

        mail = composeMail(sender_email, receiver_email, html, text)
        sendMail(smtp_server, sender_email, password, mail, port)
finally:
    print('done')
