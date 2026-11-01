from database.DAO import DAO
from itertools import combinations
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}


    def buildGraph(self):
        self._grafo.clear()
        self._idMap = {}

        nodi = DAO.getNodi()
        self._idMap = {a.id: a for a in nodi}
        self._grafo.add_nodes_from(nodi)

        for idA, idC in DAO.getCoppia():
            if idA in self._idMap:
                self._idMap[idA].playlist.add(idC)

        for idA, idT in DAO.getTracks():
            if idA in self._idMap:
                self._idMap[idA].brani.add(idT)

        for a1, a2 in combinations(nodi, 2):
            comuni = a1.playlist & a2.playlist
            if len(comuni) > 0:
                self._grafo.add_edge(a1, a2, weight=len(comuni))


    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()


    def getGradoMax(self):
        gradoMax = -1
        for n in self._grafo.nodes:
            grado = self._grafo.degree(n)
            if grado > gradoMax:
                gradoMax = grado

        best = [n for n in self._grafo.nodes if self._grafo.degree(n) == gradoMax]
        best.sort(key=lambda x: x.nome.lower())
        return best[0], gradoMax


    def getIncidenti(self):
        peso = -1
        artista = None
        for n in self._grafo.nodes:
            p = self._grafo.degree(n, weight="weight")
            if p>peso:
                peso = p
                artista = n
        return artista,peso


    def get10(self):
        archi =[]
        for u,v,dati in self._grafo.edges(data=True):
          nomi = sorted([u.nome,v.nome])
          archi.append((nomi[0], nomi[1], dati["weight"]))
        archi.sort(key=lambda x: (-x[2], x[0],x[1]))
        return archi[:10]

    def getNodiOrdinati(self):
        return sorted(self._grafo.nodes, key=lambda a: str(a))


    def getGruppo(self, partenza, N):
        self._solBest = []
        self._braniBest = -1
        self._N = N
        self._ricorsione([partenza])
        return self._solBest, self._braniBest

    # ==================== PUNTO 2 ====================

    def getGruppo(self, partenza, N):
        self._N = N
        self._solBest = []
        self._braniBest = -1
        self._visti = set()
        self._ricorsione([partenza])
        return self._solBest, self._braniBest

    def _ricorsione(self, parziale):
        # 0. gruppo già visto in un altro ordine -> mi fermo
        chiave = frozenset(parziale)
        if chiave in self._visti:
            return
        self._visti.add(chiave)

        # 1. caso terminale: il gruppo ha N artisti
        if len(parziale) == self._N:
            brani = sum(len(a.brani) for a in parziale)
            if brani > self._braniBest:
                self._braniBest = brani
                self._solBest = list(parziale)
            return

        # 2. candidati: vicini degli artisti già nel gruppo
        candidati = set()
        for p in parziale:
            for v in self._grafo.neighbors(p):
                if self._ammissibile(v, parziale):
                    candidati.add(v)

        # 3. provo ad aggiungere ogni candidato
        for c in candidati:
            parziale.append(c)
            self._ricorsione(parziale)
            parziale.pop()

    def _ammissibile(self, c, parziale):
        if c in parziale:
            return False
        for p in parziale:
            if self._grafo.has_edge(c, p) and self._grafo[c][p]["weight"] == 1:
                return False
        return True

    def getArtista(self, idA):
        return self._idMap.get(idA)