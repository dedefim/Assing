"""
Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

"""

worlds = ['разработка', 'администрирование', 'protocol', 'standard']
list_2 = []
list_3 = []

for i in worlds:
    list_2.append(i.encode('utf-8'))
for i in list_2:
    list_3.append(i.decode('utf-8'))

print(list_2)
print(list_3)
