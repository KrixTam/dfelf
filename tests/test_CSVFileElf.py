# coding: utf-8

import unittest
import os
from CSVFileElf import CSVFileElf


# import pandas as pd


class TestCSVFileElf(unittest.TestCase):

    def test_drop_duplicates(self):
        input_filename = os.path.join('sources', 'ori_data.csv')
        log_result = os.path.join('result', 'drop_duplicates.ori.log')
        df_elf = CSVFileElf()
        df = df_elf.read_content(input_filename)
        log_filename = df_elf.drop_duplicates(df, 'brand')[1]
        log_file = os.path.join('log', log_filename)
        self.assertEqual(df_elf.checksum(log_file), df_elf.checksum(log_result))

    def test_add(self):
        df_elf = CSVFileElf()
        config = {
            'base': {
                'name': os.path.join('sources', 'df1.csv'),
                'key': 'key'
            },
            'output': {
                'name': 'test_add.csv'
            },
            'tags': [
                {
                    'name': os.path.join('sources', 'df3.csv'),
                    'key': 'key',
                    'fields': ['new_value'],
                    'defaults': ['0.0']
                }
            ]
        }
        df_elf.add(**config)
        result_filename = os.path.join('sources', 'add.csv')
        dist_filename = df_elf.get_output_path(config['output']['name'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))

    def test_split(self):
        df_elf = CSVFileElf()
        config = {
            'input': os.path.join('sources', 'products_p3.csv'),
            'output': {
                'prefix': 'split'
            },
            'key': 'B'
        }
        df_elf.split(**config)
        filenames = ['B1', 'B2', 'B3', 'B4']
        for filename in filenames:
            real_filename = config['output']['prefix'] + '_' + filename + '.csv'
            result_filename = os.path.join('result', real_filename)
            dist_filename = df_elf.get_output_path(real_filename)
            self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))
        config = {
            'input': os.path.join('sources', 'products_p3.csv'),
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
            result_filename = os.path.join('result', real_filename)
            dist_filename = df_elf.get_output_path(real_filename)
            self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))


if __name__ == '__main__':
    unittest.main()
