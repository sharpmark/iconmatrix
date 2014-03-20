from django.core.management.base import BaseCommand

from app_parser.wdj_parser import crawl_wdj_weekly_top

class Command(BaseCommand):
    def handle(self, *args, **options):
        crawl_wdj_weekly_top()

