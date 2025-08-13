from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://ozh.github.io/cookieclicker/')
time.sleep(2)
en_lan = driver.find_element(By.CSS_SELECTOR, value="div#promptContent div#langSelect-EN")
en_lan.click()
time.sleep(1)
cookies_button = driver.find_element(By.ID, value="bigCookie")
start_time = time.time()
timeout = start_time + 60 * 5
while time.time() < timeout:
    cookies_button.click()
    if int(time.time() - start_time) % 20 == 0:
        products = driver.find_elements(By.CSS_SELECTOR, value="div.product")
        prices = driver.find_elements(By.CSS_SELECTOR, value="span.price")
        num_cookies = driver.find_element(By.ID, value="cookies").text.split(" ")[0].replace(",", "")
        cookies_count = int(num_cookies)
        affordable = {}

        for a in range(len(products)):
            price_text = prices[a].text.replace(",", "")
            if price_text.isdigit():
                price = int(price_text)
                if cookies_count >= price:
                    affordable[a] = products[a]

        if affordable:
            max_price = max(affordable.keys())
            affordable[max_price].click()


cps = driver.find_element(By.ID, value="cookiesPerSecond")
print(f"Cookies {cps.text}")

