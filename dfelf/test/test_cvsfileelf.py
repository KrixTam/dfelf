import os
import json
import pandas as pd
import unittest
from dfelf import CSVFileElf
import numpy as np
from random import random


cwd = os.path.abspath(os.path.dirname(__file__))


class TestCSVFileElf(unittest.TestCase):

    def test_drop_duplicates_01(self):
        input_filename = os.path.join(cwd, 'sources', 'ori_data.csv')
        log_result = os.path.join(cwd, 'result', 'drop_duplicates.ori.log')
        df_elf = CSVFileElf()
        df = CSVFileElf.read_content(input_filename)
        log_filename = df_elf.drop_duplicates(df, 'brand')[1]
        log_file = os.path.join('log', log_filename)
        self.assertEqual(df_elf.checksum(log_file), df_elf.checksum(log_result))

    def test_drop_duplicates_02(self):
        input_filename = os.path.join(cwd, 'sources', 'ori_data.csv')
        log_result = os.path.join(cwd, 'result', 'drop_duplicates.multi.log')
        df_elf = CSVFileElf()
        df = CSVFileElf.read_content(input_filename)
        log_filename = df_elf.drop_duplicates(df, ['brand', 'style'])[1]
        log_file = os.path.join('log', log_filename)
        self.assertEqual(df_elf.checksum(log_file), df_elf.checksum(log_result))

    def test_drop_duplicates_03(self):
        input_filename = os.path.join(cwd, 'sources', 'ori_data.csv')
        df_elf = CSVFileElf()
        df = CSVFileElf.read_content(input_filename)
        with self.assertRaises(TypeError):
            df_elf.drop_duplicates(df, 123)

    def test_drop_duplicates_04(self):
        fof_list = ['009213', '006297', '006880', '010266', '005215', '005156', '005957', '008145']
        df_elf = CSVFileElf()
        columns = ['日期']
        df_all = pd.DataFrame([], columns=columns)
        for fund_code in fof_list:
            filename = fund_code + '_adj.csv'
            df = CSVFileElf.read_content(os.path.join(cwd, 'sources', 'fof', filename))
            df.sort_values(by='日期', inplace=True)
            df = df[(df['日期'] >= '2022-06-16') & (df['日期'] <= '2022-07-22')]
            df_all = pd.concat([df_all, df[columns]])
        res = df_elf.drop_duplicates(df_all, columns)[0]
        self.assertEqual(res.shape[0], 27)
        self.assertEqual(res.iloc[0]['日期'], '2022-06-16')
        self.assertEqual(res.iloc[-1]['日期'], '2022-07-22')

    def test_add_01(self):
        df_elf = CSVFileElf()
        config = {
            'base': {
                'name': os.path.join(cwd, 'sources', 'df1.csv'),
                'key': 'key'
            },
            'output': {
                'name': 'test_add.csv'
            },
            'tags': [
                {
                    'name': os.path.join(cwd, 'sources', 'df3.csv'),
                    'key': 'key',
                    'fields': ['new_value'],
                    'defaults': ['0.0']
                }
            ]
        }
        df_elf.add(**config)
        result_filename = os.path.join(cwd, 'sources', 'add.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))
        df_elf_01 = CSVFileElf()
        df_elf_01.shutdown_output()
        df_elf_01.add(**config)
        dist_filename_01 = df_elf_01.get_log_path(config['output']['name'])
        self.assertEqual(df_elf_01.checksum(result_filename), df_elf_01.checksum(dist_filename_01))
        config_01 = config.copy()
        config_01['output']['name'] = 'test_add_bom.csv'
        config_01['output']['BOM'] = True
        df_elf.add(**config_01)
        result_filename_01 = os.path.join(cwd, 'result', 'test_add_bom.csv')
        dist_filename_02 = df_elf.get_output_path(config_01['output']['name'])
        self.assertEqual(df_elf.checksum(dist_filename_02), df_elf.checksum(result_filename_01))

    def test_add_02(self):
        df_elf = CSVFileElf()
        config = {
            'base': {
                'name': os.path.join(cwd, 'sources', 'df1.csv'),
                'key': 'key'
            },
            'output': {
                'name': 'test_add_02.csv'
            },
            'tags': [
                {
                    'name': os.path.join(cwd, 'sources', 'df5.csv'),
                    'key': 'new_key',
                    'fields': ['new_value'],
                    'defaults': ['0.0']
                }
            ]
        }
        df_elf.add(**config)
        result_filename = os.path.join(cwd, 'sources', 'add.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_add_03(self):
        df_elf = CSVFileElf(output_flag=False)
        df_elf.activate_output()
        config = {
            'base': {
                'name': os.path.join(cwd, 'sources', 'df1.csv'),
                'key': 'key'
            },
            'output': {
                'name': 'test_add_03.csv'
            },
            'tags': [
                {
                    'name': os.path.join(cwd, 'sources', 'df6.csv'),
                    'key': 'key',
                    'fields': ['new_value'],
                    'defaults': ['0.0']
                }
            ]
        }
        df_elf.add(**config)
        result_filename = os.path.join(cwd, 'sources', 'add.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_add_04(self):
        df_elf = CSVFileElf()
        config = {
            'add': {
                'base': {
                    'name': os.path.join(cwd, 'sources', 'df1.csv'),
                    'key': 'key'
                },
                'output': {
                    'name': 'test_add_04.csv'
                },
                'tags': [
                    {
                        'name': os.path.join(cwd, 'sources', 'df3.csv'),
                        'key': 'key',
                        'fields': ['new_value'],
                        'defaults': ['0.0']
                    }
                ]
            }
        }
        config_file = df_elf.get_output_path('test_config.cfg')
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        df_elf.load_config(config_file)
        df_elf.add()
        result_filename = os.path.join(cwd, 'sources', 'add.csv')
        dist_filename = df_elf.get_output_path(config['add']['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_add_05(self):
        df_elf = CSVFileElf()
        config = {
            'add': {
                'base': {
                    'key': 'key'
                },
                'output': {
                    'name': 'test_add_05.csv'
                },
                'tags': [
                    {
                        'name': os.path.join(cwd, 'sources', 'df3.csv'),
                        'key': 'key',
                        'fields': ['new_value'],
                        'defaults': ['0.0']
                    }
                ]
            }
        }
        config_file = df_elf.get_output_path('test_config.cfg')
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        df_elf.load_config(config_file)
        input_df = pd.read_csv(os.path.join(cwd, 'sources', 'df1.csv'), dtype=str)
        df_elf.add(input_df)
        result_filename = os.path.join(cwd, 'sources', 'add.csv')
        dist_filename = df_elf.get_output_path(config['add']['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_add_06(self):
        df_elf = CSVFileElf()
        config = {
            'base': {
                'name': os.path.join(cwd, 'sources', 'df1.csv'),
                'key': 'key'
            },
            'output': {
                'name': 'test_add_06.csv'
            },
            'tags': [
                {
                    'name': os.path.join(cwd, 'sources', 'df5.csv'),
                    'key': 'new_key',
                    'fields': ['new_value'],
                    'defaults': ['0.0']
                }
            ]
        }
        result = df_elf.add(silent=True, **config)
        dist_filename = df_elf.get_output_path(config['output']['name'])
        result_filename = os.path.join(cwd, 'sources', 'add.csv')
        self.assertFalse(os.path.exists(dist_filename))
        res = df_elf.read_content(result_filename)
        self.assertTrue(np.array_equal(result.fillna(""), res.fillna("")))

    def test_add_duplicates(self):
        df_elf = CSVFileElf()
        config = {
            'base': {
                'name': os.path.join(cwd, 'sources', 'df4.csv'),
                'key': 'key',
                'drop_duplicates': True,
            },
            'output': {
                'name': 'test_add_d.csv'
            },
            'tags': [
                {
                    'name': os.path.join(cwd, 'sources', 'df3.csv'),
                    'key': 'key',
                    'fields': ['new_value'],
                    'defaults': ['0.0']
                }
            ]
        }
        df_elf.add(**config)
        result_filename = os.path.join(cwd, 'sources', 'add.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_exclude_n01(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'exclusion': [
                {
                    'key': 'value',
                    'op': '=',
                    'value': 0.18012179694014036
                }
            ],
            'output': {
                'name': 'test_exclude_n_=.csv'
            }
        }
        df_elf.exclude(**config)
        result_filename = os.path.join(cwd, 'result', 'exclude', 'exclude_n_=.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_exclude_n02(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'exclusion': [
                {
                    'key': 'value',
                    'op': '!=',
                    'value': 0.18012179694014036
                }
            ],
            'output': {
                'name': 'test_exclude_n_!=.csv'
            }
        }
        df_elf.exclude(**config)
        result_filename = os.path.join(cwd, 'result', 'exclude', 'exclude_n_!=.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_exclude_n03(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'exclusion': [
                {
                    'key': 'value',
                    'op': '>',
                    'value': 0
                }
            ],
            'output': {
                'name': 'test_exclude_n_gt.csv'
            }
        }
        df_elf.exclude(**config)
        result_filename = os.path.join(cwd, 'result', 'exclude', 'exclude_n_gt.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_exclude_n04(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'exclusion': [
                {
                    'key': 'value',
                    'op': '>=',
                    'value': 0
                }
            ],
            'output': {
                'name': 'test_exclude_n_gte.csv'
            }
        }
        df_elf.exclude(**config)
        result_filename = os.path.join(cwd, 'result', 'exclude', 'exclude_n_gte.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_exclude_n05(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'exclusion': [
                {
                    'key': 'value',
                    'op': '<',
                    'value': 0
                }
            ],
            'output': {
                'name': 'test_exclude_n_lt.csv'
            }
        }
        df_elf.exclude(**config)
        result_filename = os.path.join(cwd, 'result', 'exclude', 'exclude_n_lt.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_exclude_n06(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'exclusion': [
                {
                    'key': 'value',
                    'op': '<=',
                    'value': 0
                }
            ],
            'output': {
                'name': 'test_exclude_n_lte.csv'
            }
        }
        df_elf.exclude(**config)
        result_filename = os.path.join(cwd, 'result', 'exclude', 'exclude_n_lte.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_exclude_n07(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'exclusion': [
                {
                    'key': 'value',
                    'op': '=',
                    'value': 0.18012179694014036
                }
            ],
            'output': {
                'name': 'test_exclude_n_07.csv'
            }
        }
        result = df_elf.exclude(silent=True, **config)
        result_filename = os.path.join(cwd, 'result', 'exclude', 'exclude_n_=.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertFalse(os.path.exists(dist_filename))
        res = df_elf.read_content(result_filename)
        self.assertTrue(np.array_equal(result.fillna(""), res.fillna("")))

    def test_exclude_s01(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'exclusion': [
                {
                    'key': 'key',
                    'op': '=',
                    'value': 'D'
                }
            ],
            'output': {
                'name': 'test_exclude_=.csv'
            }
        }
        df_elf.exclude(**config)
        result_filename = os.path.join(cwd, 'result', 'exclude', 'exclude_=.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_exclude_s02(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'exclusion': [
                {
                    'key': 'key',
                    'op': '!=',
                    'value': 'D'
                }
            ],
            'output': {
                'name': 'test_exclude_!=.csv'
            }
        }
        df_elf.exclude(**config)
        result_filename = os.path.join(cwd, 'result', 'exclude', 'exclude_!=.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_exclude_s03(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'exclusion': [
                {
                    'key': 'key',
                    'op': '>',
                    'value': 'D'
                }
            ],
            'output': {
                'name': 'test_exclude_gt.csv'
            }
        }
        df_elf.exclude(**config)
        result_filename = os.path.join(cwd, 'result', 'exclude', 'exclude_gt.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_exclude_s04(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'exclusion': [
                {
                    'key': 'key',
                    'op': '>=',
                    'value': 'D'
                }
            ],
            'output': {
                'name': 'test_exclude_gte.csv'
            }
        }
        df_elf.exclude(**config)
        result_filename = os.path.join(cwd, 'result', 'exclude', 'exclude_gte.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_exclude_s05(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'exclusion': [
                {
                    'key': 'key',
                    'op': '<',
                    'value': 'D'
                }
            ],
            'output': {
                'name': 'test_exclude_lt.csv'
            }
        }
        df_elf.exclude(**config)
        result_filename = os.path.join(cwd, 'result', 'exclude', 'exclude_lt.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_exclude_s06(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'exclusion': [
                {
                    'key': 'key',
                    'op': '<=',
                    'value': 'D'
                }
            ],
            'output': {
                'name': 'test_exclude_lte.csv'
            }
        }
        df_elf.exclude(**config)
        result_filename = os.path.join(cwd, 'result', 'exclude', 'exclude_lte.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_exclude_s07(self):
        df_elf = CSVFileElf()
        config = {
            'exclusion': [
                {
                    'key': 'key',
                    'op': '<=',
                    'value': 'D'
                }
            ],
            'output': {
                'name': 'test_exclude_lte_02.csv'
            }
        }
        input_df = pd.read_csv(os.path.join(cwd, 'sources', 'df4.csv'), dtype=str)
        df_elf.exclude(input_df, **config)
        result_filename = os.path.join(cwd, 'result', 'exclude', 'exclude_lte.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_split_01(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'products_p3.csv'),
            'output': {
                'prefix': 'split'
            },
            'key': 'B'
        }
        df_elf.split(**config)
        df_elf_01 = CSVFileElf(output_flag=False)
        df_elf_01.split(**config)
        filenames = ['B1', 'B2', 'B3', 'B4']
        for filename in filenames:
            real_filename = config['output']['prefix'] + '_' + filename + '.csv'
            result_filename = os.path.join(cwd, 'result', 'split', real_filename)
            dist_filename = df_elf.get_output_path(real_filename)
            dist_filename_01 = df_elf_01.get_log_path(real_filename)
            self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))
            self.assertEqual(df_elf_01.checksum(result_filename), df_elf_01.checksum(dist_filename_01))

    def test_split_02(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'products_p3.csv'),
            'output': {
                'prefix': 'split02',
                'non-numeric': ['E', 'D']
            },
            'key': 'D'
        }
        df_elf.split(**config)
        filenames = ['D1', 'D2']
        for filename in filenames:
            real_filename = config['output']['prefix'] + '_' + filename + '.csv'
            result_filename = os.path.join(cwd, 'result', 'split', real_filename)
            dist_filename = df_elf.get_output_path(real_filename)
            self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_split_03(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'products_p3.csv'),
            'output': {
                'prefix': 'split02',
                'non-numeric': ['E', 'D']
            },
            'key': 'Z'
        }
        with self.assertRaises(KeyError):
            df_elf.split(**config)

    def test_split_04(self):
        df_elf = CSVFileElf()
        config = {
            'output': {
                'prefix': 'split04',
                'non-numeric': ['E', 'D']
            },
            'key': 'D'
        }
        input_df = pd.read_csv(os.path.join(cwd, 'sources', 'products_p3.csv'), dtype=str)
        df_elf.split(input_df, **config)
        filenames = ['D1', 'D2']
        for filename in filenames:
            real_filename = config['output']['prefix'] + '_' + filename + '.csv'
            result_filename = 'split02_' + filename + '.csv'
            result_filename = os.path.join(cwd, 'result', 'split', result_filename)
            dist_filename = df_elf.get_output_path(real_filename)
            self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_split_05(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'products_p3.csv'),
            'output': {
                'prefix': 'split_05'
            },
            'key': 'B'
        }
        result = df_elf.split(silent=True, **config)
        filenames = ['B1', 'B2', 'B3', 'B4']
        i = 0
        for filename in filenames:
            real_filename = config['output']['prefix'] + '_' + filename + '.csv'
            result_filename = 'split_' + filename + '.csv'
            result_filename = os.path.join(cwd, 'result', 'split', result_filename)
            dist_filename = df_elf.get_output_path(real_filename)
            self.assertFalse(os.path.exists(dist_filename))
            res = df_elf.read_content(result_filename)
            self.assertTrue(np.array_equal(result[i].fillna(""), res.fillna("")))
            i = i + 1

    def test_filter_n01(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'filters': [
                {
                    'key': 'value',
                    'op': '=',
                    'value': 0.18012179694014036
                }
            ],
            'output': {
                'name': 'test_filter_n_=.csv'
            }
        }
        df_elf.filter(**config)
        result_filename = os.path.join(cwd, 'result', 'filter', 'filter_n_=.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_filter_n02(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'filters': [
                {
                    'key': 'value',
                    'op': '!=',
                    'value': 0.18012179694014036
                }
            ],
            'output': {
                'name': 'test_filter_n_!=.csv'
            }
        }
        df_elf.filter(**config)
        result_filename = os.path.join(cwd, 'result', 'filter', 'filter_n_!=.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_filter_n03(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'filters': [
                {
                    'key': 'value',
                    'op': '>',
                    'value': 0
                }
            ],
            'output': {
                'name': 'test_filter_n_gt.csv'
            }
        }
        df_elf.filter(**config)
        result_filename = os.path.join(cwd, 'result', 'filter', 'filter_n_gt.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_filter_n04(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'filters': [
                {
                    'key': 'value',
                    'op': '>=',
                    'value': 0
                }
            ],
            'output': {
                'name': 'test_filter_n_gte.csv'
            }
        }
        df_elf.filter(**config)
        result_filename = os.path.join(cwd, 'result', 'filter', 'filter_n_gte.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_filter_n05(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'filters': [
                {
                    'key': 'value',
                    'op': '<',
                    'value': 0
                }
            ],
            'output': {
                'name': 'test_filter_n_lt.csv'
            }
        }
        df_elf.filter(**config)
        result_filename = os.path.join(cwd, 'result', 'filter', 'filter_n_lt.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_filter_n06(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'filters': [
                {
                    'key': 'value',
                    'op': '<=',
                    'value': 0
                }
            ],
            'output': {
                'name': 'test_filter_n_lte.csv'
            }
        }
        df_elf.filter(**config)
        result_filename = os.path.join(cwd, 'result', 'filter', 'filter_n_lte.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_filter_n07(self):
        df_elf = CSVFileElf()
        config = {
            'filters': [
                {
                    'key': 'value',
                    'op': '<=',
                    'value': 0
                }
            ],
            'output': {
                'name': 'test_filter_n_lte.csv'
            }
        }
        input_df = pd.read_csv(os.path.join(cwd, 'sources', 'df4.csv'), dtype=str)
        df_elf.filter(input_df, **config)
        result_filename = os.path.join(cwd, 'result', 'filter', 'filter_n_lte.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_filter_n08(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'filters': [
                {
                    'key': 'value',
                    'op': '=',
                    'value': 0.18012179694014036
                }
            ],
            'output': {
                'name': 'test_filter_n_08.csv'
            }
        }
        result = df_elf.filter(silent=True, **config)
        result_filename = os.path.join(cwd, 'result', 'filter', 'filter_n_=.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertFalse(os.path.exists(dist_filename))
        res = df_elf.read_content(result_filename)
        self.assertTrue(np.array_equal(result.fillna(""), res.fillna("")))

    def test_filter_s01(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'filters': [
                {
                    'key': 'key',
                    'op': '=',
                    'value': 'D'
                }
            ],
            'output': {
                'name': 'test_filter_=.csv'
            }
        }
        df_elf.filter(**config)
        result_filename = os.path.join(cwd, 'result', 'filter', 'filter_=.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_filter_s02(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'filters': [
                {
                    'key': 'key',
                    'op': '!=',
                    'value': 'D'
                }
            ],
            'output': {
                'name': 'test_filter_!=.csv'
            }
        }
        df_elf.filter(**config)
        result_filename = os.path.join(cwd, 'result', 'filter', 'filter_!=.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_filter_s03(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'filters': [
                {
                    'key': 'key',
                    'op': '>',
                    'value': 'D'
                }
            ],
            'output': {
                'name': 'test_filter_gt.csv'
            }
        }
        df_elf.filter(**config)
        result_filename = os.path.join(cwd, 'result', 'filter', 'filter_gt.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_filter_s04(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'filters': [
                {
                    'key': 'key',
                    'op': '>=',
                    'value': 'D'
                }
            ],
            'output': {
                'name': 'test_filter_gte.csv'
            }
        }
        df_elf.filter(**config)
        result_filename = os.path.join(cwd, 'result', 'filter', 'filter_gte.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_filter_s05(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'filters': [
                {
                    'key': 'key',
                    'op': '<',
                    'value': 'D'
                }
            ],
            'output': {
                'name': 'test_filter_lt.csv'
            }
        }
        df_elf.filter(**config)
        result_filename = os.path.join(cwd, 'result', 'filter', 'filter_lt.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_filter_s06(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'df4.csv'),
            'filters': [
                {
                    'key': 'key',
                    'op': '<=',
                    'value': 'D'
                }
            ],
            'output': {
                'name': 'test_filter_lte.csv'
            }
        }
        df_elf.filter(**config)
        result_filename = os.path.join(cwd, 'result', 'filter', 'filter_lte.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_join_01(self):
        df_elf = CSVFileElf()
        config = {
            'base': os.path.join(cwd, 'sources', 'df4.csv'),
            'output': {
                'name': 'test_join_01.csv'
            },
            'files': [
                {
                    'name': os.path.join(cwd, 'sources', 'df3.csv'),
                    'mappings': {'new_value': 'value'}
                },
                {
                    'name': os.path.join(cwd, 'sources', 'df2.csv'),
                    'mappings': {}
                }
            ]
        }
        df_elf.join(**config)
        result_filename = os.path.join(cwd, 'result', 'join.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_join_02(self):
        df_elf = CSVFileElf()
        config = {
            'output': {
                'name': 'test_join_02.csv'
            },
            'files': [
                {
                    'name': os.path.join(cwd, 'sources', 'df3.csv'),
                    'mappings': {'new_value': 'value'}
                },
                {
                    'name': os.path.join(cwd, 'sources', 'df2.csv'),
                    'mappings': {}
                }
            ]
        }
        input_df = pd.read_csv(os.path.join(cwd, 'sources', 'df4.csv'), dtype=str)
        df_elf.join(input_df, **config)
        result_filename = os.path.join(cwd, 'result', 'join.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_join_03(self):
        df_elf = CSVFileElf()
        config = {
            'base': os.path.join(cwd, 'sources', 'df4.csv'),
            'output': {
                'name': 'test_join_03.csv'
            },
            'files': [
                {
                    'name': os.path.join(cwd, 'sources', 'df3.csv'),
                    'mappings': {'new_value': 'value'}
                },
                {
                    'name': os.path.join(cwd, 'sources', 'df2.csv'),
                    'mappings': {}
                }
            ]
        }
        result = df_elf.join(silent=True, **config)
        result_filename = os.path.join(cwd, 'result', 'join.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertFalse(os.path.exists(dist_filename))
        res = df_elf.read_content(result_filename)
        self.assertTrue(np.array_equal(result.fillna(""), res.fillna("")))

    def test_default(self):
        df_elf = CSVFileElf()
        config = {}
        self.assertEqual(None, df_elf.add(**config))
        self.assertEqual(None, df_elf.join(**config))
        self.assertEqual(None, df_elf.exclude(**config))
        self.assertEqual(None, df_elf.filter(**config))
        self.assertEqual(None, df_elf.split(**config))
        self.assertEqual(None, df_elf.merge(**config))

    def test_set_output(self):
        output_dir = os.path.join('output', 'test' + str(random()))
        self.assertFalse(os.path.exists(output_dir))
        CSVFileElf(output_dir=output_dir)
        self.assertTrue(os.path.exists(output_dir))

    def test_merge_01(self):
        df_elf = CSVFileElf()
        input_filename_01 = os.path.join(cwd, 'sources', 'merge', 'cf_161505.csv')
        input_filename_02 = os.path.join(cwd, 'sources', 'merge', 'fh_161505.csv')
        config = {
            'input': [input_filename_01, input_filename_02],
            'output': {
                'name': 'merge_01.csv',
                'BOM': False,
                'non-numeric': []
            },
            'on': ['生效日期', '基金代码'],
            'mappings': {'权益登记日': '生效日期', '拆分折算日': '生效日期'}
        }
        df_elf.merge(**config)
        result_filename = os.path.join(cwd, 'result', 'merge.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_merge_02(self):
        df_elf = CSVFileElf()
        input_filename_01 = os.path.join(cwd, 'sources', 'merge', 'cf_161505.csv')
        input_filename_02 = os.path.join(cwd, 'sources', 'merge', 'fh_161505.csv')
        config = {
            'output': {
                'name': 'merge_02.csv',
            },
            'on': ['生效日期', '基金代码'],
            'mappings': {'权益登记日': '生效日期', '拆分折算日': '生效日期'}
        }
        input_df_01 = pd.read_csv(input_filename_01, dtype=str)
        input_df_02 = pd.read_csv(input_filename_02, dtype=str)
        result = df_elf.merge([input_df_01, input_df_02], True, **config)
        result_filename = os.path.join(cwd, 'result', 'merge.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertFalse(os.path.exists(dist_filename))
        res = df_elf.read_content(result_filename)
        self.assertTrue(np.array_equal(result.fillna(""), res.fillna("")))

    def test_merge_03(self):
        df_elf = CSVFileElf()
        input_filename_01 = os.path.join(cwd, 'sources', 'merge', 'cf_161505.csv')
        input_filename_02 = os.path.join(cwd, 'sources', 'merge', 'fh_161505.csv')
        config = {
            'output': {
                'name': 'merge_03.csv',
                'BOM': False,
                'non-numeric': []
            },
            'on': ['生效日期', '基金代码'],
            'mappings': {'权益登记日': '生效日期', '拆分折算日': '生效日期'}
        }
        df_elf.merge([input_filename_01, input_filename_02], **config)
        result_filename = os.path.join(cwd, 'result', 'merge.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_merge_04(self):
        df_elf = CSVFileElf()
        input_filename_01 = os.path.join(cwd, 'sources', 'merge', 'cf_161505.csv')
        input_filename_02 = os.path.join(cwd, 'sources', 'merge', 'fh_161505.csv')
        input_df_01 = pd.read_csv(input_filename_01, dtype=str)
        config = {
            'output': {
                'name': 'merge_04.csv',
                'BOM': False,
                'non-numeric': []
            },
            'on': ['生效日期', '基金代码'],
            'mappings': {'权益登记日': '生效日期', '拆分折算日': '生效日期'}
        }
        df_elf.merge([input_df_01, input_filename_02], **config)
        result_filename = os.path.join(cwd, 'result', 'merge.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_trans_object_error_01(self):
        df_elf = CSVFileElf()
        input_filename_01 = os.path.join(cwd, 'sources', 'merge', 'cf_161505.csv')
        config = {
            'output': {
                'name': 'merge_04.csv',
                'BOM': False,
                'non-numeric': []
            },
            'on': ['生效日期', '基金代码'],
            'mappings': {'权益登记日': '生效日期', '拆分折算日': '生效日期'}
        }
        with self.assertRaises(TypeError):
            df_elf.merge(input_filename_01, **config)

    def test_trans_object_error_02(self):
        df_elf = CSVFileElf()
        config = {
            'output': {
                'name': 'merge_04.csv',
                'BOM': False,
                'non-numeric': []
            },
            'on': ['生效日期', '基金代码'],
            'mappings': {'权益登记日': '生效日期', '拆分折算日': '生效日期'}
        }
        with self.assertRaises(TypeError):
            df_elf.merge([1, 2], **config)

    def test_trans_object_error_03(self):
        df_elf = CSVFileElf()
        config = {
            'exclusion': [
                {
                    'key': 'key',
                    'op': '<=',
                    'value': 'D'
                }
            ],
            'output': {
                'name': 'test_exclude_lte_02.csv'
            }
        }
        with self.assertRaises(TypeError):
            df_elf.exclude(123, **config)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
