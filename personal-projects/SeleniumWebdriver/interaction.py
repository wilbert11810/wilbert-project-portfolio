from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://en.wikipedia.org/wiki/Main_Page')

wiki_num = driver.find_element(By.XPATH, value='//*[@id="articlecount"]/ul/li[2]/a[1]')

search = driver.find_element(By.XPATH, value='//*[@id="p-search"]/a')
search.click()
search_input = driver.find_element(By.NAME, value='search')
search_input.send_keys("Python", Keys.ENTER)
# driver.quit()