# -*- coding:utf-8 -*-
import logging
import logging.handlers
import sys
from datetime import datetime, timedelta

def logger_init():
    logger = logging.getLogger();
    logger.setLevel(logging.INFO);

    handler = logging.StreamHandler(sys.stdout);
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s');
    handler.setFormatter(formatter);

    logger.addHandler(handler);

def get_date_since(days):
    dt = datetime.now() - timedelta(days=days)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    print get_date_since(2)
