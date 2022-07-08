
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class Driver(object):
    def __init__(self, webdriver_path):
        self.webdriver_path = webdriver_path
      
    def __enter__(self):
        option = webdriver.ChromeOptions()
        option.add_argument("start-maximized")
        self.driver = webdriver.Chrome(service=Service(self.webdriver_path),options=option)
        return self.driver
  
    def __exit__(self,*args,**kwargs):
        self.driver.close()
        