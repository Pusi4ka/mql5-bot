import requests
import time
from random import randint
import json
from bs4 import BeautifulSoup
import csv


def main(url):
    statistics_ = '#!tab=stats'
    http = 'https://www.mql5.com/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9 '
    }

    with open(r'data.csv', 'w', encoding='cp1251', newline='') as file:
        data = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
        data.writerow(
            (
                "Всего трейдов",
                "Никнейм",
                "URL",
                "Символы",
                "Брокер",
                "Плечо",
                "Платформа",
                "Алготрейдинг",
                "Просадка по балансу",
                "Прибыльных трейдов",
                "Прирост в месяц",
                "Макс. загрузка депозита",
                "Средства",
                "Недель",
                "Мат. ожидание",
                "Фактор восстановления",
                "Торговая активность",
                "Коэффициент Шарпа",
                "Профит фактор",
                "Трейдов в неделю",
                "Подписчики",
                "Просадка по эквити",
                "Средняя прибыль",
                "Годовой прогноз",
                "Цена за сигнал",

            )
        )

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    pages = int(soup.find_all('div', class_='paginatorEx')[0].find_all('a')[-1].text)

    res = []
    data_s = []
    for pages_ in range(1, pages + 1):

        urls = f'https://www.mql5.com/ru/signals/mt5/page{pages_}'
        time.sleep(randint(1, 5))
        r = requests.get(urls, headers=headers)

        s = BeautifulSoup(r.text, 'lxml')
        a = s.find_all('a', class_='signal-card__wrapper')
        print(f"Обработано страниц | ")

        for item in a:
            time.sleep(randint(1, 5))
            signal_card = item.get('href')

            r_2 = requests.get(http + signal_card + statistics_, headers=headers)
            soup_2 = BeautifulSoup(r_2.text, 'lxml')

            risky = requests.get(http + signal_card + '#!tab=risks', headers=headers)
            soup_3 = BeautifulSoup(risky.text, 'lxml')

            col = soup_2.find('div', class_='s-data-columns__value').text.replace(' ', '')
            name = soup_2.find('span', class_='s-plain-card__title-wrapper').text.strip()
            symbol_ = soup_2.find_all('td', class_='col-symbol')
            broker = soup_2.find(onclick="parentNode.submit ()").text
            plecho = soup_2.find('div', class_='s-plain-card__leverage').text.replace('1:', '')
            platform_ = soup_2.find('span', text='MetaTrader 5').text.replace('eta', '').replace('rader', '').replace(
                ' ', '')
            algotrede = soup_2.find_all('div', class_='s-data-columns__value')[26].text

            risky_ = soup_3.find_all('div', class_='s-data-columns__value')[-2].text.split(' ')[0]
            prirost_x = soup_2.find_all('div', class_='s-data-columns__value')[1].text.split(' ')[1].replace('(',
                                                                                                             '').replace(
                ')', '')
            prirost_v_mes = soup_2.find_all('div', class_='s-data-columns__value')[24].text.strip()
            max_dep = soup_2.find_all('div', class_='s-data-columns__value')[11].text.strip()
            sredstvo = soup_2.find_all('div', class_='s-list-info__value')[2].text.replace(' ', '')
            nedel = soup_2.find_all('div', class_='s-list-info__value')[-2].text

            ojidanie = soup_2.find_all('div', class_='s-data-columns__value')[19].text.replace(' ', '').strip()
            factor = soup_2.find_all('div', class_='s-data-columns__value')[15].text
            activnost = soup_2.find_all('div', class_='s-data-columns__value')[10].text
            coef_sharpa = soup_2.find_all('div', class_='s-data-columns__value')[9].text
            profit = soup_2.find_all('div', class_='s-data-columns__value')[18].text
            treidov_v_nedel = soup_2.find_all('div', class_='s-data-columns__value')[13].text
            subs = soup_2.find_all('div', class_='s-list-info__value')[-3].text
            ecvity = soup_3.find_all('div', class_='s-data-columns__value')[-1].text.split(' ')[0]
            sredniy_prib = soup_2.find_all('div', class_='s-data-columns__value')[20].text.strip().replace(' ', '')
            godovoi_prognoz = soup_2.find_all('div', class_='s-data-columns__value')[25].text.strip().replace(' ', '')
            signal_ = soup_2.find('a', class_='button button_tiny button_green').text.strip().replace('Копировать за',
                                                                                                      '').replace(
                'в месяц', '').replace(' ', '')

            for sy in symbol_:
                data_s.append(sy.text)
            str_ = len(symbol_) / 3
            s = str(str_).replace('.0', '')

            # print("[INFO] Всего трейдов:" + col + "| ник:" + name + 'Ссылка: '
            #       + http + signal_card + statistics_ + "| " + "Брокер: " + broker + '\n' + "Плечо: "
            #       + plecho.strip().replace('1:', '') + ' | Платформа: ' + platform_ + ' | Алготрейдинг: ' + algotrede +
            #       "| Просадка по балансу: " + risky_ + ' | Прибыльных трейдов: ' + prirost_x + ' | Прирост в месяц ' +
            #       prirost_v_mes + ' | Макс. загрузка депозита: ' + max_dep  + "\n | Средства: " + sredstvo + " | " +
            #       'Недель: ' + nedel + ' | Мат. ожидание: ' + ojidanie + ' | Фактор восстановления: ' + factor +
            #       ' | Торговая активность: ' + activnost + ' | Коэффициент Шарпа: ' + coef_sharpa + ' | Профит фактор: ' +
            #       profit + "\n | Трейдов в неделю: " + treidov_v_nedel + ' | Подписчики: ' + subs + ' | Просадка по эквити: ' +
            #       ecvity + ' | Средняя прибыль: ' + sredniy_prib + ' | Годовой прогноз: ' + godovoi_prognoz + ' | Цена за сигнал: ' + signal_)

            res.append(
                {
                    'col': col,
                    'name': name,
                    'url': http + signal_card + statistics_,
                    'symbol': data_s[0:int(s)],
                    'broker': broker,
                    'plecho': plecho.strip(),
                    'platform': platform_,
                    'risky': risky_,
                    'prirost_x': prirost_x,
                    'prirost_v_mes': prirost_v_mes,
                    'sredstrva': sredstvo,
                    'nedel': nedel,
                    'max_dep': max_dep,
                    'ojidanie': ojidanie,
                    'activnost': activnost,
                    'coef_sharpa': coef_sharpa,
                    'profit': factor,
                    'treidov_v_nedely': treidov_v_nedel,
                    'ecvity': ecvity,
                    'sred_prib': sredniy_prib,
                    'godovoi_prognoz': godovoi_prognoz,
                    'signal_': signal_,

                }
            )

            with open(r'data.csv', 'a', newline='', encoding='cp1251') as file:
                data = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')

                data.writerow(
                    [
                        col,
                        name,
                        http + signal_card + statistics_,
                        data_s[0:int(s)],
                        broker,
                        plecho.strip(),
                        platform_,
                        algotrede,
                        risky_,
                        prirost_x,
                        prirost_v_mes,
                        max_dep,
                        sredstvo,
                        nedel,
                        max_dep,
                        ojidanie,
                        activnost,
                        coef_sharpa,
                        profit,
                        factor,
                        treidov_v_nedel,
                        subs,
                        ecvity,
                        sredniy_prib,
                        godovoi_prognoz,
                        signal_
                    ]

                )
    with open('text.json', 'w', encoding='UTF-8') as file:
        json.dump(res, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main('https://www.mql5.com/ru/signals/mt5/page1')
