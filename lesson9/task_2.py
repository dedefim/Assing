from ipaddress import ip_address
from task_1 import hostPing


def host_range_ping():
    while True:
        startIp = input('Введите первоначальный адрес: ')
        try:
            las_oct = int(startIp.split('.')[3])
            break
        except Exception as e:
            print(e)
    while True:
        en_ip = input('Сколько адресов проверить?: ')
        if not en_ip.isnumeric():
            print('Необходимо ввести число: ')
        else:
            if (las_oct+int(en_ip)) > 254:
                print(f"Можем менять только последний октет, т.е. "
                      f"максимальное число хостов для проверки: {254-las_oct}")
            else:
                break
    hostList = []
    # формируем список ip адресов
    [hostList.append(str(ip_address(startIp)+x)) for x in range(int(en_ip))]
    # передаем список в функцию из задания 1 для проверки доступности
    return hostPing(hostList)


if __name__== "__main__":
    host_range_ping()
