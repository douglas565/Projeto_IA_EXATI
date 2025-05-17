import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Configurações
load_dotenv()
EXATI_URL = os.getenv('EXATI_URL')
EXATI_USER = os.getenv('EXATI_USER')
EXATI_PASS = os.getenv('EXATI_PASSWORD')
SCREENSHOT_DIR = "screenshots"

class ExatiCrawler:
    def __init__(self):
        self.driver = webdriver.Chrome()
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    def login(self):
        """Realiza login no EXATI"""
        self.driver.get(f"{EXATI_URL}/login")
        self.driver.find_element(By.ID, "username").send_keys(EXATI_USER)
        self.driver.find_element(By.ID, "password").send_keys(EXATI_PASS)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)  # Aguarda carregamento

    def search_by_id(self, id_saac):
        """Busca um ID SAAC e captura a imagem da luminária"""
        try:
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "search_input"))
            search_box.clear()
            search_box.send_keys(id_saac)
            self.driver.find_element(By.ID, "search_button").click()
            
            # Aguarda elemento da luminária
            luminaire = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "luminaire-container")))
            
            # Captura screenshot
            screenshot_path = f"{SCREENSHOT_DIR}/{id_saac}.png"
            luminaire.screenshot(screenshot_path)
            return screenshot_path

        except Exception as e:
            print(f"Erro ao buscar ID {id_saac}: {str(e)}")
            return None

    def close(self):
        self.driver.quit()

# Exemplo de uso
if __name__ == "__main__":
    crawler = ExatiCrawler()
    crawler.login()
    result = crawler.search_by_id("SAAC-001")  # ID de teste
    if result:
        print(f"Imagem salva em: {result}")
    crawler.close()