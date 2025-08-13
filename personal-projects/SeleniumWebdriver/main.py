from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.python.org/")
# dict_event = {}
# upcoming_event = driver.find_elements(By.XPATH, value='//*[@id="content"]/div/section/div[2]/div[2]/div/ul/li')
# for index, event in enumerate(upcoming_event):
#     time = event.find_element(By.TAG_NAME, value="time").get_attribute("datetime")
#     name = event.find_element(By.CSS_SELECTOR, value="li a").text
#     dict_event[index] = {"time": time, "name": name}
# print(dict_event)

event_times = driver.find_elements(By.CSS_SELECTOR, value=".event-widget time")
event_names = driver.find_elements(By.CSS_SELECTOR, value=".event-widget li a")

events = { n : {'time': event_times[n].text,
                'name': event_names[n].text} for n in range(len(event_times))}

print(events)
# price_dollar = driver.find_element(By.CLASS_NAME, value="a-price-whole")
# price_cents = driver.find_element(By.CLASS_NAME, value="a-price-fraction")
# print(f"The price is {price_dollar.text}.{price_cents.text}")

# search_bar = driver.find_element(By.NAME, value="q")
# print(search_bar.get_attribute("placeholder"))
#
# anchor_tag = driver.find_element(By.CSS_SELECTOR, value=".documentation-widget a")
# print(anchor_tag.text)

# bug_link = driver.find_element(By.XPATH, value='//*[@id="site-map"]/div[2]/div/ul/li[3]/a')
# print(bug_link.text)
driver.quit()