# percorrendo um dicionário:

dicionário = {"a1": "A-B", "a2": "A-C", "a3": "B-C"}
for x in dicionário:
    print(x, "-", dicionário[x])

# contando ocorrências em uma lista:

lista = [["A", "B"], ["A", "C"], ["B", "C"]]
contador1 = lista.count(["A", "B"])
print(contador1)

# teste

lista2 = [["a", "b"], ["c", "d"], ["e", "f"]]
lista3 = []
for x in lista2:
    lista3.append(x)

for ç in lista3:
    ç.reverse()

print(lista2)
print("----------")
print(lista3)

"""
Percorri o dicionário salvando as arestas dentro de uma matriz, onde cada elemento é uma lista que contém como primeiro
e segundo elementos os primeiro e segundo vértices da aresta em questão, respectivamente.

Criei uma lista com todas as combinações de vértices possíveis, ou seja, o que há nessa lista são todas as posições da
matriz de adjacência.
"""