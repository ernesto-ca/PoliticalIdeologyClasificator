import os
import re
from datetime import datetime
import pandas as pd
from pandas import read_excel
import constants as const
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected_conditions
# TODO MAKE EACH FILE SCRAPPING IN A DIFFERENT CPU PROCESS, AND USE BLOCKS OF THREADS FOR THE CANDIDATES
def get_unions(union_value):
    unions = str(union_value).split(',')
    unions_numbers = ''
    for index, union in enumerate(unions):
        current = const.UNIONS_NAME.get(union.lower())
        if current:
            unions_numbers += str(current)
        if (index < len(unions) - 1 and current):
            unions_numbers += '-'
    return unions_numbers

list_of_excel = os.listdir(const.DOWNLOAD_PATH)
# Start with the lightest files
list_of_excel.reverse()
chrome_options = Options()
chrome_options.add_argument("--headless")
try:
    print(f"El Proceso compenzo a las: {datetime.now()}")
    for excel in list_of_excel:
        print(f"Empezando a procesar {excel}")
        data_frame = read_excel(f"{const.DOWNLOAD_PATH}\\{excel}")
        excel_name = excel.removesuffix(".xlsx")
        data_frame.columns = ['union', 'name', 'url_pdf']
        data_frame.dropna(subset=['union', 'name', 'url_pdf'], inplace= True)
        clean_data_frame = pd.DataFrame(columns = ['union', 'name', 'visions', 'proposals'])
        for index, candidate in enumerate(data_frame.itertuples()):
            try:
                driver = webdriver.Chrome(options=chrome_options)
                # extract id (the IDS are those that are 'n' long of numbers and has .pdf as suffix)
                id = str(re.findall(r'\d+.pdf',candidate.url_pdf)[0]).removesuffix(".pdf")
                driver.get(const.DETAILS_URL(id,const.CARGOS_NAME[excel_name].value))
                WebDriverWait(driver, 8).until(
                    expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, const.DYNAMIC_CANDIDATE_CARDS))
                )
                html_content = driver.page_source
                driver.close()
                soup = BeautifulSoup(html_content, "html.parser")
                visions = soup.find('div', attrs={'aria-labelledby' : const.FUNCTION_VISION_ID}).find('span').text
                visions += "\n" + soup.find('div', attrs={'aria-labelledby' : const.IMPART_VISION_ID}).find('span').text
                proposals = soup.find('div', attrs={'aria-labelledby' : const.PROPOSAL_CSS_ID}).find_all('span')
                proposals = "\n".join([p.text for p in proposals])
                new_record = pd.DataFrame(
                    {
                    'union': [get_unions(candidate.union)],
                    'name': [candidate.name],
                    'visions': [visions],
                    'proposals': [proposals]
                }
                )
                clean_data_frame = pd.concat([clean_data_frame, new_record], ignore_index= True)
            except Exception as error:
                print(f"Hubo un error al intentar obtener los datos de {candidate.name} con el id {id}, mensaje del error: {error}")
        clean_data_frame.dropna(subset=['visions', 'proposals'], inplace = True)
        clean_data_frame.to_csv(f"{const.PROCESSED_PATH}\\{excel_name.lower()}.csv")
        print(f"{excel} Procesado exitosamente.")
except Exception as error:
    print(f"Hubo un error al intentar extraer los datos: {error}")
finally:
    print(f"El Proceso termino a las{datetime.now()}")
