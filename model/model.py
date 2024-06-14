import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodi = []
        self._idMap = dict()
        self._migliori3 = []
        self.bestSol = []

    def buildGraph(self, brand, year):
        self._grafo.clear()
        for n in DAO.getAllNodi():
            if brand == n.Product_brand:
                self._grafo.add_node(n)
        self.addEdgesPesati(year)

    def addEdgesPesati(self, year):
        self._grafo.clear_edges()
        for n1 in self._grafo.nodes:
            for n2 in self._grafo.nodes:
                if n1.Product_number != n2.Product_number:
                    if self._grafo.has_edge(n1, n2) is False:
                        peso = DAO.getAllArchiPesati(n1, n2, year)
                        if peso > 0:
                            self._grafo.add_edge(n1, n2, weight=peso)

    def getBestPath(self, partenza):
        self.bestSol = []
        parziale = [partenza]
        self.ricorsione(parziale)
        print(self.bestSol)
        return self.bestSol

    def ricorsione(self, parziale):
        if len(self.bestSol) < len(parziale):
            self.bestSol = copy.deepcopy(parziale)
        for n in self._grafo.neighbors(parziale[-1]):
            parziale.append(n)
            if self.isCrescente(parziale):
                self.ricorsione(parziale)
            parziale.pop()

    def getBrand(self):
        brand = set()
        for s in DAO.getAllNodi():
            brand.add(s.Product_brand)
        return brand

    def isCrescente(self, parziale):
        peso = 0
        for i in range(len(parziale)-1):
            if self._grafo[parziale[i]][parziale[i+1]]['weight'] >= peso:
                peso += self._grafo[parziale[i]][parziale[i+1]]['weight']
            else:
                return False
        return True

    def getMigliori3(self):
        self._migliori3 = []
        for e in self._grafo.edges:
            self._migliori3.append((e[0], e[1], self._grafo[e[0]][e[1]]['weight']))
        ordinata = sorted(self._migliori3, key=lambda x: x[2], reverse=True)
        return ordinata

    def getCaratteristiche(self):
        return len(self._grafo.nodes), len(self._grafo.edges)