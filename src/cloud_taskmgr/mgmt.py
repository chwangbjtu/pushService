#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import logging
import state_machine

URL_SHUTDONW_SERVER = "/mgmt/close"
URL_SHOW_STATE = "/mgmt/show_state"

def initialize(router):
    router.add(URL_SHUTDONW_SERVER,handle_to_shutdown_server)
    router.add(URL_SHOW_STATE,handle_to_show_state)

def handle_to_shutdown_server(request):
    state_machine.cycle.set_exit()
    body = {}
    body["result"] = "ok"
    body["status"] = "exiting..."
    body = json.dumps(body)
    logging.info("to shutdown server message from %s, url %s: %s", request.remote_ip, request.uri, body)
    return body

def handle_to_show_state(request):
    map_obj = state_machine.cycle.pack_map_obj()
    try:
        json_str = json.dumps(map_obj)
        return json_str
    except Exception,e:
        return {"result":"fail"}
