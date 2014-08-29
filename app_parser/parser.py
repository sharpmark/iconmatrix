from applications.models import Application
from app_parser.wdj_parser import wdj_parse
from app_parser.play_parser import play_parse


def get_app(package_name):

    app = wdj_parse(package_name)
    if app == None:
        app = play_parse(package_name)

    return app
