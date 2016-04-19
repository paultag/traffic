from django.core.management.base import BaseCommand, CommandError
from traffic.models import Moving

import os
import csv

class Command(BaseCommand):
    help = 'Load Mappings'

    def add_arguments(self, parser):
        parser.add_argument(type=str, dest='path', help='csv root')

    def handle(self, *args, path, **options):
        for dirpath, dirnames, filenames in os.walk(top=path):
            for name in filenames:
                if not name.startswith("Moving_Violations_in_"):
                    continue
                with open(os.path.join(dirpath, name), 'r') as fd:
                    entries = csv.DictReader(fd)
                    self.scrape_moving_violations(entries)

    def scrape_moving_violations(self, rows):
        for row in rows:
            moving = Moving.create_from_csv(row)
            # print(moving)
