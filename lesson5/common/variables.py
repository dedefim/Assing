
import logging

# Порт поумолчанию для сетевого ваимодействия
port_defal = 7000
# IP адрес по умолчанию для подключения клиента
defal_ip = '127.0.0.1'
# Максимальная очередь подключений
connect_max = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'
# Текущий уровень логирования
LOGGING_LEVEL = logging.DEBUG

# Прококол JIM основные ключи:
action = 'action'
TIME = 'time'
users = 'user'
name_account = 'account_name'
sender = 'from'
destional = 'to'
# Прочие ключи, используемые в протоколе
presence = 'presence'
response = 'response'
error = 'error'
message = 'message'
text_mes = 'mess_text'
exit = 'exit'

# Словари - ответы:
# 200
response_200 = {response: 200}
# 400
RESPONSE_400 = {
    response: 400,
    error: None
}