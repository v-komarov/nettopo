#!/usr/bin/python3.6
import unittest
import redis
import json
import conf
import networkx as nx
import sys
import pickle



def redis_obj():

    ### Redis 
    redis_host = conf.redis_host
    redis_port = conf.redis_port
    r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
    
    return r
    



def get_segment(data,ip):
    """Возвращение сегмента из общего графа"""
    aggr = json.loads(data)
    ag = aggr["aggr"] ### Адрес агрегатора
    G = nx.node_link_graph(aggr["data"])
    GG = nx.node_link_graph(aggr["data"])
    """Удаление агрегатора из графа"""
    G.remove_node(ag)
    """Поиск ip по сегментам"""
    segment_list = []
    for g in [G.subgraph(c) for c in nx.connected_components(G)]: # Обход подграфов
        if g.has_node(ip):
            segment_list = list(g.nodes())
            break
    segment_list.append(ag)
    SEG = GG.subgraph(segment_list)

    return SEG






class TestMethod(unittest.TestCase):


    def setUp(self):

        ### Redis 
        redis_host = conf.redis_host
        redis_port = conf.redis_port
        self.r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

    def tearDown(self):
        pass


    def test_redis(self):
        """Проверка записи - чтения ключа"""
        self.r.set('test','xxxxxxxxxxxxxxx',60)
        self.assertEqual(self.r.get('test').decode(),'xxxxxxxxxxxxxxx',"Нет связи с Redis сервером")


    def test_data(self):
        """Проверка наличия данных для теста"""
        aggr = json.loads(self.r.get('55.17.0.19').decode())
        self.assertIs(type(aggr),type(dict()),"Данные для теста отсутствуют или не корректны")


    def test_segment(self):
        """Проверка выделения сегмента по ip адресу"""
        aggr = json.loads(self.r.get('55.17.0.19').decode())
        G = nx.node_link_graph(aggr["data"])
        GG = nx.node_link_graph(aggr["data"])
        ag = aggr["aggr"] ### Адрес агрегатора
        """Удаление агрегатора из графа"""
        G.remove_node(ag)
        """Поиск ip по сегментам"""
        segment_list = []
        for g in [G.subgraph(c) for c in nx.connected_components(G)]: # Обход подграфов
            if g.has_node('55.17.2.32'):
                segment_list = list(g.nodes())
                break
        segment_list.append(ag)
        SEG = GG.subgraph(segment_list)
        print(SEG.nodes)
        with open('segment.pickle', 'wb') as f:
            pickle.dump(SEG,f)
        self.assertNotEqual(len(list(SEG.nodes)),0,"Не создана структура сегмента сети")




if __name__ == "__main__":


    unittest.main()
