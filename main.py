import requests
from bs4 import BeautifulSoup as bs4


urll = 'https://ezov.mzv.sk/e-zov/calendarDay.do?day={}&timeSlotId=&calendarId=&consularPostId=601'





cookies = {
    'JSESSIONID': '8F38BBF968406F872C9027A1E7B12FAA',
    'cookiesession1': '678A3E2809E9B4A42B1D2B0A2D2D520F',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',

    'Referer': 'https://ezov.mzv.sk/e-zov/consularPost.do',
    'DNT': '1',
    'Connection': 'keep-alive',

    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
}



q = 1
while True:
    '''
    бесконечный цикл, который проверяет
    наличие мест в очереди на получение визы
    '''
    params = {
        'month': q,
        'consularPost': '601',
    } # полезная нагрузка для запроса

    response = requests.get('https://ezov.mzv.sk/e-zov/calendar.do', params=params, cookies=cookies, headers=headers)

    soup = bs4(response.text, 'html.parser')

    innovar = soup.find('div', attrs={'id': 'infoBarBigInnerDiv'})
    cTable = innovar.find('table', attrs={'class': 'calendarMonthTable'})
    Data = cTable.find('td', attrs={'class': 'calendarMonthLabel'})
    month, year = Data.text.strip().split('/')[0], Data.text.strip().split('/')[1].split('-')[0].replace(' ', '')

    vals = cTable.find_all('td', attrs={'class': 'calendarMonthCell'})
    for i in vals:

        res = i.text.strip() if i.text != "" else ""

        if res != "":
            if len(res.split('.')) >= 3:
                day = res.split('.')[0].strip()

                w = res.split('.')[2].strip()


                if any(u in w for u in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']) == 1:

                    if any(u in w for u in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']) == 1:
                        r = f"{str(day)}.{str(month)}.{str(year)}"
                        print(f"{day}/{month}/{year} {w}\n{urll.format(r)}")
                        

    if year > '2022':
        q = - 1
    if month == '12' and year == '2022':
        q = -1
    if month <= '08' and year <= '2022':
        q = 1
    






