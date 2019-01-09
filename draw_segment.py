#!/usr/bin/python3.6
import unittest
import networkx as nx
import pickle
import matplotlib as plt



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





if __name__ == "__main__":


    unittest.main()
