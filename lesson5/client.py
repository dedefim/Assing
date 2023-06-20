import sys
import json
import socket
import time
import dis
import argparse
import logging
import threading
from errors import ReqFieldMissingError, ServerError, IncorrectDataRecivedError
from decos import log
from common.variables import *
from common.utils import *
from metaclasses import ClientMaker
import logs.config_client_log
from errors import ReqFieldMissingError
from common.variables import action, presence, TIME, users, name_account, \
    response, port_defal, error, defal_ip, message, text_mes, sender, destional, exit
from common.utils import get_message, send_message


logger_cliente = logging.getLogger('client')


class ClientSender(threading.Thread, metaclass=ClientMaker):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()
    def create_exit_message(self):
        return {
            action: exit,
            TIME: time.time(),
            name_account: self.account_name
        }
    def create_message(self):
        to = input('Введите получателя сообщения: ')
        message = input('Введите сообщение для отправки: ')
        message_dict = {
            action: message,
            sender: self.account_name,
            destional: to,
            TIME: time.time(),
            text_mes: message
        }
        logger_cliente.debug(f'Сформирован словарь сообщения: {message_dict}')
        try:
            send_message(self.sock, message_dict)
            logger_cliente.info(f'Отправлено сообщение для пользователя {to}')
        except:
            logger_cliente.critical('Потеряно соединение с сервером.')
            exit(1)

    def run(self):
        self.print_help()
        while True:
            command = input('Введите команду: ')
            if command == 'message':
                self.create_message()
            elif command == 'help':
                self.print_help()
            elif command == 'exit':
                try:
                    send_message(self.sock, self.create_exit_message())
                except:
                    pass
                print('Завершение соединения.')
                logger_cliente.info('Завершение работы по команде пользователя.')
                # Задержка неоходима, чтобы успело уйти сообщение о выходе
                time.sleep(0.5)
                break
            else:
                print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')

    def print_help(self):
        print('Поддерживаемые команды:')
        print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
        print('help - вывести подсказки по командам')
        print('exit - выход из программы')

class ClientReader(threading.Thread , metaclass=ClientMaker):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()
    def run(self):
        while True:
            try:
                message = get_message(self.sock)
                if action in message and message[action] == message and sender in message and destional in message \
                        and text_mes in message and message[destional] == self.account_name:
                    print(f'\nПолучено сообщение от пользователя {message[sender]}:\n{message[text_mes]}')
                    logger_cliente.info(f'Получено сообщение от пользователя {message[sender]}:\n{message[text_mes]}')
                else:
                    logger_cliente.error(f'Получено некорректное сообщение с сервера: {message}')
            except IncorrectDataRecivedError:
                logger_cliente.error(f'Не удалось декодировать полученное сообщение.')
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                logger_cliente.critical(f'Потеряно соединение с сервером.')
                break

@log
def create_presence(account_name):
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
def process_response_ans(message):
    logger_cliente.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if response in message:
        if message[response] == 200:
            return '200 : OK'
        elif message[response] == 400:
            raise ServerError(f'400 : {message[error]}')
    raise ReqFieldMissingError(response)

@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=port_defal, nargs='?')
    parser.add_argument('port', default=port_defal, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    if not 1023 < server_port < 65536:
        logger_cliente.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. Допустимы адреса с 1024 до 65535. Клиент завершается.')
        exit(1)

    return server_address, server_port, client_name


def main():
    print('Консольный месседжер. Клиентский модуль.')

    server_address, server_port, client_name = arg_parser()

    if not client_name:
        client_name = input('Введите имя пользователя: ')
    else:
        print(f'Клиентский модуль запущен с именем: {client_name}')

    logger_cliente.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address} , порт: {server_port}, имя пользователя: {client_name}')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence(client_name))
        answer = process_response_ans(get_message(transport))
        logger_cliente.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        logger_cliente.error('Не удалось декодировать полученную Json строку.')
        exit(1)
    except ServerError as error:
        logger_cliente.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        exit(1)
    except ReqFieldMissingError as missing_error:
        logger_cliente.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        exit(1)
    except (ConnectionRefusedError, ConnectionError):
        logger_cliente.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, конечный компьютер отверг запрос на подключение.')
        exit(1)
    else:
        module_reciver = ClientReader(client_name , transport)
        module_reciver.daemon = True
        module_reciver.start()

        module_sender = ClientSender(client_name , transport)
        module_sender.daemon = True
        module_sender.start()
        logger_cliente.debug('Запущены процессы')

        while True:
            time.sleep(1)
            if module_reciver.is_alive() and module_sender.is_alive():
                continue
            break


if __name__ == '__main__':
    main()