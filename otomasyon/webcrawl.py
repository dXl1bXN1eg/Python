# https://github.com/unclecode/crawl4ai?tab=readme-ov-file

import asyncio
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup

async def fetch_page_content(url):
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url=url)
        return result.html

def extract_hacked_messages(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    messages = []
    for message in soup.find_all('div', class_='post'):
        if 'aranacak' in message.get_text().lower():
            link = message.find('a', href=True)
            messages.append({
                'content': message.get_text(strip=True),
                'link': link['href'] if link else 'No link found'
            })
    return messages

async def main():
    base_url = 'https://www.sacekimisonuclari.com/index.php?board=2.0;start='
    all_messages = []
    for i in range(0, 3500, 50):  # Örneğin, 70 sayfa için
        url = f'{base_url}{i}'
        html_content = await fetch_page_content(url)
        messages = extract_hacked_messages(html_content)
        all_messages.extend(messages)
        await asyncio.sleep(1)  # Sunucuyu aşırı yüklememek için bekleme süresi
    for message in all_messages:
        print(f"Link: {message['link']}\nİçerik: {message['content']}\n")

if __name__ == "__main__":
    asyncio.run(main())
