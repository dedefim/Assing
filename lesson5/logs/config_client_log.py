import sys
import os
import logging
from common.variables import LOGGING_LEVEL
sys.path.append('../')

# создаём формировщик логов (formatter):
CLIENT_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

# создаём потоки вывода логов
hsnd_strem = logging.StreamHandler(sys.stderr)
hsnd_strem.setFormatter(CLIENT_FORMATTER)
hsnd_strem.setLevel(logging.ERROR)
file_log = logging.FileHandler(PATH, encoding='utf8')
file_log.setFormatter(CLIENT_FORMATTER)

# создаём регистратор и настраиваем его
loggers = logging.getLogger('client')
loggers.addHandler(hsnd_strem)
loggers.addHandler(file_log)
loggers.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    loggers.critical('Критическая ошибка')
    loggers.error('Ошибка')
    loggers.debug('Отладочная информация')
    loggers.info('Информационное сообщение')
