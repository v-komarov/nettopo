#!/usr/bin/python3.6
from bottle import route, get, run, request, response
import bottle
import redis
import json
import conf
import networkx as nx
import sys

from segment import get_segment

### Redis 
redis_host = conf.redis_host
redis_port = conf.redis_port
r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)





def aggr(ip):
    """Поиск информации по агрегатору"""
    result = r.get(ip)
    if result:
        
        if json.loads(result)["aggr"] == ip:
            """Агрегатор найден сразу"""
            data = json.loads(result.decode())
            data["segment"] = {}
            data["picture"] = ""
            return data
        
        else:
            """Поиск агрегатора"""
            d = r.get(json.loads(result)["aggr"]).decode()
            seg = get_segment(d,ip)
            data = json.loads(d)
            data["segment"] = nx.node_link_data(seg)
            data["picture"] = ""
            return data
    else:
        return json.dumps({"result":"error"})




@route('/',method='GET')
def topo():
    ip = request.query.get("ip")

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    response.content_type = 'application/json'

    return "{}".format(aggr(ip))


if __name__ == "__main__":

    run(host="", port=8080, debug=True)

app = bottle.default_app()
