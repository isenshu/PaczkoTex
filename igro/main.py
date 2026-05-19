from config import mapFileName
from graf import buildGraph
from mapa import createMap


G = buildGraph()
m = createMap(G)

try:
    m.save(mapFileName)
    print("zapisano mape")
except:
    print("blad, nie zapisano mapy")
