# Required libraries
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re
import logging

class StoreAllDividends():
    dividend_list = []
    def set(self, stock, current_value, dividend, exdivdate, paydivdate, amountpershare):
        self.dividend_list.append((stock,current_value,dividend,exdivdate,paydivdate,amountpershare))
    def get(self):
        return self.dividend_list
    
class HL():
    def setUp(self):
        # Define Brave path
        brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        options = webdriver.ChromeOptions()
        options.binary_location = brave_path
        options.add_experimental_option("detach", True)
        options.add_argument("--headless")

        # Create new automated instance of Brave
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        # Required for brave ^^

    def getStockInfo(self, stock):
        driver = self.driver
        driver.get("http://www.hl.co.uk/search")

        driver.find_element(By.XPATH, '//*[@id="acceptCookieButton"]').click()
        
        elem = driver.find_element(By.XPATH, '//*[@id="searchBar"]/div[1]/input[1]')
        elem.send_keys(stock[0])
        elem.send_keys(Keys.RETURN)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/a')))
            print(stock[0])
            try:
                driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/h2/a')
                is_big_thing = True
            except Exception as e:
                is_big_thing = False
                
            if is_big_thing:
                driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/h2/a').click()
            else:
                try:
                    driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/a').click()
                except:
                    driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[1]/div[1]/a').click()
                
            dividend = driver.find_element(By.XPATH, '//*[@id="security-detail"]/div[1]/div[11]/strong').text
            print(dividend)
            header = driver.find_element(By.XPATH, '//*[@id="security-title"]/h1').get_attribute("innerText")
            header = re.sub("^(.*?)\(", "",header)
            header = re.sub("\)([\s\S]*)$","",header)
            print(header)
            
            present = False
            try:
                driver.find_element(By.XPATH, '//*[@id="dividend-table"]/tbody/tr[1]/td[2]')
                present = True
            except Exception as e:
                present = False
                
            if present:
                exdivdate = driver.find_element(By.XPATH, '//*[@id="dividend-table"]/tbody/tr[1]/td[2]').text
                paydivdate = driver.find_element(By.XPATH, '//*[@id="dividend-table"]/tbody/tr[1]/td[3]').get_attribute("innerText")
                amountpershare = driver.find_element(By.XPATH, '//*[@id="dividend-table"]/tbody/tr[1]/td[4]').text
                amountpershare = re.sub("[^0-9.]+","", amountpershare)
                earnings = (float(amountpershare)/100) * float(stock[1])
                earnings = round(earnings, 2)
            else:
                exdivdate = "Unknown"
                paydivdate = "Unknown"
                amountpershare = 0
                
            try:    
                current_stock_value = driver.find_element(By.XPATH, '//*[@id="ls-bid-'+header+'-L"]').get_attribute("innerText")
            except:
                current_stock_value = driver.find_element(By.XPATH, '//*[@id="security-price"]/div/div/div[1]/div/div[1]/div[1]/span[2]').get_attribute("innerText")
            
            current_stock_value = re.sub("[^0-9.]+","",current_stock_value)
            current_shares_value = float(current_stock_value)/100 * float(stock[1])
            current_shares_value = round(current_shares_value,2)
            
            #Store data
            print(stock[0], current_shares_value, dividend, exdivdate, paydivdate, "£" + str(earnings))
            sad.set(stock[0], current_shares_value, dividend, exdivdate, paydivdate, "£" + str(earnings))
        except Exception as e:
            print(e)
            
    def tearDown(self):
        self.driver.close()

sad = StoreAllDividends()
if __name__ == "__main__":
    #Random List of stocks to test
    #("BATS",57), ("IMB",106), ("Rio Tinto",41), ("BHP",84), ("BP",517), ("Glencore",461), ("Shell",144), 
    #stock = input("Enter name of stock: ")
    #stocks = [("BARRICK GOLD CORP",76), ("Realty Income",33), ("Sibanye Stillwater Limited", 125), ("Woodside Energy Group", 15)]
    stocks = [("BATS",57), ("IMB",106), ("Rio Tinto",41), ("BHP",84), ("BP",517), ("Glencore",461), ("Shell",144)]
    hl = HL()
    for i in stocks:
        hl.setUp()
        hl.getStockInfo(i)
        hl.tearDown()
    print(sad.get())
   
#URL = "https://www.hl.co.uk/shares/shares-search-results/h/hsbc-holdings-plc-ordinary-usd0.50"
#page = requests.get(URL)
#soup = BeautifulSoup(page.content, "html.parser")

#results = soup.find_all("div", string="Elsie")
#print(soup)