# coding: utf-8

import pandas as pd
from DataFileElf import DataFileElf


class CVSFileElf(DataFileElf):

    def __init__(self, cfg_filename=None):
        super().__init__(cfg_filename)

    def dropDuplicates(self, df, subset):
        mask = df.duplicated(subset=subset)

