import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests


with open('data_folder/user.txt', 'r', encoding='utf-8') as control:
    users = set(line.strip() for line in control)

def download_image(image_url, save_path):
    try:
        # Resmi indir
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Resim indirildi: {save_path}")
        else:
            print(f"Resim indirilemedi: {image_url}")
    except BaseException:
        pass

def save_message_to_file(author, message, folder_path):
    try:
        message_file_path = os.path.join("/home/x/Desktop/Yapay Zeka/" + folder_path, f"{author}_message.txt")
        with open(message_file_path, 'a', encoding='utf-8') as f:
            f.write(message)
        print(f"Mesaj kaydedildi: {message_file_path}")
    except BaseException:
        pass

with open('data_folder/new_data.txt', 'w', encoding='utf-8') as file:
    chrome_options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get('https://www.sacekimisonuclari.com')

        for page in range(0, 11):
            page_number = page * 50
            page_link = f"https://www.sacekimisonuclari.com/index.php?board=2.{page_number}"

            print(f"Sayfa: {page} - URL: {page_link}")
            driver.get(page_link)

            rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//table/tbody/tr'))
            )

            title_links = []  

            for row in rows:
                try:
                    title_link = row.find_element(By.XPATH, './/span[@id]/a').get_attribute('href')
                    title_links.append(title_link)  
                except BaseException:
                    pass

            for title_link in title_links:
                try:
                    driver.get(title_link) 
                    element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/div/div[3]/form/div[1]/div/div[1]/h4/a'))
                    )
                    author = element.text
                    if author in users:
                        current_url = driver.current_url
                        print(f"{author} Sayfa: {current_url}")

                        base_url, number = current_url.rsplit('.', 1)
                        number = int(number)

                        tkq = 0
                        for i in range(1, 30): 
                            next_page_url = f"{base_url}.{number + (i * 15)}"
                            try:
                                driver.get(next_page_url)
                                page_source_length = len(driver.page_source)
                              
                                username_elements = driver.find_elements(By.XPATH, "//div[@class='poster']//h4/a")
                                for username_element in username_elements:
                                    username = username_element.text
                                    if username == author:
                                        print(f"Kullanıcı Adı: {username}")
                                        user_folder_path = os.path.join("downloaded_images", author)
                                        if not os.path.exists(user_folder_path):
                                            os.makedirs(user_folder_path)
                                            
                                        # Mesaj başlığı çekme
                                        message_title_elements = driver.find_elements(By.XPATH, "//div[@class='keyinfo']//h5/a")
                                        for message_title_element in message_title_elements:
                                            message_title = message_title_element.text
                                            print(f"Mesaj Başlığı: {message_title}")
                                            save_message_to_file(author, message_title, "downloaded_images/" + author)

                                        # Mesaj içeriği çekme
                                        message_content_elements = driver.find_elements(By.XPATH, "//div[@class='post']//div[contains(@id, 'msg_')]")
                                        for message_content_element in message_content_elements:
                                            message_content = message_content_element.text
                                            print(f"Mesaj İçeriği: {message_content}")
                                            save_message_to_file(author, message_content, "downloaded_images/" + author)

                                        image_elements = driver.find_elements(By.XPATH, "//div[@class='post']//img")
                                        for image_element in image_elements:
                                            image_url = image_element.get_attribute("src")
                                            if image_url and (image_url.endswith(".png") or image_url.endswith(".jpg") or image_url.endswith(".jpeg")):
                                                image_name = author + "/" +author + "__" + image_url.split("/")[-1]
                                                user_folder_path = os.path.join("downloaded_images", image_name)
                                                
                                                if not os.path.exists(user_folder_path):
                                                    os.makedirs(user_folder_path)

                                                download_image(image_url, user_folder_path)

                                if page_source_length == tkq: 
                                    print("Sayfa değişmedi, geri dönülüyor.")
                                    driver.get(current_url)  
                                    break  
                                else:
                                    tkq = page_source_length
                                    print("Sayfa içeriği güncellendi.")
                            except BaseException:
                                pass

                except BaseException:
                    pass

    except BaseException:
        pass

    finally:
        driver.quit()
