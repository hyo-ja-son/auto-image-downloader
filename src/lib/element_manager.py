from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By


chromedriver_autoinstaller.install()
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)

def findElement(css_selector:str):
    return driver.find_element(by=By.CSS_SELECTOR, value=css_selector)

def findElements(css_selector:str):
    return driver.find_elements(by=By.CSS_SELECTOR, value=css_selector)
    

def getValueFromAttribute(element, attribute:str):
    return element.get_attribute(attribute)

def moveToPage(url:str):
    driver.get(url)