# coding: utf-8

import pandas as pd
from DataFileElf import DataFileElf
from moment import moment
from config import config


class CSVFileElf(DataFileElf):

    def __init__(self):
        super().__init__()

    def init_config(self):
        self._config = config({
            'name': 'CSVFileElf',
            'default': {
                'add': {
                    'base': {
                        'name': 'base_filename',
                        'key': 'key_field'
                    },
                    'output': {
                        'name': 'output_filename',
                        'BOM': False,
                        'non-numeric': []
                    },
                    'tags': [
                        {
                            'name': 'base_filename',
                            'key': 'key_field',
                            'fields': ['field A', 'field B'],
                            'defaults': ['default value of field A', 'default value of field B']
                        }
                    ]
                },
                'join': {

                },
                'exclude': {},
                'filter': {},
                'split': {
                    'input': 'input_filename',
                    'output': {
                        'prefix': 'output_filename_prefix',
                        'BOM': False,
                        'non-numeric': []
                    },
                    'key': 'key_field'
                }
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
                                    'name': {"type": "string"},
                                    'key': {"type": "string"}
                                }
                            },
                            'output': {
                                "type": "object",
                                "properties": {
                                    'name': {"type": "string"},
                                    'BOM': {"type": "boolean"},
                                    'non-numeric': {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                }
                            },
                            'tags': {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        'name': {"type": "string"},
                                        'key': {"type": "string"},
                                        'fields': {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        },
                                        'defaults': {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'join': {
                        'type': 'object'
                    },
                    'exclude': {
                        'type': 'object'
                    },
                    'filter': {
                        'type': 'object'
                    },
                    'split': {
                        'type': 'object',
                        "properties": {
                            'input': {"type": "string"},
                            'output': {
                                "type": "object",
                                "properties": {
                                    'prefix': {"type": "string"},
                                    'BOM': {"type": "boolean"},
                                    'non-numeric': {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                }
                            },
                            'key': {"type": "string"}
                        }
                    }
                }
            }
        })

    def drop_duplicates(self, df, subset):
        mask = pd.Series(df.duplicated(subset=subset))
        log_filename = 'drop_duplicates' + moment().format('.YYYYMMDD.HHmmss') + '.log'
        filename = self.get_log_path(log_filename)
        duplicates = df[mask]
        duplicates.to_csv(filename)
        # CSVFileElf.to_csv_without_bom(duplicates, filename)
        else_mask = ~ mask
        return df[else_mask], log_filename

    @staticmethod
    def tidy(df, nn):
        df_export = df.copy()
        for field in nn:
            if field in df_export.columns:
                df_export[field] = df_export[field].apply(lambda x: '="' + x + '"')
        return df_export

    @staticmethod
    def to_csv(df, output_filename, bom, nn=[]):
        if bom:
            CSVFileElf.to_csv_with_bom(df, output_filename, nn)
        else:
            CSVFileElf.to_csv_without_bom(df, output_filename, nn)

    @staticmethod
    def to_csv_without_bom(df, output_filename, nn=[]):
        df_export = CSVFileElf.tidy(df, nn)
        df_export.to_csv(output_filename, index=False)

    @staticmethod
    def to_csv_with_bom(df, output_filename, nn=[]):
        df_export = CSVFileElf.tidy(df, nn)
        df_export.to_csv(output_filename, index=False, encoding='utf-8-sig')

    def read_content(self, cvs_filename=None):
        filename = self.get_filename_with_path(cvs_filename)
        content = pd.read_csv(filename, dtype=str)
        return content

    # TODO：增加去重；
    def add(self, **kwargs):
        new_kwargs = {
            'add': kwargs
        }
        self.set_config(**new_kwargs)
        df_ori = self.read_content(self._config['add']['base']['name'])
        key_ori = self._config['add']['base']['key']
        for tag in self._config['add']['tags']:
            df2 = self.read_content(tag['name'])
            key_right = tag['key']
            fields = tag['fields']
            defaults = tag['defaults']
            columns = df2.columns
            for col in columns:
                if col in fields or col == key_right:
                    pass
                else:
                    df2.drop([col], axis=1, inplace=True)
            df_ori = pd.merge(df_ori, df2, how="left", left_on=key_ori, right_on=key_right)
            for x in range(len(fields)):
                df_ori[fields[x]].fillna(defaults[x], inplace=True)
        output_filename = self.get_output_path(self._config['add']['output']['name'])
        bom = self._config['add']['output']['BOM']
        nn = self._config['add']['output']['non-numeric']
        CSVFileElf.to_csv(df_ori, output_filename, bom, nn)

    def join(self, **kwargs):
        new_kwargs = {
            'join': kwargs
        }
        self.set_config(**new_kwargs)

    def exclude(self, **kwargs):
        new_kwargs = {
            'exclude': kwargs
        }
        self.set_config(**new_kwargs)

    def filter(self, **kwargs):
        new_kwargs = {
            'filter': kwargs
        }
        self.set_config(**new_kwargs)

    def split(self, **kwargs):
        new_kwargs = {
            'split': kwargs
        }
        self.set_config(**new_kwargs)
        input_filename = self._config['split']['input']
        df_ori = self.read_content(input_filename)
        key_name = self._config['split']['key']
        columns = df_ori.columns
        output_prefix = ''
        if '' != self._config['split']['output']['prefix']:
            output_prefix = self._config['split']['output']['prefix'] + '_'
        non_numeric = self._config['split']['output']['non-numeric']
        if key_name in columns:
            split_keys = df_ori[key_name].unique()
            if self._config['split']['output']['BOM']:
                for key in split_keys:
                    tmp_df = df_ori.loc[df_ori[key_name] == key]
                    output_filename = self.get_output_path(output_prefix + key + '.csv')
                    # tmp_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
                    CSVFileElf.to_csv_with_bom(tmp_df, output_filename, non_numeric)
            else:
                for key in split_keys:
                    tmp_df = df_ori.loc[df_ori[key_name] == key]
                    output_filename = self.get_output_path(output_prefix + key + '.csv')
                    # tmp_df.to_csv(output_filename, index=False)
                    CSVFileElf.to_csv_without_bom(tmp_df, output_filename, non_numeric)
        else:
            raise KeyError('"split"中的"key"不存在，请检查数据文件"' + input_filename + '"是否存在该字段')

