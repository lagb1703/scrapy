from selenium import webdriver 
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

url = "https://www.mercadolibre.com.co/"

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

data = {'nombre':[], 'precio':[], 'descuento':[], 'imagen':[], 'link':[]}

def buscar(termino:str):
    driver.find_element(By.CSS_SELECTOR, "input#cb1-edit").send_keys(termino)
    driver.find_element(By.CSS_SELECTOR, "button.nav-search-btn").click()

def obtenerProductos(tamaño):
    while(len(data["nombre"]) < tamaño):
        lista = driver.find_elements(By.CSS_SELECTOR, "li .ui-search-result__wrapper .andes-card")
        print("analisando pagina")
        for elemento in lista:
            data["nombre"].append(elemento.find_element(By.CSS_SELECTOR, ".ui-search-item__group a h2").text)
            data["precio"].append(elemento.find_element(By.CSS_SELECTOR, ".andes-money-amount__fraction").text)
            data["descuento"].append(elemento.find_element(By.CSS_SELECTOR, ".andes-money-amount__fraction").text)
            data["imagen"].append(elemento.find_element(By.CSS_SELECTOR, "div .ui-search-link img").get_attribute("src"))
            data["link"].append(elemento.find_element(By.CSS_SELECTOR, "div .ui-search-link").get_attribute("href"))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        for i in driver.find_elements(By.CSS_SELECTOR, "a.andes-pagination__link.shops__pagination-link.ui-search-link"):
            if i.find_element(By.CSS_SELECTOR, "span").text == "Siguiente":
                i.click()

def main():
    buscar("computador")
    obtenerProductos(200)
    df = pd.DataFrame(data)
    df.to_csv("datosMercadoLibre.csv", index=False) 

if __name__ == "__main__":
    main()
    driver.close()