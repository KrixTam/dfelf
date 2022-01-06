import os
import unittest
from dfelf import CSVFileElf

cwd = os.path.abspath(os.path.dirname(__file__))


class TestCSVFileElf(unittest.TestCase):

    def test_drop_duplicates(self):
        input_filename = os.path.join(cwd, 'sources', 'ori_data.csv')
        log_result = os.path.join(cwd, 'result', 'drop_duplicates.ori.log')
        df_elf = CSVFileElf()
        df = df_elf.read_content(input_filename)
        log_filename = df_elf.drop_duplicates(df, 'brand')[1]
        log_file = os.path.join('log', log_filename)
        self.assertEqual(df_elf.checksum(log_file), df_elf.checksum(log_result))

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
        filenames = ['B1', 'B2', 'B3', 'B4']
        for filename in filenames:
            real_filename = config['output']['prefix'] + '_' + filename + '.csv'
            result_filename = os.path.join(cwd, 'result', 'split', real_filename)
            dist_filename = df_elf.get_output_path(real_filename)
            self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

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

    def test_join(self):
        df_elf = CSVFileElf()
        config = {
            'base': os.path.join(cwd, 'sources', 'df4.csv'),
            'output': {
                'name': 'test_join.csv'
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


if __name__ == '__main__':
    unittest.main()
