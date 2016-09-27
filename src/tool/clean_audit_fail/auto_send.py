import sys
from http_client import HttpClient
import json
from dao import Dao
from db_connect import MysqlConnect
import logging

if __name__ == "__main__":
    try:
        from util import logger_init
        from util import get_date_since
        logger_init()

        db_conn = MysqlConnect()
        dao = Dao(db_conn)

        http_client = HttpClient()

        fail_task = dao.get_fail_task(get_date_since(2))

        for t in fail_task:
            body = {"task_id": [t['task_id']]}
            logging.info(json.dumps(body))
            res = http_client.post_data('http://centaurus.funshion.com:6531/notify_delete_task', json.dumps(body))
            logging.info(res)
            if res and res[0] == 200:
                dao.insert_fail(t)
                db_conn.commit()


    except Exception,e:
        logging.info(traceback.format_exc())
