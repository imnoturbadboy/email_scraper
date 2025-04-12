import asyncio
import re
import argparse
import random
from urllib.parse import urlparse, urlunparse
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import aiofiles
import httpx
from fake_useragent import UserAgent

print("EMAIL_SCRAPER by [imnoturbadboy | https://github.com/imnoturbadboy]\n")

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

async def check_robots_txt(url):
    parsed_url = httpx.URL(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.host}/robots.txt"
    try:
        response = await httpx.get(robots_url)
        if response.status_code == 200:
            return response.text
    except Exception:
        return None
    return None

async def extract_emails_from_page(page):
    content = await page.content()
    emails = EMAIL_REGEX.findall(content)
    return set(emails)

async def handle_consent_forms(page, verbose):
    try:
        await page.wait_for_selector('button:has-text("Принять"), button:has-text("Согласен")', timeout=5000)
        await page.click('button:has-text("Принять"), button:has-text("Согласен")')
        if verbose:
            print("Согласие на использование cookies принято.")
    except Exception:
        if verbose:
            print("Форма согласия не найдена или не требуется.")

async def handle_captcha(page, verbose):
    try:
        await page.wait_for_selector('iframe[src*="captcha"], div:has-text("пожалуйста, подтвердите")', timeout=5000)
        if verbose:
            print("Обнаружена CAPTCHA. Перезагрузка страницы...")
        await page.reload()
        return True
    except Exception:
        return False

async def save_intermediate_results(all_emails, output_file):
    async with aiofiles.open(output_file, 'w') as f:
        for email in all_emails:
            await f.write(email + '\n')

def normalize_url(url):
    parsed_url = urlparse(url)
    query = parsed_url.query
    if query:
        params_to_remove = [
            'utm_',
            'fbclid',
            'gclid',
            'msclkid',
            'yclid',
            'dclid',
            'sessionid',
            'sid',
            'jsessionid',
            'sort',
            'order',
            'filter',
            'ref',
            'referrer',
            'trk',
            'tracking',
            'source',
            'campaign',
        ]

        new_query = '&'.join(
            part for part in query.split('&')
            if not any(part.startswith(prefix) for prefix in params_to_remove)
        )

        parsed_url = parsed_url._replace(query=new_query)
    return urlunparse(parsed_url)


async def crawl(url, depth, page, visited, all_emails, verbose, delay, max_pages):
    normalized_url = normalize_url(url)

    if depth == 0 or normalized_url in visited or len(visited) >= max_pages:
        return

    visited.add(normalized_url)
    try:
        if verbose:
            print(f"Переход к {normalized_url}...")
        await page.goto(normalized_url)
        await handle_consent_forms(page, verbose)

        if await handle_captcha(page, verbose):
            return

    except Exception as e:
        if verbose:
            print(f"Не удалось установить соединение с {normalized_url}: {e}")
        return

    emails = await extract_emails_from_page(page)
    all_emails.update(emails)

    await asyncio.sleep(delay)

    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')
    links = {a['href'] for a in soup.find_all('a', href=True)}

    for link in links:
        if link.startswith('/'):
            link = f"{url}{link}"
        elif not link.startswith('http'):
            continue

        await crawl(link, depth - 1, page, visited, all_emails, verbose, delay, max_pages)

async def main(urls, depth, output_file=None, protocol='https', proxy=None, verbose=False, delay=0, max_pages=10):
    visited = set()
    all_emails = set()
    ua = UserAgent()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()

        for url in urls:
            if not url.startswith('http://') and not url.startswith('https://'):
                url = f"{protocol}://{url}"

            robots_txt = await check_robots_txt(url)
            if robots_txt and "Disallow: /" in robots_txt:
                if verbose:
                    print(f"Доступ к {url} запрещен robots.txt")
                continue

            if verbose:
                print(f'Сбор email адресов для {url}...')
            page = await context.new_page()
            headers = {'User-Agent': ua.random}
            await page.set_extra_http_headers(headers)

            await crawl(url, depth, page, visited, all_emails, verbose, delay, max_pages)
            await page.close()

        await browser.close()

    if output_file:
        await save_intermediate_results(all_emails, output_file)
        print(f"Результаты сохранены в файл: {output_file}")
    else:
        print("Сбор завершен. Найденные email адреса:")
        for email in all_emails:
            print(email)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Email scrapper.')
    parser.add_argument('-u', '--url', type=str, help='URL для извлечения адресов электронной почты')
    parser.add_argument('-r', '--read', type=str, help='Файл для чтения доменов')
    parser.add_argument('-o', '--output', type=str, help='Файл для записи найденных адресов электронной почты')
    parser.add_argument('-d', '--depth', type=int, default=1, help='Глубина обхода сайта (по умолчанию 1)')
    parser.add_argument('-p', '--protocol', type=str, choices=['http', 'https'], default='https',
                        help='Протокол (http или https), по умолчанию https')
    parser.add_argument('--proxy', type=str, help='Прокси-сервер в формате http://user:pass@host:port')
    parser.add_argument('-v', '--verbose', action='store_true', help='Выводить подробную информацию о процессе')
    parser.add_argument('--delay', type=float, help='Задержка между запросами в секундах (по умолчанию случайное значение от 2 до 5 секунд)')
    parser.add_argument('--max_pages', type=int, default=10, help='Максимальное количество страниц для обхода (по умолчанию 10)') 

    args = parser.parse_args()

    if args.read:
        with open(args.read, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    elif args.url:
        urls = [args.url]
    else:
        print("Необходимо указать URL или файл с доменами.")
        exit(1)

    if args.delay is None:
        delay = random.uniform(2, 5)
    else:
        delay = args.delay

    asyncio.run(main(urls, args.depth, args.output, args.protocol, args.proxy, args.verbose, delay, args.max_pages))
