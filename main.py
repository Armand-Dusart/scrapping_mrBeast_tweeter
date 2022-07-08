
#%%
from Driver.Driver import Driver
from selenium.webdriver.common.by import By
from time import sleep
from random import randint
import pandas as pd

def getABreak(option:str) :
    print("Break...")
    if option == "low" :
        sleep(randint(1,3))
    elif option == "medium" :
        sleep(randint(4,6))
    elif option == "high" :
        sleep(randint(7,10))
    print("Resume...")

def getLink() :
    return f"https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html"

#%%
if __name__ == "__main__":  
    place = "18e Arr"
    data = []
    with Driver(r'Driver/chromedriver_win32/chromedriver.exe') as driver :
        driver.get(getLink())
        getABreak("medium")
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        getABreak("low")
        btn_showMore = [btn  for btn in driver.find_elements(By.CLASS_NAME,"byNma") if btn.get_attribute("data-automation") == "showMore"]
        btn_showMore[-2].click()
        getABreak("medium")
        checkBox = [i for i in driver.find_elements(By.CLASS_NAME,"yhGLv") if place in i.text][0]
        checkBox.click()
        getABreak("low")
        btn_showMore = [btn  for btn in driver.find_elements(By.CLASS_NAME,"ui_button") if btn.text == "Appliquer"][0]
        btn_showMore.click()
        getABreak("low")
        restaurants = driver.find_elements(By.CLASS_NAME,"zqsLh")

        for restaurant in restaurants :
            data.append({"name":restaurant.find_element(By.CLASS_NAME,"Lwqic").text.split(".")[1:],"note":restaurant.find_element(By.CLASS_NAME,"UctUV").get_attribute("aria-label").split(" ")[0],"avis":restaurant.find_element(By.CLASS_NAME,"IiChw").text.replace("(","").replace(")","")})


# %%
