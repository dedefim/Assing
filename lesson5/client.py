import sys
import json
import socket
import time
import argparse
import logging
import logs.config_client_log
from errors import ReqFieldMissingError
from common.variables import action, presence, TIME, users, name_account, \
    response, port_defal, error, defal_ip, message, text_mes, sender
from common.utils import get_message, send_message
from errors import ReqFieldMissingError, ServerError
from decos import log



logger_cliente = logging.getLogger('client')

@log
def message_from_server(message):
    if action in message and message[action] == message and \
            sender in message and text_mes in message:
        print(f'Получено сообщение от пользователя '
              f'{message[sender]}:\n{message[text_mes]}')
        logger_cliente.info(f'Получено сообщение от пользователя '
                    f'{message[sender]}:\n{message[text_mes]}')
    else:
        logger_cliente.error(f'Получено некорректное сообщение с сервера: {message}')


@log
def create_message(sock, account_name='Guest'):
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        logger_cliente.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        action: message,
        TIME: time.time(),
        account_name: account_name,
        text_mes: message
    }
    logger_cliente.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict




@log
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


@log
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


@log
def arg_parser():
    parsering = argparse.ArgumentParser()
    parsering.add_argument('addr', default=defal_ip, nargs='?')
    parsering.add_argument('port', default=defal_ip, type=int, nargs='?')
    parsering.add_argument('-m', '--mode', default='listen', nargs='?')
    space_name = parsering.parse_args(sys.argv[1:])
    address_ser = space_name.addr
    port_ser = space_name.port
    mode_client = space_name.mode

    if not 1023 < port_ser < 65536:
        logger_cliente.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {port_ser}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    if mode_client not in ('listen', 'send'):
        logger_cliente.critical(f'Указан недопустимый режим работы {mode_client}, '
                        f'допустимые режимы: listen , send')
        sys.exit(1)

    return address_ser, port_ser, mode_client


def main():
    server_address, server_port, client_mode = arg_parser()

    logger_cliente.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
        f'порт: {server_port}, режим работы: {client_mode}')


    try:
        transp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transp.connect((server_address, server_port))
        send_message(transp, create_presence())
        answer = process_ans(get_message(transp))
        logger_cliente.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        logger_cliente.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        logger_cliente.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        logger_cliente.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        logger_cliente.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:

            if client_mode == 'send':
                try:
                    send_message(transp, create_message(transp))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    logger_cliente.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transp))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    logger_cliente.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)

if __name__ == '__main__':
    main()
