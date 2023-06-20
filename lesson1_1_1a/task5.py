"""
Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.
"""

import subprocess
import chardet

list_1 = ['ping', 'yandex.ru']
list_2 = ['ping', 'youtube.com']
"""
ping_ya = subprocess.Popen(list_1, stdout=subprocess.PIPE)
for line in ping_ya.stdout:
    result = chardet.detect(line)
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))
    print(result)
"""
ping_yot = subprocess.Popen(list_2, stdout=subprocess.PIPE)
for line in ping_yot.stdout:
    result = chardet.detect(line)
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))
    print(result)