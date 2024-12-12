from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

def find_element(driver, by, value):
    try:
        return driver.find_element(by, value)
    except NoSuchElementException:
        return None

def find_elements(driver, by, **kwargs):
    all_elements = {}
    for key, value in kwargs.items():
        element = find_element(driver, by, value)
        all_elements[key] = element
    return all_elements

driver = Driver(uc=True)
url = "https://www.google.com/localservices/prolist?q=tattoo studios in australia&src=2&lci=0&scp=ChBnY2lkOnRhdHRvb19zaG9wKhNFc3R1ZGlvIGRlIHRhdHVhamVz"
driver.get(url)
all_cards = driver.find_elements(By.XPATH, '//div[@data-test-id="organic-list-card"]')
for card in all_cards:
    card.click()
    time.sleep(2)
    # card_info = find_elements(driver, By.XPATH, 
    #                           title='//div[@class="rgnuSb tZPcob"]',
    #                           address='//div[@class="fccl3c"]',
    #                           rating='//div[@class="rGaJuf"]',
    #                           ratings_count='//div[@class="leIgTe"]',
    #                           phone='//div[@class="eigqqc"]',
    #                           website='//div[@class="Gx8NHe"]',
    #                           services='//div[@class="AQrsxc"]',
    #                           services_location='//div[@class="lDJsr"]')
    # print(f"NEW ENTRY")
    # for key, value in card_info.items():
    #     if value is not None:
    #         print(f"{key}: {value.text}")
    mark = find_element(driver, By.XPATH, '//div[@class="lDJsr"]')
    if mark:
        print(mark.get_attribute("aria-label"))
    