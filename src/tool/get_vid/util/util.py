# -*- coding:utf-8 -*-
import logging
import logging.handlers
import sys

def logger_init():
    logger = logging.getLogger();
    logger.setLevel(logging.INFO);

    handler = logging.StreamHandler(sys.stdout);
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s');
    handler.setFormatter(formatter);

    logger.addHandler(handler);
