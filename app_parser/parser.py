from applications.models import Application
from app_parser.wdj_parser import parse_url


def get_app(package_name, update=False):

    app, created = Application.objects.get_or_create(package_name=package_name)
    if created or update:
        parse_url(app)

    return app
