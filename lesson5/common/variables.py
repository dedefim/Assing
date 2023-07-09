
import logging

# Порт поумолчанию для сетевого ваимодействия
port_defal = 7777
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
database_server = 'sqlite:///server_base.db3'
conf_serv = 'server.ini'

# Прококол JIM основные ключи:
action = 'action'
TIME = 'time'
users = 'user'
name_account = 'account_name'
sender = 'from'
destional = 'to'
public_keys = 'pubkey'
# Прочие ключи, используемые в протоколе
presence = 'presence'
response = 'response'
error = 'error'
message = 'message'
text_mes = 'mess_text'
exit = 'exit'
contacts = 'get_contacts'
info = 'data_list'
contact_remove = 'remove'
contact_add = 'add'
request_user = 'get_users'
pub_key_req = 'pubkey_need'
data = 'bin'
# Словари - ответы:
# 200
response_200 = {response: 200}
respons_202 = {response: 202,
                info:None
                }
# 400
RESPONSE_400 = {
    response: 400,
    error: None
}
responss_205 = {
    response: 205
}
response_511 = {
    response: 511,
    data: None
}