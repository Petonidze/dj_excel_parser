
from django.core.management.base import BaseCommand, CommandError

from excel_parser.logic import TotalCalculator


class Command(BaseCommand):
    help = "Calculate total by date"

    def handle(self, *args, **options):
        total_calc = TotalCalculator()
        total_calc.print_totals()
