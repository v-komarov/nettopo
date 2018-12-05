#!/usr/bin/python3.6

import redis
import argparse
import unittest
import json
import networkx as nx
import conf

### Redis 
redis_host = conf.redis_host
redis_port = conf.redis_port
r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

### Файл связей оборудования
flink = conf.flink

### Файл агрегаторов
faggr = conf.faggr

### Файл результатов
fresult = conf.fresult



class TestMethod(unittest.TestCase):

    def test_redis(self):
        """Проверка записи - чтения ключа"""
        r.set('test','xxxxxxxxxxxxxxx',60)
        self.assertEqual(r.get('test').decode(),'xxxxxxxxxxxxxxx')


    def test_link_file(self):
        """Проверка чтения файла связей"""
        f = open(flink,"r")
        j = f.readlines()
        f.close()
        for line in j:
            d = json.loads(line)


    def test_aggregator_file(self):
        """Проверка файла агрегаторов"""
        f = open(faggr,"r")
        j = f.readlines()
        f.close()
        k = {}
        for line in j:
            d = json.loads(line)
            aggr = d["address1"] # Адрес агрегатора
            port = d["port1"].strip() # Порт агрегатора
            if aggr in k:
                k[aggr].append(port)
            else:
                k[aggr] = [port,]





class MakeTopos(object):
    """Создание графов"""
    def __init__(self):
        global flink
        global faggr
        self.l = self.links(flink) # линки
        self.a = self.links(faggr) # агрегаторы
        self.d = self.mkdict() # Словарь агрегаторов
        self.g = [] # Набор графов структур агрегаторов
        self.res = {} # результирующий набор графов


    def links(self, fdata):
        """Создание генераторной функции"""
        with open(fdata,"r") as f:
            for j in f.readlines():
                yield json.loads(j)


    def mkdict(self):
        """Создание словаря агрегаторов"""
        k = {}
        for d in self.a:
            aggr = d["address1"] # Адрес агрегатора
            port = d["port1"].strip() # Порт агрегатора
            if aggr in k:
                k[aggr].append(port)
            else:
                k[aggr] = [port,]
        return k



    def mkgraphs(self):
        """Создание графов топологии"""
        G = nx.Graph()
        for l in self.l:
            if self.chkaggr(l["address1"],l["port1"].strip()) and self.chkaggr(l["address2"],l["port2"].strip()):
                G.add_edge(l["address1"],l["address2"])
        self.g = list(nx.connected_component_subgraphs(G))


    def chkgraph(self):
        """Проверка подграфов на наличие в них ip агрегаторов"""
        for g in self.g:
            for a in self.d.keys():
                if g.has_node(a):
                    self.res[a] = g


    def chkaggr(self,addr,port):
        """Проверка портов агрегаторов (на дерево вниз)"""
        if addr in self.d:
            aggr = self.d[addr]
            if port.strip() in aggr:
                return True
            else:
                return False
        else:
            return True


    def writefile(self):
        """Запись результатов в файл"""
        global fresult
        with open(fresult,"w") as f:
            for a in self.a:
                pass



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--testing', action="store_true", help='test mode')
    parser.add_argument('--flink', type=str)
    args = parser.parse_args()
    
    #unittest.main()
    m=MakeTopos()
    m.mkgraphs()
    m.chkgraph()
    print(m.res)