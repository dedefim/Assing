"""Программа-сервер"""

import socket
import sys
import json
from common.variables import act, name_accaunte, present, MAX_CONNECTIONS, \
    PRESENCE, TIME, users, ERROR, port_defail
from common.utils import get_message, send_message


def proc_client(message):
    if act in message and message[act] == present and TIME in message \
            and users in message and message[users][name_accaunte] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    try:
        if '-p' in sys.argv:
            port_liste = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            port_liste = port_defail
        if port_liste < 1024 or port_liste > 65535:
            raise ValueError
    except IndexError:
        print('После -\'p\' укажите порт.')
        sys.exit(1)
    except ValueError:
        print(
            'Порт- это  число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        print(
            'После \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, port_liste))

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_cient = get_message(client)
            print(message_from_cient)
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = proc_client(message_from_cient)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
