from selenium import webdriver  # портрирование вэбдрайвера селениум
import time  # портирование библиотеки для работы со временем
import csv


def headers_csv_writer():
    with open('baltik.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['brand',
                        'h1',
                        'ссылка',
                        'adr3',
                        'adr4',
                        'adr5',
                        'kolvo',
                        'cash1',
                        'cash2',
                        'Keel',
                        'Könes',
                        'Kirjas',
                        'email'
                        ])


def data_csv_writer(data):
    with open('baltik.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([data['brand'],
                         data['h1'],
                         data['ссылка'],
                         data['adr3'],
                         data['adr4'],
                         data['adr5'],
                         data['kolvo'],
                         data['cash1'],
                         data['cash2'],
                         data['Keel'],
                         data['Könes'],
                         data['Kirjas'],
                         data['email'],
                         ])


def get_html(driver, driver_2, url):  # рабочая функция

    try:  # блок запуска браузера
        driver.get(url)  # запуск браузера
        time.sleep(2)  # остановка процесса

        for i in range(2):  # цикл прокликивания всех страниц
            pagination = driver.find_element_by_xpath('/html/body/app-root/div/tk-shell/main/tk-search-page/main/div/div/tk-load-more/div/span')  # выбор кнопки пагинации
            driver.execute_script("arguments[0].click();", pagination)  # клик по элементу pagination с помощью JS
            time.sleep(2)  # остановка процесса

        elements = driver.find_elements_by_xpath('/html/body/app-root/div/tk-shell/main/tk-search-page/main/div/div/tk-joboffer-list-block/div/div[1]/div[1]/h2/a')  # поиск всех элементов, помещение их в список(ссылки)

        for item in elements:  # проход по элементам списка
            try:
                link = item.get_attribute('href')
                driver_2.get(link)
                time.sleep(2)  # остановка процесса
            except:  # блок обработки ошибок
                link = ''

            try:
                brand = driver_2.find_element_by_xpath('/html/body/app-root/div/tk-joboffer-details-page/div/div[3]/div[2]/div[1]/div[2]/div[1]/h2').text  # получение ссылки на продукт
            except:
                brand = ''

            try:
                h1 = driver_2.find_element_by_xpath('/html/body/app-root/div/tk-joboffer-details-page/div/div[3]/div[2]/div[1]/div[1]/h1').text  # получение заголовкка
            except:
                h1 = ''

            try:
                all_adr = driver_2.find_element_by_xpath('/html/body/app-root/div/tk-joboffer-details-page/div/div[3]/div[2]/div[1]/div[6]/ul/li[1]/div/p').text.split(',')
                adr3 = all_adr[0]
            except:
                adr3 = ''

            try:
                adr4 = all_adr[1]
            except:
                adr4 = ''

            try:
                adr5 = all_adr[2] + all_adr[3]
            except:
                adr5 = ''

            try:
                kolvo = driver_2.find_element_by_xpath('/html/body/app-root/div/tk-joboffer-details-page/div/div[3]/div[2]/div[1]/div[6]/ul/li[2]/span[2]').text
            except:
                kolvo = ''

            try:
                cash_all = driver_2.find_element_by_xpath('/html/body/app-root/div/tk-joboffer-details-page/div/div[3]/div[2]/div[1]/div[6]/ul/li[3]/span[2]').text.split(' ')
                cash1 = cash_all[0]
            except:
                cash1 = ''

            try:
                if len(cash_all) > 3:
                    cash2 = cash_all[2]
                else:
                    cash2 = ''
            except:
                cash2 = ''

            try:
                data_all = driver_2.find_element_by_xpath('/html/body/app-root/div/tk-joboffer-details-page/div/div[3]/div[2]/div[1]/div[7]/ul/li[3]/span[2]').text.split(',')
                Keel = data_all[0]
            except:
                Keel = ' '

            try:
                Könes = data_all[1]
            except:
                Könes = ' '

            try:
                Kirjas = data_all[-2]
            except:
                Kirjas = ' '

            try:
                email = data_all[-1]
            except:
                email = ' '


            data = {
                'brand': brand,
                'h1': h1,
                'ссылка': link,
                'adr3': adr3,
                'adr4': adr4,
                'adr5': adr5,
                'kolvo': kolvo,
                'cash1': cash1,
                'cash2': cash2,
                'Keel': Keel,
                'Könes': Könes,
                'Kirjas': Kirjas,
                'email': email
            }
            print(data)

            data_csv_writer(data)

        time.sleep(2)  # остановка процесса


    except Exception as error:  # блок обработки ошибок
        print(error)  # вывод ошибки
    finally:  # финальный блок
        driver_2.close()  # закрытие браузера
        driver_2.quit()  # контрольное закрытие процессов браузера
        driver.close()  # закрытие браузера
        driver.quit()  # контрольное закрытие процессов браузера


def main():  # управляющая функция

    # headers_csv_writer()

    user_agent = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'  # создание юзер агента
    servis = 'D:\\Selenium_priject\\assets\\chromedriver101.0.4951.41.exe'  # создание пути для подключения драйвера актуальной версии
    url = 'https://www.tootukassa.ee/et/toopakkumised?haridustaseMin=&haridustaseMaks=DOKTORIOPE&kinnitamiseVanusPaeviMaks=7&varasemTookogemusAastaidMaks=10'  # url для рабочего запросса
    #url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'  # url для проверки драйвера

    options = webdriver.ChromeOptions()  # создание переменной для работы с опциями
    options.add_argument(user_agent)  # добавление опции, юзер агент
    options.add_argument('--disable-blink-features=AutomationControlled')  # добавление опции, отключение режима работы вэббраузера под вэбдрайвером
    options.add_argument('--headless')  # добавление опции, работа браузера в фонновом режиме
    driver = webdriver.Chrome(executable_path=servis, options=options)  # создания вэббраузера с параметрами
    driver_2 = (webdriver.Chrome(executable_path=servis, options=options))
    get_html(driver, driver_2,  url)  # запуск рабочий функции


if __name__ == '__main__':  # управляющая конструкция
    main()