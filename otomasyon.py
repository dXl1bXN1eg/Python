import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

output_folder = "/home/x/Desktop/Yapay Zeka/Messages"  

with open('link.txt', 'r', encoding='utf-8') as control:
    link_info = [line.strip() for line in control]  
    links = [url.split(' - ')[0] for url in link_info]  
    usernames = [url.split(' - ')[1] for url in link_info] 

def save_message_to_file(author, message, folder_path):
    try:
        user_file_path = os.path.join(folder_path, f"{author}_messages.txt")
        with open(user_file_path, 'a', encoding='utf-8') as f:
            f.write(message + "\n")
        print(f"Message saved for user: {author}")
    except Exception as e:
        print(f"Error saving message for user {author}: {e}")

chrome_options = Options()
chrome_options.add_argument("--headless")  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

for url, username in zip(links, usernames):
    try:
        link_folder = os.path.join(output_folder, url.split('/')[-1])  
        if not os.path.exists(link_folder):
            os.makedirs(link_folder)
        
        driver.get(url)
        print(url)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='windowbg']")))
        posts = driver.find_elements(By.XPATH, "//*[@class='windowbg']")
        
        for post in posts:
            try:
                users = post.find_element(By.XPATH, ".//a[contains(@title, 'Profilini görüntüle')]").text
                message = post.find_element(By.XPATH, ".//div[@class='post']").text
                save_message_to_file(username, "Username: " + users + " \n " + message, link_folder)  
            except BaseException:
                pass

        current_url = driver.current_url
        base_url, number = current_url.rsplit('.', 1)
        number = int(number)

        tkq = 0
        for i in range(1, 30): 
            next_page_url = f"{base_url}.{number + (i * 15)}"
            try:
                driver.get(next_page_url)
                print(next_page_url)
                page_source_length = len(driver.page_source)

                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='windowbg']")))
                posts = driver.find_elements(By.XPATH, "//*[@class='windowbg']")
                for post in posts:
                    try:
                        users = post.find_element(By.XPATH, ".//a[contains(@title, 'Profilini görüntüle')]").text
                        message = post.find_element(By.XPATH, ".//div[@class='post']").text
                        save_message_to_file(username, "Username: " + users + " \n " + message, link_folder)
                    except BaseException:
                        pass

                if page_source_length == tkq: 
                    print("Sayfada değişiklik yok, orijinal URL'ye dönülüyor.")
                    driver.get(current_url)  
                    break  
                else:
                    tkq = page_source_length
                    print("Sayfa içeriği güncellendi.")

            except BaseException:
                pass

        print("Bu bağlantının işlenmesi tamamlandı, bir sonraki bağlantıya geçiliyor.\n")

    except BaseException:
        pass

driver.quit()
