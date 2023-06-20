import sys
import os
import logging
import logging.handlers
from comm.variables import LOGGING_LEVEL
sys.path.append('../')

# создаём формировщик логов (formatter):
format_server = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')

# создаём потоки вывода логов
handler_stream = logging.StreamHandler(sys.stderr)
handler_stream.setFormatter(format_server)
handler_stream.setLevel(logging.ERROR)
file_log = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
file_log.setFormatter(format_server)

# создаём регистратор и настраиваем его
loggers = logging.getLogger('server')
loggers.addHandler(handler_stream)
loggers.addHandler(file_log)
loggers.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    loggers.critical('Критическая ошибка')
    loggers.error('Ошибка')
    loggers.debug('Отладочная информация')
    loggers.info('Информационное сообщение')
