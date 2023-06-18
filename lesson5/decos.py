import sys
import logging
import logs.config_server_log
import logs.config_client_log

if sys.argv[0].find('client') == -1:
    Loggers = logging.getLogger('server')
else:
    Loggers = logging.getLogger('client')


def log(func_to_log):
    def log_saver(*args, **kwargs):
        ret = func_to_log(*args, **kwargs)
        Loggers.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func_to_log.__module__}')
        return ret
    return log_saver
