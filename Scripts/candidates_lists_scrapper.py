import constants as const
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as expected_conditions

try:
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": const.DOWNLOAD_PATH,
        "download.prompt_for_download": False,
        "safebrowsing_for_trusted_sources_enabled": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,
    })
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(const.MAIN_URL)
    WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, const.MODAL_CLOSE_CLASS))
        )
    driver.find_element(By.CLASS_NAME, const.MODAL_CLOSE_CLASS).click()
    time.sleep(1)
    dynamic_index = 1
    while(dynamic_index <= len(const.CARGOS_NAME)):
        dynamic_area = const.DYNAMIC_COLLAPSE_ID_SELECTOR(dynamic_index)
        WebDriverWait(driver, 3).until(
            expected_conditions.presence_of_element_located((By.ID, dynamic_area))
        )
        dynamic_content = driver.find_element(By.ID, dynamic_area)
        driver.execute_script("arguments[0].scrollIntoView(true);", dynamic_content)
        time.sleep(2)
        dynamic_content.click()
        time.sleep(1)
        WebDriverWait(driver, 3).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, const.DYNAMIC_COLLAPSE_CONTENT_CLASS_NAME))
        )
        dynamic_area_content = driver.find_element(By.CSS_SELECTOR, const.DYNAMIC_COLLAPSE_CONTENT_CLASS_NAME)
        download_button = dynamic_area_content.find_element(By.TAG_NAME, "button")
        download_button.click()
        time.sleep(3)
        # Rename file
        list_of_files = os.listdir(const.DOWNLOAD_PATH)
        full_paths = [os.path.join(const.DOWNLOAD_PATH, f) for f in list_of_files]
        latest_file = max(full_paths, key=os.path.getctime)
        os.rename(latest_file, os.path.join(const.DOWNLOAD_PATH, f"{const.CARGOS_NAME(dynamic_index).name}.xlsx"))
        dynamic_index += 1
except Exception as error:
    print(f"Hubo un error al intentar extraer los datos {error}")
finally:
    driver.quit()