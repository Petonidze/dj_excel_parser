import datetime
from random import choice
import pandas as pd
from json import loads
from excel_parser.models import Data
from django.db.models import Sum

COMPANY_HEADER = "('company', 'Unnamed: 1_level_1', 'Unnamed: 1_level_2')"
DAYS_CHOICES_LIST = [22, 11, 11, 11, 11, 21, 13, 21, 21, 22, 22]


class ExcelParser:
    def __init__(self, file_name=''):
        self.file_name = file_name

    def get_formatted_object_dict(self):
        json_data = self.parse_excel_to_json()
        parsed_data_dict = loads(json_data)
        object_dict = self.objects_cu(parsed_data_dict)
        return object_dict

    def parse_excel_to_json(self):
        df = pd.read_excel(f'excel_parser/excels/{self.file_name}.xlsx', index_col=0, header=[0, 1, 2])
        self.rows_count = len(df.index)
        json_data = df.to_json(orient="columns")
        return json_data

    def objects_cu(self, parsed_data_dict):
        """create/update objects to dict"""
        object_dict = {}
        for row_number in range(1, self.rows_count + 1):
            for headers_tuple, data_values_dict in parsed_data_dict.items():
                if headers_tuple == COMPANY_HEADER:
                    continue
                key_header = self.get_header_from_tuplestring(headers_tuple)
                data_obj = None
                if object_dict.get(str(row_number)):
                    data_obj = object_dict.get(str(row_number)).get(key_header)
                if not data_obj:
                    data_obj = Data()
                    data_obj.company = parsed_data_dict.get(COMPANY_HEADER).get(
                        str(row_number))
                    data_obj.fact = 'fact' in headers_tuple
                    data_obj.forecast = 'forecast' in headers_tuple
                    data_obj.qliq = 'Qliq' in headers_tuple
                    data_obj.qoil = 'Qoil' in headers_tuple
                    data_obj.date = datetime.date(2023, 4, choice(DAYS_CHOICES_LIST))
                if 'data1' in headers_tuple:
                    data_obj.data1 = data_values_dict.get(str(row_number))
                if 'data2' in headers_tuple:
                    data_obj.data2 = data_values_dict.get(str(row_number))
                result_header = self.get_result_header(data_obj)
                object_dict.setdefault(str(row_number), {}).update({result_header: data_obj})
        return object_dict

    @staticmethod
    def get_header_from_tuplestring(headers_tuple):
        result_header = headers_tuple.replace('data1', '').replace('data2', '')
        result_header = ''.join(filter(str.isalpha, result_header))
        return result_header

    @staticmethod
    def get_result_header(data_obj):
        result_header = 'fact' if data_obj.fact else ''
        result_header += 'forecast' if data_obj.forecast else ''
        result_header += 'Qliq' if data_obj.qliq else ''
        result_header += 'Qoil' if data_obj.qoil else ''
        return result_header


class TotalCalculator:

    def print_totals(self):
        params = [
            {"fact": True, 'qliq': True},
            {"fact": True, 'qoil': True},
            {"forecast": True, 'qliq': True},
            {"forecast": True, 'qoil': True},
        ]
        for param in params:
            fact_qliq_qs = self.get_data_qs(param)
            print(f'{" ".join(param.keys())} total:')
            for obj in fact_qliq_qs:
                print(f"On {obj.get('date')}:")
                print('data1_total:', obj.get('data1_total'))
                print('data2_total:', obj.get('data2_total'))
                print('_______________________________________')
            print('\n')

    @staticmethod
    def get_data_qs(param):
        return Data.objects.filter(**param).values('date').order_by('date') \
            .annotate(data1_total=Sum('data1')) \
            .annotate(data2_total=Sum('data2'))