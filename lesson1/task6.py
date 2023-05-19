"""
Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""

from chardet import detect

with open('test.txt', encoding='utf-8') as file:
    for line in file.read():
        print(line)
#file.close()


file = open('test.txt', 'rb')
for line in file:
    print(line.decode(encoding='utf-8'))