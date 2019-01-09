#!/usr/bin/python3.6
import unittest
import networkx as nx
import pickle
from graphviz import Graph



class TestMethod(unittest.TestCase):



    def test_segment(self):
        """Проверка чтения сегмента"""
        with open('segment.pickle', 'rb') as f:
            G = pickle.load(f)
            self.assertNotEqual(len(list(G.nodes)),0)


    def test_draw(self):
        """Рисование сегмента"""
        with open('segment.pickle', 'rb') as f:
            G = pickle.load(f)

            g = Graph()
            for e in G.edges:
                g.edge(e[0],e[1])
                
            Graph.draw('pic.png')

            #pos = nx.spring_layout(G)
            #nx.draw(G,pos)



if __name__ == "__main__":


    unittest.main()
