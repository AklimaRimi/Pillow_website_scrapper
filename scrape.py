import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
import requests
import os
import warnings
import pandas as pd 

warnings.filterwarnings('ignore')
os.makedirs('Images',exist_ok= True)


driver = webdriver.Edge('msedgedriver.exe')
driver.maximize_window()
df = pd.read_csv('Product_information.csv')
search_link = pd.read_csv('links.csv')
search_link = search_link['links'].values.tolist()


if len(os.listdir("Images")) > 0:
    cnt = len(os.listdir("Images"))+1
else:
    cnt = 0
    
last = df['website_link'].values.tolist()[-1]

ind = search_link.index(last)

for link in search_link[ind+1:]:
        driver.get(f'{link}')
        time.sleep(2)
        
        name = driver.find_element(By.XPATH,'//*[@id="container"]/div[2]/div[1]/div[1]/div[1]/div/h1').text
        time.sleep(1)
        try: 
            driver.find_element(By.XPATH,'//*[@id="container"]/div[2]/div[1]/div[1]/div[6]/div/div/div[3]/a').click()
        except:
            driver.find_element(By.XPATH,'//*[@id="container"]/div[2]/div[1]/div[1]/div[6]/div/div/div[4]/a').click()
        time.sleep(1)
        other_attributes = driver.find_element(By.XPATH, '//div[@class="attribute-info"]/h4[text()="Other attributes"]/following-sibling::div[@class="attribute-list"]').text
    
        brand_name = ''
        model_number = ''
        material =''
        
        other_attributes = other_attributes.split('\n')
        for att in other_attributes:            
            if 'Model Number' in str(att):
                model_number = str(att)[12:]
            if 'Material' in str(att):
                material = str(att)[8:]
        
        time.sleep(1)
        
        
        img_loc = []
        img_links = []
        imgs = driver.find_elements(By.XPATH,'//div[@class="image-list-item-mask"]')
        print('total images',len(imgs))
        time.sleep(1)
        try:
            imgs[0].click()
        except:
            driver.find_element(By.XPATH,'//*[@id="container"]/div[2]/div[1]/div[1]/div[4]/div/div/div[1]/div[2]/div[2]').click()
        for i in range(0,len(imgs)):
            try:
                
                time.sleep(1)
                driver.find_element(By.XPATH,'//div[@class="arrow-link arrow-link-button arrow-link-right "]').click()
                time.sleep(1)
                
                img_link = driver.find_element(By.XPATH,"//img[@class='detail-main-img']").get_attribute('src')
                img_links.append(img_link)
                img = Image.open(requests.get(img_link, stream = True).raw)
                
                img.save(f'Images/{cnt}.jpg')
                img_loc.append(f'Images/{cnt}.jpg' )
                cnt+=1
            except:
                img_link = driver.find_element(By.XPATH,"//img[@class='detail-main-img']").get_attribute('src')
                img_links.append(img_link)
                img = Image.open(requests.get(img_link, stream = True).raw)
                
                img.save(f'Images/{cnt}.jpg')
                img_loc.append(f'Images/{cnt}.jpg' )
                cnt+=1
                break
            
        driver.execute_script("window.scrollTo(0, 100);")
        time.sleep(1)
        try:
            driver.find_element(By.XPATH,'//a[@class="image selected"]').click()
        except:
            driver.find_element(By.XPATH,'//*[@id="container"]/div[2]/div[1]/div[2]/div/div/div/div[4]/div/div[2]/div[1]/a').click()
        time.sleep(1)
        size = driver.find_element(By.XPATH,'//span[@class="text"]').text
        time.sleep(1)
        price_1 = driver.find_element(By.XPATH,'//span[@class="price"]').text
        time.sleep(1)
        try:
            color = driver.find_element(By.XPATH,'//*[@id="container"]/div[2]/div[3]/div[2]/div/div[1]/div[2]/div/h4[1]/span').text
        except:        
            color = driver.find_element(By.XPATH,'//*[@id="container"]/div[2]/div[1]/div[2]/div/div/div/div[4]/div/div[2]/h4[1]/span').text
        li = [[link,name, size, price_1,color,model_number,material,img_loc,img_links]]
        df = pd.DataFrame(li)
        df.to_csv('Product_information.csv',index=False,mode='a',header=False)

driver.quit()


df = pd.read_csv('Product_information.csv')

df = df.drop_duplicates()
df.to_csv('Product_information.csv',index=False )



