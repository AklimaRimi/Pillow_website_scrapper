from selenium import webdriver
from selenium.webdriver.common.by import By
# Assuming you have a WebDriver instance (e.g., ChromeDriver) initialized
import time
driver = webdriver.Edge(f'msedgedriver.exe')

# Navigate to your webpage
driver.get(f"https://aibuzhijia.m.en.alibaba.com/")
driver.maximize_window()

# Find the div element by its class name
# div_element = driver.find_element_by_class_name("hide-item")

time.sleep(2)
container = driver.find_element(By.XPATH,'//*[@id="J_SC_header"]')
container.find_element(By.XPATH,"//div[@class='current-value']").click()

print(container.text)

inputs = container.find_elements(By.TAG_NAME,'input')
for i in inputs:
    print(i.get_attribute('placeholder'))
time.sleep(5)
# container.find_element(By.XPATH,'//*[@id="J_SC_header"]/header/div/div[3]/div[5]/div/div/div/div[2]/div[4]/div/div/div[2]/div/input').click()
# time.sleep(2)
driver.quit()