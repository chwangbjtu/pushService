import sys
from http_client import HttpClient
import json

def load_id(f):
    fd = open(f)
    ids = []
    while True:
        line = fd.readline().strip('\n')
        if not line:
            break
        ids.append(line)

    return ids

if __name__ == "__main__":
    f = sys.argv[1]
    ids = load_id(f)
    #print ids

    http_client = HttpClient()
    for id in ids:
        body = {"task_id": [id]}
        print json.dumps(body)
        http_client.post_data('http://centaurus.funshion.com:6531/notify_delete_task', json.dumps(body))
