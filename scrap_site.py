import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

from database import most_recent_date, process_data

URL = 'https://webapp.spypoint.com/login'
CAMERA_URL = 'https://webapp.spypoint.com/camera/'
EMAIL = "rcollazo@gmail.com"
PASSWORD = "Hg7Zvbgss*&"


def scrape():
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    driver.get(URL)
    img_folder = {}

    delay = 3  # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'email')))
        print("Page is ready!")
        driver.find_element(By.ID, "email").send_keys(EMAIL)
        elem = driver.find_element(By.ID, "password")
        elem.clear()
        elem.send_keys(PASSWORD)
        elem.send_keys(Keys.RETURN)
        print("Page is logged In!!!")
        time.sleep(10)

        divs = driver.find_elements(By.CLASS_NAME, 'MuiTypography-body1')
        for div in divs:
            above_div = div.find_element(By.XPATH, "..")
            img_folder[above_div.get_attribute("id")] = div.text

        # if img_folder:
        #
        #     time.sleep(10)
        #     modal = driver.find_element(By.CLASS_NAME, "MuiDialog-paperFullScreen")
        #
        #     main_img = modal.find_element(By.TAG_NAME, "img").get_attribute("src")
        #     print("main image url ", main_img)
        #     # download_image(main_img, folder_key, image_key)

        date_img = {}
        if img_folder:
            for key, value in img_folder.items():
                driver.get(CAMERA_URL + key)
                time.sleep(20)
                i, j = 1, 2
                date_images = {}
                scroll_bottom = 500
                try:
                    while True:
                        elem = driver.find_element(By.XPATH, f'//*[@id="root"]/div[2]/div[3]/div/div[2]/div[{i}]')
                        i += 2

                        if value not in elem.text:
                            print("elem.text ", elem.text)

                            div_elem = driver.find_element(By.XPATH,
                                                           f'//*[@id="root"]/div[2]/div[3]/div/div[2]/div[{j}]')
                            j += 2

                            img_tags = div_elem.find_elements(By.TAG_NAME, "img")
                            img_ids = []

                            for img in img_tags:
                                img_ids.append(img.get_attribute("id"))

                            date_images[elem.text] = img_ids
                            driver.execute_script(f"window.scrollTo(0, {scroll_bottom})")
                            scroll_bottom += 500
                            time.sleep(5)
                except NoSuchElementException:
                    date_img[key] = date_images
                    continue

        print(img_folder)
        print(date_img)
        detail_list = []
        if date_img:
            for key, values in date_img.items():
                if values:
                    for date, img_list in values.items():
                        for img_id in img_list:
                            # append folder name and date
                            image_object = [key, img_folder[key], date, img_id]

                            driver.get(CAMERA_URL + key + "/photo/" + img_id)
                            time.sleep(10)
                            modal = driver.find_element(By.CLASS_NAME, "MuiDialog-paperFullScreen")
                            main_img = modal.find_element(By.TAG_NAME, "img").get_attribute("src")
                            print("main image url ", main_img)
                            # download_image(main_img, folder_key, image_key)
                            image_object.append(main_img)
                            detail_list.append(image_object)
        driver.close()
        if detail_list:
            print("detail list ", detail_list)
            process_data(detail_list)

    except TimeoutException:
        driver.close()
        print("Loading took too much time!")

    return None


if __name__ == "__main__":
    scrape()
