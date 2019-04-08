"""
Apps module is responsible for all required application configuration

"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    CoreConfig prepares proprietary configuration for application
    """
    name = 'core'
