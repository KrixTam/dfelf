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
                        'key': 'key_field',
                        'drop_duplicates': False,
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
                'exclude': {
                    'input': 'input_filename',
                    'exclusion': [
                        {
                            'key': 'field',
                            'op': '=',
                            'value': 123
                        }
                    ],
                    'output': {
                        'name': 'output_filename',
                        'BOM': False,
                        'non-numeric': []
                    }
                },
                'filter': {
                    'input': 'input_filename',
                    'filters': [
                        {
                            'key': 'field',
                            'op': '=',
                            'value': 123
                        }
                    ],
                    'output': {
                        'name': 'output_filename',
                        'BOM': False,
                        'non-numeric': []
                    }
                },
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
                                    'key': {"type": "string"},
                                    'drop_duplicates': {"type": "boolean"}
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
                        'type': 'object',
                        "properties": {
                            'input': {"type": "string"},
                            'exclusion': {
                                "type": "array",
                                "items": {
                                    'type': 'object',
                                    "properties": {
                                        'key': {"type": "string"},
                                        'op': {
                                            "type": "string",
                                            "enum": ['=', '!=', '>', '>=', '<=', '<']
                                        },
                                        'value': {"type": ["number", "string"]}
                                    }
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
                            }
                        }
                    },
                    'filter': {
                        'type': 'object',
                        "properties": {
                            'input': {"type": "string"},
                            'filters': {
                                "type": "array",
                                "items": {
                                    'type': 'object',
                                    "properties": {
                                        'key': {"type": "string"},
                                        'op': {
                                            "type": "string",
                                            "enum": ['=', '!=', '>', '>=', '<=', '<']
                                        },
                                        'value': {"type": ["number", "string"]}
                                    }
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
                            }
                        }
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
        CSVFileElf.to_csv_with_bom(duplicates, filename)
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
    def to_csv(df, output_filename, bom, non_numeric=None):
        nn = non_numeric if non_numeric else []
        if bom:
            CSVFileElf.to_csv_with_bom(df, output_filename, nn)
        else:
            CSVFileElf.to_csv_without_bom(df, output_filename, nn)

    @staticmethod
    def to_csv_without_bom(df, output_filename, non_numeric=None):
        nn = non_numeric if non_numeric else []
        df_export = CSVFileElf.tidy(df, nn)
        df_export.to_csv(output_filename, index=False)

    @staticmethod
    def to_csv_with_bom(df, output_filename, non_numeric=None):
        nn = non_numeric if non_numeric else []
        df_export = CSVFileElf.tidy(df, nn)
        df_export.to_csv(output_filename, index=False, encoding='utf-8-sig')

    def read_content(self, cvs_filename=None):
        filename = self.get_filename_with_path(cvs_filename)
        content = pd.read_csv(filename, dtype=str)
        return content

    def to_output_file(self, df, key):
        output_filename = self.get_output_path(self._config[key]['output']['name'])
        bom = self._config[key]['output']['BOM']
        nn = self._config[key]['output']['non-numeric']
        CSVFileElf.to_csv(df, output_filename, bom, nn)

    def add(self, **kwargs):
        new_kwargs = {
            'add': kwargs
        }
        self.set_config(**new_kwargs)
        df_ori = self.read_content(self._config['add']['base']['name'])
        key_ori = self._config['add']['base']['key']
        if self._config['add']['base']['drop_duplicates']:
            df_ori = self.drop_duplicates(df_ori, key_ori)[0]
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
        self.to_output_file(df_ori, 'add')

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
        input_filename = self._config['exclude']['input']
        df_ori = self.read_content(input_filename)
        exclusion = self._config['exclude']['exclusion']
        for e in exclusion:
            key = e['key']
            op = e['op']
            value = e['value']
            if isinstance(value, str):
                if '=' == op:
                    df_ori = df_ori.loc[df_ori[key] != value]
                    continue
                if '!=' == op:
                    df_ori = df_ori.loc[df_ori[key] == value]
                    continue
                if '>' == op:
                    df_ori = df_ori.loc[df_ori[key] <= value]
                    continue
                if '>=' == op:
                    df_ori = df_ori.loc[df_ori[key] < value]
                    continue
                if '<' == op:
                    df_ori = df_ori.loc[df_ori[key] >= value]
                    continue
                if '<=' == op:
                    df_ori = df_ori.loc[df_ori[key] > value]
                    continue
            else:
                key_tmp = key + '_tmp'
                df_ori[key_tmp] = df_ori[key].apply(lambda x: float(x))
                if '=' == op:
                    df_ori = df_ori.loc[df_ori[key_tmp] != value].drop(columns=[key_tmp])
                    continue
                if '!=' == op:
                    df_ori = df_ori.loc[df_ori[key_tmp] == value].drop(columns=[key_tmp])
                    continue
                if '>' == op:
                    df_ori = df_ori.loc[df_ori[key_tmp] <= value].drop(columns=[key_tmp])
                    continue
                if '>=' == op:
                    df_ori = df_ori.loc[df_ori[key_tmp] < value].drop(columns=[key_tmp])
                    continue
                if '<' == op:
                    df_ori = df_ori.loc[df_ori[key_tmp] >= value].drop(columns=[key_tmp])
                    continue
                if '<=' == op:
                    df_ori = df_ori.loc[df_ori[key_tmp] > value].drop(columns=[key_tmp])
                    continue
        self.to_output_file(df_ori, 'exclude')

    def filter(self, **kwargs):
        new_kwargs = {
            'filter': kwargs
        }
        self.set_config(**new_kwargs)
        input_filename = self._config['filter']['input']
        df_ori = self.read_content(input_filename)
        filters = self._config['filter']['filters']
        for f in filters:
            key = f['key']
            op = f['op']
            value = f['value']
            if isinstance(value, str):
                if '=' == op:
                    df_ori = df_ori.loc[df_ori[key] == value]
                    continue
                if '!=' == op:
                    df_ori = df_ori.loc[df_ori[key] != value]
                    continue
                if '>' == op:
                    df_ori = df_ori.loc[df_ori[key] > value]
                    continue
                if '>=' == op:
                    df_ori = df_ori.loc[df_ori[key] >= value]
                    continue
                if '<' == op:
                    df_ori = df_ori.loc[df_ori[key] < value]
                    continue
                if '<=' == op:
                    df_ori = df_ori.loc[df_ori[key] <= value]
                    continue
            else:
                key_tmp = key + '_tmp'
                df_ori[key_tmp] = df_ori[key].apply(lambda x: float(x))
                if '=' == op:
                    df_ori = df_ori.loc[df_ori[key_tmp] == value].drop(columns=[key_tmp])
                    continue
                if '!=' == op:
                    df_ori = df_ori.loc[df_ori[key_tmp] != value].drop(columns=[key_tmp])
                    continue
                if '>' == op:
                    df_ori = df_ori.loc[df_ori[key_tmp] > value].drop(columns=[key_tmp])
                    continue
                if '>=' == op:
                    df_ori = df_ori.loc[df_ori[key_tmp] >= value].drop(columns=[key_tmp])
                    continue
                if '<' == op:
                    df_ori = df_ori.loc[df_ori[key_tmp] < value].drop(columns=[key_tmp])
                    continue
                if '<=' == op:
                    df_ori = df_ori.loc[df_ori[key_tmp] <= value].drop(columns=[key_tmp])
                    continue
        self.to_output_file(df_ori, 'filter')

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
