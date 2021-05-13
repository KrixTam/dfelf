# coding: utf-8

import pandas as pd
from DataFileElf import DataFileElf


class CVSFileElf(DataFileElf):

    def __init__(self, cfg_filename=None):
        super().__init__(cfg_filename)

    def dropDuplicates(self, df, subset):
        # TODO
        mask = df.duplicated(subset=subset)

    def readContent(self, cvs_filename=None):
        # TODO
        headers = None
        with open(filename) as f:
            headers = f.readline().split(',')


    def add(self, *args):
        # TODO
        pass

    def merge(self, *args):
        # TODO
        pass

    def match(self, *args):
        # TODO
        pass