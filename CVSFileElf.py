# coding: utf-8

import pandas as pd
from DataFileElf import DataFileElf
import os
from moment import moment


class CVSFileElf(DataFileElf):

    def __init__(self, cfg_filename=None):
        super().__init__(cfg_filename)

    def drop_duplicates(self, df, subset):
        mask = pd.Series(df.duplicated(subset=subset))
        self.make_log_dir()
        log_filename = 'drop_duplicates' + moment().format('.YYYYMMDD.HHmmss') + '.log'
        filename = os.path.join(self._log_path, log_filename)
        duplicates = df[mask]
        duplicates.to_csv(filename)
        else_mask = mask.apply(lambda x: True if not x else not x)
        return df[else_mask], log_filename

    def read_content(self, cvs_filename=None):
        headers = []
        filename = self.get_filename(cvs_filename)
        with open(filename) as f:
            headers = f.readline().split(',')
        data_type = {}
        for header in headers:
            data_type[header] = str
        content = pd.read_csv(filename, dtype=data_type)
        return content

    def set_default_config(self):
        self._config = {
            'add': {
                'base': {
                    'name': 'base_filename',
                    'key': 'key_field'
                },
                'output': 'output_filename',
                'tags': [
                    {
                        'name': 'base_filename',
                        'key': 'key_field',
                        'fields': [
                            {'field A': 'default value of field A'},
                            {'field B': 'default value of field B'}
                        ]
                    }
                ]
            },
            'merge': {},
            'match': {},
            'filter': {}
        }

    def add(self, *args):
        # TODO
        base = {
            'name': 'base_filename',
            'key': 'key_field'
        }
        output_filename = ''
        tags = []
        if 3 == len(args):
            base = args[0]
            output_filename = args[1]
            tags = args[2]

    def merge(self, *args):
        # TODO
        pass

    def match(self, *args):
        # TODO
        pass

    def filter(self, *args):
        # TODO
        pass
