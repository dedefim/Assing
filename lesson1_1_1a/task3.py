"""
Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b''.
"""


worlds = ['attribute', 'класс', 'функция', 'type']

# Вариант 1
for i in worlds:
    try:
        print(bytes(i, 'ascii'))
    except UnicodeEncodeError:
        print(f'Слово "{i}" невозможно записать в виде байтовой строки')
