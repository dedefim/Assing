

import socket
import sys
import argparse
import json
import logging
import logs.config_server_log
from errors import IncorrectDataRecivedError
from common.variables import action, presence, TIME, users, name_account, \
    response, port_defal, connect_max, error
from common.utils import get_message, send_message

#Инициализация логирования сервера.
logger_server = logging.getLogger('server')

def process_client_message(message):
    logger_server.debug(f'Разбор сообщения от клиента : {message}')
    if action in message and message[action] == presence and TIME in message and \
            users in message and message[users][name_account] == 'Guest':
        return {response: 200}
    return {
        response: 400,
        error: 'Bad Request'
    }


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=port_defal, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser


def main():
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        logger_server.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    logger_server.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    transport.listen(connect_max)

    while True:
        client, client_address = transport.accept()
        logger_server.info(f'Установлено соедение с ПК {client_address}')
        try:
            message_from_cient = get_message(client)
            logger_server.debug(f'Получено сообщение {message_from_cient}')
            response = process_client_message(message_from_cient)
            logger_server.info(f'Cформирован ответ клиенту {response}')
            send_message(client, response)
            logger_server.debug(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            logger_server.error(f'Не удалось декодировать JSON строку, полученную от '
                                f'клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataRecivedError:
            logger_server.error(f'От клиента {client_address} приняты некорректные данные. '
                                f'Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()
