"""Local development settings."""

from config.settings.base import *  # noqa: F403
from config.settings.base import env

DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
