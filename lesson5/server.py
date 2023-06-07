

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
    response, port_defal, connect_max, error, text_mes, message, sender
from common.utils import get_message, send_message
from decos import log

#Инициализация логирования сервера.
logger_server = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client):
    logger_server.debug(f'Разбор сообщения от клиента : {message}')
    if action in message and message[action] == presence and TIME in message and \
            users in message and message[users][name_account] == 'Guest':
        return {response: 200}
    elif action in message and message[action] == message and \
            TIME in message and text_mes in message:
        messages_list.append((message[name_account], message[text_mes]))
        return
        # Иначе отдаём Bad request
    else:
        send_message(client, {
            response: 400,
            error: 'Bad Request'
        })
        return

@log
def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=port_defal, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    if not 1023 < listen_port < 65536:
        logger_server.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


def main():
    listen_address, listen_port = create_arg_parser()

    logger_server.info(
        f'Запущен сервер, порт для подключений: {listen_port}, '
        f'адрес с которого принимаются подключения: {listen_address}. '
        f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Готовим сокет
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    clients = []
    messages = []

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
        err_lst = []
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)
                except:
                    logger_server.info(f'Клиент {client_with_message.getpeername()} '
                                f'отключился от сервера.')
                    clients.remove(client_with_message)

        if messages and send_data_lst:
            message = {
                action: messages,
                sender: messages[0][0],
                TIME: time.time(),
                text_mes: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    logger_server.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
