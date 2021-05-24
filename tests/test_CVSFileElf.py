# coding: utf-8

import unittest
import os
from CVSFileElf import CVSFileElf


# import pandas as pd


class TestCVSFileElf(unittest.TestCase):

    def test_drop_duplicates(self):
        input_filename = os.path.join('sources', 'ori_data.csv')
        log_result = os.path.join('result', 'drop_duplicates.ori.log')
        df_elf = CVSFileElf()
        df = df_elf.read_content(input_filename)
        log_filename = df_elf.drop_duplicates(df, 'brand')[1]
        log_file = os.path.join('log', log_filename)
        self.assertEqual(df_elf.checksum(log_file), df_elf.checksum(log_result))

    def test_add(self):
        df_elf = CVSFileElf()
        config = {
            'base': {
                'name': os.path.join('sources', 'df1.csv'),
                'key': 'key'
            },
            'output': 'test_add.csv',
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
        dist_filename = df_elf.get_output_path(config['output'])
        self.assertEqual(df_elf.checksum(result_filename), df_elf.checksum(dist_filename))


if __name__ == '__main__':
    unittest.main()
