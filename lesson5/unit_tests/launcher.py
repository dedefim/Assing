import subprocess

proc = []

while True:
    act = input('Выберите действие: qwaiet - выход, '
                   'server - запустить сервер и клиенты, close - закрыть все окна: ')

    if act == 'qwaiet':
        break
    elif act == 'server':
        proc.append(subprocess.Popen('python server.py',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(2):
            proc.append(subprocess.Popen('python client.py -m send',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(5):
            proc.append(subprocess.Popen('python client.py -m listen',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif act == 'close':
        while proc:
            vict = proc.pop()
            vict.kill()
