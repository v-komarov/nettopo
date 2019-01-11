#!/usr/bin/python3.6
import unittest
import networkx as nx
import pickle
import pydot
import base64





def get_svg(G,ip,aggr):
    """Создание картинки в формате svg"""

    comments = nx.get_edge_attributes(G, 'comment')
    g = pydot.Dot(graph_type='graph')

    for n in G.nodes:

        if n == ip:
            color = "#E6E6FA"
        elif n == aggr:
            color = "#FFEBCD"
        else:
            color = "#F1F0F0"

            node = pydot.Node(n, style="filled", fillcolor=color)
            g.add_node(node)

    for e in G.edges:
        g.add_edge(pydot.Edge(e[0],e[1], label= comments[(e[0],e[1])]))

    svg = g.create_svg()

    return svg.decode()
    #return "data: image/svg+xml;base64,{}".format(base64.b64encode(svg))





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

            comments = nx.get_edge_attributes(G, 'comment')
            g = pydot.Dot(graph_type='graph')
            for n in G.nodes:
                
                if n == "55.17.2.32":
                    color = "#E6E6FA"
                elif n == "55.17.0.19":
                    color = "#FFEBCD"
                else:
                    color = "#F1F0F0"
                
                node = pydot.Node(n, style="filled", fillcolor=color)                    
                g.add_node(node)
                
            for e in G.edges:
                g.add_edge(pydot.Edge(e[0],e[1], label= comments[(e[0],e[1])]))
            
            g.write_svg('test.svg')
            svg = g.create_svg()
            print(svg.decode())



if __name__ == "__main__":


    unittest.main()
