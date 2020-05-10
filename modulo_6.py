from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def buscar(output):
    driver = webdriver.Chrome(
             executable_path=r"chromedriver.exe"
             )
    
    driver.get("https://www.google.com/maps")
    
    try:
        buscar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="searchboxinput"]'))
        )
        buscar.send_keys(output)
        buscar.send_keys(Keys.ENTER)
        return
    except Exception as e:
        print('Ha ocurrido un error: ', e)
        driver.quit()
        return