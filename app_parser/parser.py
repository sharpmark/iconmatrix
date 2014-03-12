from applications.models import Application
from app_parser.wdj_parser import parse_url

def get_app_from_url(url):

    return parse_url(url)
