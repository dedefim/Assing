

import socket
import sys
import argparse
import json
import logging
import select
import time
import logs.config_server_log
from errors import IncorrectDataRecivedError
from common.variables import action, presence, TIME, users, name_account, \
    response, port_defal, connect_max, error, text_mes, message, sender, RESPONSE_400, \
    destional, response_200, exit
from common.utils import get_message, send_message
from decos import log

logger_server = logging.getLogger('server')

@log
def process_client_message(message, messages_list, client, clients, names):
    logger_server.debug(f'Разбор сообщения от клиента : {message}')

    if action in message and message[action] == presence and \
            TIME in message and users in message:

        if message[users][name_account] not in names.keys():
            names[message[users][name_account]] = client
            send_message(client, response_200)
        else:
            response = RESPONSE_400
            response[error] = 'Имя пользователя уже занято.'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    elif action in message and message[action] == message and \
            destional in message and TIME in message \
            and sender in message and text_mes in message:
        messages_list.append(message)
        return

    elif action in message and message[action] == exit and name_account in message:
        clients.remove(names[message[name_account]])
        names[message[name_account]].close()
        del names[message[name_account]]
        return

    else:
        response = RESPONSE_400
        response[error] = 'Запрос некорректен.'
        send_message(client, response)
        return


@log
def process_message(message, names, listen_socks):
    if message[destional] in names and names[message[destional]] in listen_socks:
        send_message(names[message[destional]], message)
        logger_server.info(f'Отправлено сообщение пользователю {message[destional]} '
                    f'от пользователя {message[sender]}.')
    elif message[destional] in names and names[message[destional]] not in listen_socks:
        raise ConnectionError
    else:
        logger_server.error(
            f'Пользователь {message[destional]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


@log
def arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=port_defal, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        logger_server.critical(
            f'Попытка запуска сервера с указанием неподходящего порта {listen_port}. '
            f'Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


def main():
    listen_address, listen_port = arg_parser()

    logger_server.info(
        f'Запущен сервер, порт для подключений: {listen_port}, '
        f'адрес с которого принимаются подключения: {listen_address}. '
        f'Если адрес не указан, принимаются соединения с любых адресов.')
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    clients = []
    messages = []

    names = dict()

    transport.listen(connect_max)
    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            logger_server.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass


        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message, clients, names)
                except Exception:
                    logger_server.info(f'Клиент {client_with_message.getpeername()} '
                                f'отключился от сервера.')
                    clients.remove(client_with_message)

        for i in messages:
            try:
                process_message(i, names, send_data_lst)
            except Exception:
                logger_server.info(f'Связь с клиентом с именем {i[destional]} была потеряна')
                clients.remove(names[i[destional]])
                del names[i[destional]]
        messages.clear()


if __name__ == '__main__':
    main()