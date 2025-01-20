import logging
from typing import Literal
import sys


class AzDbrBase():
    def __init__(self, name: str, log_level: int = logging.INFO):
        self._log_level = log_level
        self.logger = logging.Logger(name=name)

    def _embed_caller_info(self, msg):
        frame = None
        try:
            frame = sys._getframe(1)
        except Exception as e:
            print(f'Exception: {e}')
            return None
        return f'{frame.f_code.co_filename}:{frame.f_lineno} {msg}'

    def info(self, msg: str):
        _msg = self._embed_caller_info(msg=msg)
        self.logger.info(msg=_msg)

    def debug(self, msg: str):
        _msg = self._embed_caller_info(msg=msg)
        self.logger.debug(msg=_msg)

    def warn(self, msg: str):
        _msg = self._embed_caller_info(msg=msg)
        self.logger.warn(msg=_msg)
    
    def error(self, msg: str):
        _msg = self._embed_caller_info(msg=msg)
        self.logger.error(msg=_msg)