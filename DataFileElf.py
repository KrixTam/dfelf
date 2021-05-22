# coding: utf-8

import os
import hashlib
from abc import ABCMeta, abstractmethod


class DataFileElf(metaclass=ABCMeta):

    def __init__(self):
        self._config = None
        self.set_config()
        self._cwd = os.getcwd()
        self._log_path = self.get_filename_with_path('log')
        self.make_log_dir()

    def make_log_dir(self):
        if not os.path.exists(self._log_path):
            os.makedirs(self._log_path)

    def get_filename_with_path(self, filename):
        return os.path.join(self._cwd, filename)

    @abstractmethod
    def set_config(self):
        pass

    def generate_config_file(self, config_filename=None, **kwargs):
        for key, value in kwargs.items():
            if key in self._config:
                self._config[key] = value
        self._config.dump(config_filename)

    def load_config(self, config_filename):
        self._config.load_config(config_filename)

    def get_config(self):
        return self._config

    def checksum(self, filename):
        hash_md5 = hashlib.md5()
        input_filename = self.get_filename_with_path(filename)
        with open(input_filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
