from applications.models import Application
from app_parser.wdj_parser import parse


def get_app(package_name):

    return parse(package_name)
