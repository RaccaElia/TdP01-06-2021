import copy

import networkx as nx

from database.DAO import DAO
from database.DB_connect import DBConnect


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.idMap = {}
        for gene in DAO.getGeni():
            self.idMap[gene.GeneID] = gene
        self.ing = 0
        self.studio = {}

    def creaGrafo(self):
        self.grafo.add_nodes_from(self.idMap.values())
        archi = DAO.getArchi()
        for arco in archi:
            gene1 = self.idMap[arco[0]]
            gene2 = self.idMap[arco[1]]
            if gene1.Chromosome == gene2.Chromosome:
                peso = abs(arco[2])*2
            else:
                peso = abs(arco[2])
            self.grafo.add_edge(gene1, gene2, weight=peso)
        return self.grafo.nodes

    def grafoDetails(self):
        return len(self.grafo.nodes), len(self.grafo.edges)

    def getAdiacenti(self, gene):
        g = self.idMap[gene]
        ris = []
        for vicino in self.grafo.neighbors(g):
            ris.append((vicino, self.grafo[g][vicino]["weight"]))
        ris.sort(key=lambda x: x[1], reverse=True)
        return ris

    def simulazia(self, gene, n):
        self.ing = n
        self.ricorsione({self.idMap[gene]: n}, 0)
        return self.studio

    def ricorsione(self, parziale, mese):           #parziale = dizionario con chiave Gene e valore il numIng che lo studiano
        print(f"mese {mese}")
        if mese == 36:
            self.studio = copy.deepcopy(parziale)
            return
        else:
            for gene in parziale.keys():
                numIng = parziale[gene]
                parziale[gene] = 0.3*numIng
                self.distribuisci(gene, 0.7*numIng, parziale)
                self.ricorsione(parziale, mese+1)
                return

    def distribuisci(self, gene, ing, parziale):
        denominatore = 0
        for nodo in self.grafo.neighbors(gene):
            denominatore += self.grafo[gene][nodo]["weight"]

        for nodo in self.grafo.neighbors(gene):
            if nodo not in parziale.keys():
                parziale[nodo] = float(self.grafo[gene][nodo]["weight"]/denominatore)*ing
            else:
                parziale[nodo] += float(self.grafo[gene][nodo]["weight"]/denominatore)*ing

