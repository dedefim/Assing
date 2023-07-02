"""
Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.
"""

import re
import csv

"Функция извлекает данные из 3 текстовых данных и извлекает информацию в формате ('Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы')"
def get_data():
    prod_list = []
    name_list = []
    code_list = []
    type_list = []
    main_data = []

    for i in range(1, 4):
        file_o = open(f'info_{i}.txt', 'r')
        data = file_o.read()

        prod_reg = re.compile(r'Изготовитель системы:\s*\S*')
        prod_list.append(prod_reg.findall(data)[0].split()[2])

        name = re.compile(r'Windows\s\S*')
        name_list.append(name.findall(data)[0])

        code = re.compile(r'Код продукта:\s*\S*')
        code_list.append(code.findall(data)[0].split()[2])

        type_os = re.compile(r'Тип системы:\s*\S*')
        type_list.append(type_os.findall(data)[0].split()[2])

    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data.append(headers)

    j = 1
    for i in range(0, 3):
        row_data = []
        row_data.append(j)
        row_data.append(prod_list[i])
        row_data.append(name_list[i])
        row_data.append(code_list[i])
        row_data.append(type_list[i])
        main_data.append(row_data)
        j += 1
    return main_data


def write_to_csv(out_file):
    """Записывает полученные данные в формате csv"""

    data_m = get_data()
    with open(out_file, 'w', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        for i in data_m:
            writer.writerow(i)

get_data()
write_to_csv('data_report.csv')
