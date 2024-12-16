from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from proxy import selenium_browser_wrapper
from pydantic import BaseModel
import pandas as pd



class Card(BaseModel):
    title:  str | None = None
    address: str | None = None
    rating: str | None = None
    ratings_count: str | None = None
    phone: str | None = None
    website: str | None = None
    age: str | None = None
    services_location: str | None = None
    services: str | None = None

    @classmethod
    def export_to_csv(cls, cards: list["Card"], file_name: str):
        df = pd.DataFrame([card.model_dump() for card in cards])
        df.to_csv(f"{file_name}.csv", index=False)

    @classmethod
    def export_to_excel(cls, cards: list["Card"], file_name: str, **kwargs):
        df = pd.DataFrame([card.model_dump() for card in cards])
        df.to_excel(f"{file_name}.xlsx", index=False, **kwargs)

    @classmethod
    def export_to_json(cls, cards: list["Card"], file_name: str, **kwargs):
        df = pd.DataFrame([card.model_dump() for card in cards])
        df.to_json(f"{file_name}.json", orient='records', **kwargs)

    @classmethod
    def export_to_html(cls, cards: list["Card"], file_name: str, **kwargs):
        df = pd.DataFrame([card.model_dump() for card in cards])
        df.to_html(f"{file_name}.html", index=False, **kwargs)

    @classmethod
    def export_to_sql(cls, cards: list["Card"], file_name: str, connection, **kwargs):
        df = pd.DataFrame([card.model_dump() for card in cards])
        df.to_sql(f"{file_name}.sql", connection, **kwargs)
            
            
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


def check_next(driver):
    try:
        next = driver.find_element(By.XPATH, '//div[@jsaction="JIbuQc:Zgvrhb;"]')
        if next is not None:
            return True
        else:
            return False
    except NoSuchElementException:
        return False
    
    
def get_card(driver):
    card = {}
    card_info = find_elements(driver, By.XPATH, 
                              title='//div[@class="rgnuSb tZPcob"]',
                              address='//div[@class="fccl3c"]',
                              rating='//div[@class="rGaJuf"]',
                              ratings_count='//div[@class="leIgTe"]',
                              phone='//div[@class="eigqqc"]',
                              website='//div[@class="Gx8NHe"]',
                              age='//span[@class="FjZRNe"]',
                              services_location='//div[@class="lDJsr"]',
                              services='//div[@class="AQrsxc"]'
                              )
    
    for key, value in card_info.items():
        if value:
            card[key] = value.get_attribute("innerText").strip()
        
    return Card(**card)


def get_all_cards(driver, url):
    all_cards = []
    tries = 3
    while tries > 0:
        try:
            driver.get(url)
            break
        except TimeoutException:
            tries -= 1
            
            
    all_boxes = driver.find_elements(By.XPATH, '//div[@data-test-id="organic-list-card"]')
    all_cards = []
    for i in range(len(all_boxes)):
        tries = 3
        while tries > 0:
            try:
                all_boxes[i].click()
                wait = WebDriverWait(driver, 10)
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="rgnuSb tZPcob"]'))
                )
                card = get_card(driver)
                print(card.title)
                all_cards.append(card)
                yield card
                break
            except TimeoutException :
                tries -= 1
                print(f"Entry not found, retrying: {tries}/3")
                if i == 0:
                    all_boxes[i+1].click()
                    all_boxes[i].click()
                else:
                    all_boxes[i-1].click()
                    all_boxes[i].click()
            
    return all_cards


def gmaps_scraper(query):
    results = 0
    next_btn = True
    all_cards = []
    while next_btn:        
        tries = 3
        while tries > 0:
            try:
                driver = Driver(uc=True)
                url = f"https://www.google.com/localservices/prolist?q={query}&src=2&lci={results}"
                for card in get_all_cards(driver, url):
                    all_cards.append(card)
                results += 20
                break
            except ElementClickInterceptedException:
                tries -= 1
            finally:
                next_btn = check_next(driver)
                if not next_btn:
                    print("End of the results.")
                    break
                driver.quit()
        
    return all_cards

 
all_cards = gmaps_scraper("Tatoo studios in Toronto")
Card.export_to_csv(all_cards, "Toronto")

# element = driver.find_element(By.XPATH, '//*[contains(text(), "Try using different filters")]')
