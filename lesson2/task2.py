"""
Задание на закрепление знаний по модулю json. Есть файл orders
в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий
его заполнение данными.
"""

import json


def write_json(item, quantity, price, buyer, date):

    "Чтение файла"
    f = open('orders_1.json', 'r', encoding='utf-8')
    data = json.load(f)
    f.close()

    "Запись в файл"
    f = open('orders_1.json', 'w', encoding='utf-8')
    orders_list = data['orders']
    order_info = {'item': item, 'quantity': quantity,
                  'price': price, 'buyer': buyer, 'date': date}
    orders_list.append(order_info)
    json.dump(data, f, indent=4)
    f.close()


write_json('printer', '10', '6700', 'Ivanov I.I.', '24.09.2017')
write_json('scaner', '20', '10000', 'Petrov P.P.', '11.01.2018')
write_json('computer', '5', '40000', 'Sidorov S.S.', '2.05.2019')
