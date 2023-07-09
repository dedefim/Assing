from ipaddress import ip_address
from subprocess import Popen, PIPE

def hostPing(ip_address, timeout=500, requests=1):
    resul = {'Свободные узлы': "", 'Занятые узлы': ""}
    for address in ip_address:
        try:
            address = ip_address(address)
        except ValueError:
            pass
        proc = Popen(f"ping {address} -w {timeout} -n {requests}", shell=False, stdout=PIPE)
        proc.wait()
        if proc.returncode == 0:
            resul['Доступные узлы'] += f"{str(address)}\n"
            res_string = f'{address} - Узел доступен'
        else:
            resul['Недоступные узлы'] += f"{str(address)}\n"
            res_string = f'{address} - Узел недоступен'
        print(res_string)
    return resul


if __name__ == '__main__':
    ip_addresses = ['yandex.ru', '2.2.2.2', '192.168.0.100', '192.168.0.101']
    hostPing(ip_addresses)
