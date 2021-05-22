# coding: utf-8

import pandas as pd
from DataFileElf import DataFileElf
import os
from moment import moment
from config import config


class CVSFileElf(DataFileElf):

    def __init__(self):
        super().__init__()

    def set_config(self):
        self._config = config({
            'name': 'CVSFileElf',
            'default': {
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
            },
            'schema': {
                'type': 'object',
                'properties': {
                    'add': {
                        "type": "object",
                        "properties": {
                            'base': {
                                "type": "object",
                                "properties": {
                                    'name': { "type": "string" },
                                    'key': { "type": "string" }
                                }
                            },
                            'output': { "type": "string" },
                            'tags': {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        'name': { "type": "string" },
                                        'key': { "type": "string" },
                                        'fields': {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                        'field': { "type": "string" },
                                                        'default': { "type": "string" }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'merge': {
                        'type': 'object'
                    },
                    'match': {
                        'type': 'object'
                    },
                    'filter': {
                        'type': 'object'
                    }
                }
            }
        })

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
        filename = self.get_filename_with_path(cvs_filename)
        with open(filename) as f:
            headers = f.readline().split(',')
        data_type = {}
        for header in headers:
            data_type[header] = str
        content = pd.read_csv(filename, dtype=data_type)
        return content

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
