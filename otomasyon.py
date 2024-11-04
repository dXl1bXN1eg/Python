import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

with open('data_folder/bilgiler.txt', 'w', encoding='utf-8') as file:
    chrome_options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get('https://www.sacekimisonuclari.com')

        # Diğer sayfalara geçiş
        for page in range(34, 50):
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
                    # Başlık linkini al
                    title_link = row.find_element(By.XPATH, './/span[@id]/a').get_attribute('href')
                    title_links.append(title_link)  # Linki listeye ekle
                except BaseException:
                    pass

            # Depolanan linklere sırayla git
            for title_link in title_links:
                try:
                    driver.get(title_link)

                    try:
                        # İçerik sayfasında mesaj alanını al
                        message_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//div[@class="post"]/div[@class="inner"]'))
                        )
                        message_text = message_element.text

                    except Exception as e:
                        print("Mesaj alanı bulunamadı, sayfa kaynakları aranacak...")
                        # Sayfanın HTML içeriğini alın
                        page_source = driver.page_source
                        message_text = page_source

                    #pattern1 = r'\b(2[2-4][0-9]|250)\b'
                    #pattern2 = r'3\s*\.?\s*ay'

                    # İlk kontrolü yap
                    try:
                        if re.search(r'\b(2[2-4][0-9]|250)\b', message_text) or re.search(r'8\s*\.\s*ay|8\s*\.\s*ay', message_text, re.IGNORECASE):
                            element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/div/div[3]/form/div[1]/div/div[1]/h4/a'))
                            )
                            author = element.text
                            title = driver.title

                            file.write(f"Kullanıcı: {author}, Başlık: {title}, Link: {title_link}\n")
                            print(f"Kullanıcı: {author}, Başlık: {title}")
                    except BaseException:
                        print("\n\nKullanıcıları alamaadı Burada büyük bir sorun var hemen bakman lazım")

                    # Pagination kontrolü
                    current_url = driver.current_url
                    base_url, number = current_url.rsplit('.', 1)
                    number = int(number)

                    data_content = [] 
                    previous_html_size = 0 

                    for i in range(1, 22): 
                        next_page_url = f"{base_url}.{number + (i * 15)}"
                        try:
                            driver.get(next_page_url)

                            new_rows = WebDriverWait(driver, 10).until(
                                EC.presence_of_all_elements_located((By.XPATH, '//table/tbody/tr'))
                            )

                            html_size_new = len(driver.page_source)
                            data_content.append(html_size_new)

                            if html_size_new == previous_html_size:
                                break

                            previous_html_size = html_size_new

                            for new_row in new_rows:
                                try:
                                    new_title_link = new_row.find_element(By.XPATH, './/span[@id]/a').get_attribute('href')
                                    driver.get(new_title_link)

                                    try:
                                        # İçerik sayfasında mesaj alanını al
                                        message_element = WebDriverWait(driver, 10).until(
                                            EC.presence_of_element_located((By.XPATH, '//div[@class="post"]/div[@class="inner"]'))
                                        )
                                        message_text = message_element.text

                                    except Exception as e:
                                        print("Mesaj alanı bulunamadı, sayfa kaynakları aranacak...")
                                        # Sayfanın HTML içeriğini alın
                                        page_source = driver.page_source
                                        message_text = page_source

                                    try:
                                        if re.search(r'\b(2[2-4][0-9]|250)\b', message_text) or re.search(r'8\s*\.\s*ay|8\s*\.\s*ay', message_text, re.IGNORECASE):
                                            element = WebDriverWait(driver, 10).until(
                                                EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div[2]/div/div[3]/form/div[1]/div/div[1]/h4/a'))
                                            )
                                            author = element.text
                                            title = driver.title

                                            file.write(f"Kullanıcı: {author}, Başlık: {title}, Link: {new_title_link}\n")
                                            print(f"Kullanıcı: {author}, Başlık: {title}")
                                    except BaseException:
                                        print("\n\nKullanıcıları alamaadı Burada büyük bir sorun var hemen bakman lazım")

                                    driver.back()
                                    WebDriverWait(driver, 10).until(
                                        EC.presence_of_all_elements_located((By.XPATH, '//table/tbody/tr'))
                                    )

                                except BaseException:
                                    pass

                        except BaseException:
                            break  

                    driver.back()
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//table/tbody/tr'))
                    )

                except BaseException:
                    pass

    except BaseException:
        pass

    finally:
        driver.quit()
