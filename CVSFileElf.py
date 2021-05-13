# coding: utf-8

import pandas as pd
from DataFileElf import DataFileElf


class CVSFileElf(DataFileElf):

    def __init__(self, cfg_filename=None):
        super().__init__(cfg_filename)

    def drop_duplicates(self, df, subset):
        # TODO
        mask = df.duplicated(subset=subset)

    def read_content(self, cvs_filename=None):
        # TODO
        headers = None
        filename = self.get_filename(cvs_filename)
        with open(filename) as f:
            headers = f.readline().split(',')
        data_type = {}
        for header in headers:
            data_type[header] = str
        content = pd.read_csv(filename, dtype=data_type)
        return content

    def generate_config_file(self, cfg_filename='dfelf.cfg', *args):
        # TODO
        pass

    def add(self, *args):
        # TODO
        pass

    def merge(self, *args):
        # TODO
        pass

    def match(self, *args):
        # TODO
        pass

    def filter(self, *args):
        # TODO
        pass
