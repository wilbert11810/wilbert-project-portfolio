from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://secure-retreat-92358.herokuapp.com/')

first_name = driver.find_element(By.NAME, value="fName")
last_name = driver.find_element(By.NAME, value="lName")
email = driver.find_element(By.NAME, value="email")
submit = driver.find_element(By.CSS_SELECTOR, value="button")
first_name.send_keys("Wilbert")
last_name.send_keys("Wilbert")
email.send_keys("wilbertkruskie@gmail.com")
submit.click()
# driver.quit()