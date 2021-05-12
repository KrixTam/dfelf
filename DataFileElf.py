# coding: utf-8

import os
import yaml
import logging
import hashlib


class DataFileElf(object):

    def __init__(self, cfg_filename=None):
        super().__init__()
        self._config = None
        self._cwd = os.getcwd()
        if cfg_filename is None:
            pass
        else:
            self.getConfig(cfg_filename)

    def getConfig(self, filename):
        obj_json = None
        if (filename is not None) and (os.path.exists(filename)):
            with open(filename, 'r') as f:
                obj_json = yaml.safe_load(f)
                logging.info('Succeeded reading file "' + filename + '".')
        else:
            logging.warning(str(filename) + ' is not found.')
        self._config = obj_json

    def checksum(self, filename):
        # https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
        # Note: hash_md5.hexdigest() will return the hex string representation for the digest, if you just need the packed bytes use return hash_md5.digest(), so you don't have to convert back.
        hash_md5 = hashlib.md5()
        input_filename = os.path.join(self._cwd, filename)
        with open(input_filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
