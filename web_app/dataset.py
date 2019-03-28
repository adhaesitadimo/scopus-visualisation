import mysql.connector
import networkx as nx
import random
from collections import defaultdict
from itertools import combinations
import json
from flask import render_template
from networkx.readwrite import json_graph
import os

class Dataset():
    mydb = mysql.connector.connect(
        host="articlesgrap.cxqhtfp4sprs.eu-central-1.rds.amazonaws.com",
        user="wizard",
        passwd="12345678",
        database="TheData"
        )

    from_year = 2010
    to_year = 2010
    coef = 0.003
    components_num = 5

    def __init__(self):
        self.authors = self._get_authors()
        print('Got authors')
        self.articles = self._get_articles()
        print('Got articles')
        self.auth_map = self._get_auth_map()
        print('Got map')
        self.gen_graph()

    def _get_authors(self):
        mycursor = self.mydb.cursor()
        sql = "SELECT * from TheData.Authors"
        mycursor.execute(sql)
        authors = mycursor.fetchall()
        mycursor.close()

        return authors

    def _get_articles(self):
        mycursor = self.mydb.cursor()
        sql = "SELECT * from TheData.Articles"
        mycursor.execute(sql)
        articles = mycursor.fetchall()
        mycursor.close()

        return articles

    def _get_auth_map(self):
        mycursor = self.mydb.cursor()
        sql = "SELECT * from TheData.isAuthor"
        mycursor.execute(sql)
        auth_map = mycursor.fetchall()
        mycursor.close()

        return auth_map


    def gen_graph(self, coef=0.03, from_year=2010, to_year=2010, components_num=5):
        self.from_year = from_year
        self.to_year = to_year
        self.coef = coef
        self.components_num = components_num

        filtered_arts = set(x[0] for x in self.articles \
                        if (x[2]>=from_year and x[2]<=to_year \
                        and random.random() <= coef))

        art_to_auth = defaultdict(list)

        filtered_authors = set()

        for i, auth, art in self.auth_map:
            if art in filtered_arts:
                art_to_auth[art].append(auth)
                filtered_authors.add(auth)

        i = 0
        max_s = 0
        print('Collected art2auth')
        edges_d = defaultdict(int)

        for art, auths in art_to_auth.items():
            for u, v in combinations(auths, 2):
                if (u, v) in edges_d:
                    edges_d[(u, v)] += 1
                    max_s = max(max_s, edges_d[(u, v)])
                else:
                    edges_d[(v, u)] += 1
                    max_s = max(max_s, edges_d[(v, u)])


        edges = []
        graph = nx.Graph()
        graph.add_nodes_from(filtered_authors)
        print('Graph init')

        for (u, v), w in edges_d.items():
            graph.add_edge(u, v, weight=w / max_s)


        spring_lo = nx.spring_layout(graph)
        print('Edges collected')


        labels = {}

        for author_id, author in self.authors:
            if author_id in filtered_authors:
                labels[author_id] = {'name': author}
        nx.set_node_attributes(graph, labels)

        components = sorted(list(nx.connected_component_subgraphs(graph)), key=lambda x: -len(x))
        # print(len(components), components_num)
        components_num = min(components_num, len(components))

        graphs_to_draw = nx.Graph()
        for i in range(components_num):
            graphs_to_draw = nx.compose(graphs_to_draw, components[i])

        spring_lo = nx.spring_layout(graphs_to_draw)
        edges = []
        for i, (u, v, weight) in enumerate(graphs_to_draw.edges(data=True)):
            edges.append(
                {
                    'id': str(i),
                    'source': str(u),
                    'target': str(v),
                    'color': 'rgba({}, {}, {}, {})'.format(23,63,95,(weight['weight']) ** 0.3,
                    ),
                }
            )

        nodes = []
        for author_id, name in graphs_to_draw.nodes(data=True):
            nodes.append(
                {
                    'id': str(author_id),
                    'label': name['name'],
                    'x': spring_lo[author_id][0],
                    'y': spring_lo[author_id][1],
                    'size': 10,
                    'color': 'rgb({}, {}, {})'.format(237,85,61)
                }
            )

        print('Nodes collected')
        self.nx_graph = graph
        self.graph = {'nodes': nodes, 'edges': edges}
        self.n_nodes = len(nodes)
        self.n_edges = len(edges)

    def render_graph(self):
        return render_template('idle.html', data=self.graph,
                               total_nodes=len(self.nx_graph.nodes()),
                               total_edges=len(self.nx_graph.edges()),
                               n_nodes=self.n_nodes, n_edges=self.n_edges,
                               settings = {'from_year': self.from_year,
                                           'to_year': self.to_year,
                                           'coef': (self.coef*100),
                                           'components_num': self.components_num
                                           })

    def download_graph(self, file_format):
        if file_format == 'graphml':
            nx.write_graphml(self.nx_graph, os.path.join(os.getcwd(), 'output.graphml'))
        elif file_format == 'gexf':
            nx.write_gexf(self.nx_graph, os.path.join(os.getcwd(), 'output.gexf'))
        elif file_format == 'gml':
            nx.write_gml(self.nx_graph, os.path.join(os.getcwd(), 'output.gml'))
        elif file_format == 'gpickle':
            nx.write_gpickle(self.nx_graph, os.path.join(os.getcwd(), 'output.gpickle'))
