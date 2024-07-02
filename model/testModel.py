from model import Model

m = Model()
m.creaGrafo(2017, 1, 0.6)
print(m.grafoDetails())
print(m.top5Nodi())
print(m.trovaPercorso())