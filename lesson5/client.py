import sys
import json
import socket
import time
import argparse
import logging
import logs.config_client_log
from errors import ReqFieldMissingError
from common.variables import action, presence, TIME, users, name_account, \
    response, port_defal, error, defal_ip
from common.utils import get_message, send_message



logger_cliente = logging.getLogger('client')


def create_presence(account_name='Guest'):
    out = {
        action: presence,
        TIME: time.time(),
        users: {
            name_account: account_name
        }
    }
    logger_cliente.debug(f'Сформировано {presence} сообщение для пользователя {account_name}')
    return out


def process_ans(message):
    logger_cliente.debug(f'Разбор сообщения от сервера: {message}')
    if response in message:
        if message[response] == 200:
            return '200 : OK'
        return f'400 : {message[error]}'
    raise ReqFieldMissingError(response)


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=defal_ip, nargs='?')
    parser.add_argument('port', default=port_defal, type=int, nargs='?')
    return parser


def main():
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port

    if not 1023 < server_port < 65536:
        logger_cliente.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    logger_cliente.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_address}, порт: {server_port}')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        answer = process_ans(get_message(transport))
        logger_cliente.info(f'Принят ответ от сервера {answer}')
        print(answer)
    except json.JSONDecodeError:
        logger_cliente.error('Не удалось декодировать полученную Json строку.')
    except ReqFieldMissingError as missing_error:
        logger_cliente.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
    except ConnectionRefusedError:
        logger_cliente.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()
