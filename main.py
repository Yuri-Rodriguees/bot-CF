import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROMEDRIVER_PATH = './chromedriver/chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-logging')  # Desativa os logs
chrome_options.add_argument('--log-level=3')  # Minimiza os logs para erros
chrome_options.add_argument('--remote-debugging-port=0')
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

service = Service(CHROMEDRIVER_PATH)

def get_browser():
    try:
        return webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Erro ao inicializar o navegador: {str(e)}")
        return None

def run_script(nick_to_search):
    browser = get_browser()
    if not browser: return "Não foi possível iniciar o navegador"

    try:
        browser.get("https://br.crossfire.z8games.com/competitiveranking.html")
        
        search_box = WebDriverWait(browser, 20).until(
            EC.visibility_of_element_located((By.ID, "desk_search_text"))
        )
        
        search_box.send_keys(nick_to_search)
        search_box.submit()

        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//ul[@class='cfr-rank col-4b']"))
        )

        result_elements = browser.find_elements(By.XPATH, f"//ul[@class='cfr-rank col-4b']//li[@class='cfr-rank-name']/a[contains(text(), '{nick_to_search}')]")
        
        if not result_elements: return "Erro: Jogador não encontrado"

        profile_link = result_elements[0].get_attribute("href")
        browser.get(profile_link)
        
        rank_element = WebDriverWait(browser, 20).until(
            EC.visibility_of_element_located((By.XPATH, "(//div[@class='pastseason_tierText__3j7pS'])[4]"))
        )
        
        h5_text = rank_element.find_element(By.TAG_NAME, "h5").text
        h3_text = rank_element.find_element(By.TAG_NAME, "h3").text

        return f'\nRANK: {h5_text} - TOP: {h3_text.replace("#", "")}'

    except Exception as e:
        return f"Erro ao executar o script: {str(e)}"
    finally:
        browser.quit() if browser else None

if __name__ == "__main__":
    nick = input("Digite o nickname do jogador: ")
    result = run_script(nick)
    print(result)