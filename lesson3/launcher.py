import subprocess

name = []

while True:
    answe = input('Команды: qwiert - выход, '
                   'start - запустить сервер и клиенты, close - закрыть все окна: ')

    if answe == 'qwiert':
        break
    elif answe == 'start':
        name.append(subprocess.Popen('python server.py',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(5):
            name.append(subprocess.Popen('python client.py',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif answe == 'close':
        while name:
            process = name.pop()
            process.kill()
