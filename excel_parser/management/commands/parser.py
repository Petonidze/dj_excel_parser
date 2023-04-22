
from django.core.management.base import BaseCommand, CommandError

from excel_parser.logic import ExcelParser
from excel_parser.models import Data


class Command(BaseCommand):
    help = "Parsing excel file to filling Data table"

    def add_arguments(self, parser):
        parser.add_argument("file_name", type=str,
                            help='Enter the name of the excel file located in the "excel_parser/excels" directory')

    def handle(self, *args, **options):
        file_name = options.get('file_name')
        if file_name:
            parser = ExcelParser(file_name)
            object_list = self.get_object_list(parser)
            self.sql_insert_data(object_list)

    @staticmethod
    def get_object_list(parser):
        object_dict = parser.get_formatted_object_dict()
        object_list_of_dicts = object_dict.values()
        object_list = []
        for i in object_list_of_dicts:
            object_list.extend(list(i.values()))
        return object_list

    @staticmethod
    def sql_insert_data(object_list):
        Data.objects.bulk_create(object_list)
