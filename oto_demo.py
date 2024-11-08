import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

download_folder = "downloaded_images"
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

with open('data_folder/user.txt', 'r', encoding='utf-8') as control:
    users = set(line.strip() for line in control)

with open('data_folder/new_data.txt', 'w', encoding='utf-8') as file:
    chrome_options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get('https://www.sacekimisonuclari.com')

        for page in range(0, 130):
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

            # Depolanan linklere sırayla git
            for title_link in title_links:
                try:
                    driver.get(title_link) 
                    element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/div/div[3]/form/div[1]/div/div[1]/h4/a'))
                    )
                    author = element.text

                    if author in users:
                        # Kullanıcı sayfasına gidildiğinde sayfa numarasını veya URL'yi kaydediyoruz
                        current_url = driver.current_url
                        print(f"{author} Sayfa: {current_url}")

                        # Sayfa linkinin sonundaki sayfa numarasını alıyoruz ve işlemi tekrar başlatıyoruz
                        base_url, number = current_url.rsplit('.', 1)
                        number = int(number)

                        tkq = 0
                        for i in range(1, 30):  # Sayfa numarası, sayfa başına 15 içerik ekleniyor
                            next_page_url = f"{base_url}.{number + (i * 15)}"
                            try:
                                driver.get(next_page_url)
                                page_source_length = len(driver.page_source)

                                username_elements = driver.find_elements(By.XPATH, '/html/body/div/div[2]/div[2]/div/div[3]/form/div[1]/div/div[1]/h4/a')
                                for username_element in username_elements:
                                    username = username_element.text
                                    if username in users:
                                        print(f"Sayfa İçlerindeki Eşleşen Kullanıcı: {username}")

                                        try:
                                            message_element = driver.find_element(By.XPATH, '//*[@id="msg_658546"]') 
                                            message = message_element.text
                                            print(f"{username} - Mesajı: \n{message}")
                                        except BaseException:
                                            pass

                                if page_source_length == tkq: 
                                    print("Sayfa değişmedi, geri dönülüyor.")
                                    driver.get(current_url)  # Sayfayı tekrar yükle
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
