# coding = utf-8

import logging
logger = logging.getLogger(__name__)

from django.conf import settings


def DEBUG(msg):
    if settings.DEBUG:
        logger.debug(msg)