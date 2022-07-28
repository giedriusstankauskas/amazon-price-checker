import smtplib
import requests
from bs4 import BeautifulSoup
import lxml

# Price you want to spend on a product
BUY_PRICE = 140

# Product link
url = "https://www.amazon.com/Apple-MWP22AM-A-cr-AirPods-Renewed/dp/B0828BJGD2/ref=sr_1_5?crid=CX4H18LCXRQV&keywords=airpods&qid=1659004247&refinements=p_89%3AApple&rnid=2528832011&s=electronics&sprefix=airpods%2Caps%2C171&sr=1-5"

# Your headers according to http://myhttpheader.com/
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,lt;q=0.8"
}

response = requests.get(url, headers=header)
soup = BeautifulSoup(response.content, "lxml")

offscreen_spans = soup.find_all("span", class_="a-offscreen")
price_with_currency = offscreen_spans[0].getText()
price_without_currency = price_with_currency.split("$")[1]

price_as_float = float(price_without_currency)
title = soup.find(id="productTitle").getText().strip()

print(title)
print(price_as_float)

# Send email if product price is lower than your buy price
if price_as_float < BUY_PRICE:
    message = f"{title} is now {price_as_float}"

    # Add smtp address, email address and password
    with smtplib.SMTP(YOUR_SMTP_ADDRESS, port=587) as connection:
        connection.starttls()
        result = connection.login(YOUR_EMAIL, YOUR_PASSWORD)
        connection.sendmail(
            from_addr=YOUR_EMAIL,
            to_addrs=YOUR_EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}"
        )
