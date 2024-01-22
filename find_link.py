from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

 

driver  = webdriver.Edge('msedgedriver.exe')

categories = ['',
              ]


data = []
for cat in categories:
    driver.get(f'{cat}')
    time.sleep(2)

    run = True
    button_list = driver.find_element(By.XPATH,'//div[@class="next-pagination-list"]')

    buttons = button_list.find_elements(By.TAG_NAME,'button')

    print(len(buttons))
    
    for i in range(len(buttons)-1):
        links = driver.find_elements(By.XPATH,'//a[@class="product-image"]')


        for link in links:
            data.append(link.get_attribute('href'))
        time.sleep(5)
        driver.find_element(By.XPATH,'//button[@class="next-btn next-btn-normal next-btn-medium next-pagination-item next"]').click()

data = pd.DataFrame(data,columns=['links'])
data.to_csv('links.csv',index=False)
driver.close()


df = pd.read_csv('links.csv')

df = df.drop_duplicates()

print(len(df))

df.to_csv('links.csv',index=False)
