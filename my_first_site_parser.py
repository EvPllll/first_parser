import asyncio # встроенная библиотека для ассинхронности

import aiohttp # помогает получать html-код
from bs4 import BeautifulSoup as BS # парсер
from fake_useragent import UserAgent # анонимайзер (без него многие сайты могут не пускать к html)

headers = {"User-Agent": UserAgent().random} # создали "пользователя" для анонимайзера

async def main(): # ассинхронная функция
    async with aiohttp.ClientSession() as session: # запускаем ассинхронную сессию
        for page in range(1, 7): # на сайте 7 страниц, поэтому пробегаемся циклом по страницам
            base_url = f'https://arbuz.kz/ru/collections/249088-skidki_do_40_na_napitki?available=1&limit=48&page={page}#/'
            # это ссылка на сайт, цикл "бежит" по страницам, для каждой страницы:
            async with session.get(base_url, headers=headers) as response: # асинхронный доступ на ресурс под пользователем анонимайзера
                r = await aiohttp.StreamReader.read(response.content) # чтение html кода (await для ассинхронности)
                soup = BS(r, 'html.parser') # читаем код парсером

                items = soup.find_all('article', {'class': 'product-item product-card'}) # читаем все нужные нам объекты на странице
                for item in items: # для каждого нужного нам объекта...
                    name = item.find('a', {'class': 'product-card__title'}) # ищем имя
                    price = item.find('b').text.strip() # ищем цену
                    link = name.get('href') # ищем ссылку
                    #
                    print(f'Название продукта: {name.text.strip()}\n' # вывод
                          f'Цена: {price}\n'
                          f'Ссылка на продукт: http://{link}\n')



if __name__ == '__main__': # основная программа
    loop = asyncio.get_event_loop() # запускаем программу ассинхронно
    loop.run_until_complete(main()) # запускаем функцию main()