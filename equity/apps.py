from django.apps import AppConfig
from . import bse_utils
class EquityConfig(AppConfig):
    name = 'equity'

    def ready(self):
        bse_utils.index(self)