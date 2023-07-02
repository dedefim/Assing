"""
Задание на закрепление знаний по модулю yaml.
Написать скрипт, автоматизирующий сохранение данных
в файле YAML-формата.
"""

import yaml

dict_date = {'items': ['computer', 'printer', 'keyboard', 'mouse'],
           'items_quantity': 4,
           'items_ptice': {'computer': '200€-1000€',
                           'printer': '100€-300€',
                           'keyboard': '5€-50€',
                           'mouse': '4€-7€'}
           }

f = open('file_1.yaml', 'w', encoding='utf-8')
yaml.dump(dict_date, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

f = open('file_1.yaml', 'r', encoding='utf-8')
out = yaml.load(f, Loader=yaml.SafeLoader)

print(dict_date == out)