# percorrendo um dicionário:
#
# dicionário = {"a1": "A-B", "a2": "A-C", "a3": "B-C"}
# for x in dicionário:
#     print(x, "-", dicionário[x])
#
# contando ocorrências em uma lista:
#
# lista = [["A", "B"], ["A", "C"], ["B", "C"]]
# contador1 = lista.count(["A", "B"])
# print(contador1)
#
# teste
#
# lista2 = [["a", "b"], ["c", "d"], ["e", "f"]]
# lista3 = []
# for x in lista2:
#     lista3.append(x)
#
# for ç in lista3:
#     ç.reverse()
#
# print(lista2)
# print("----------")
# print(lista3)
#
# v = ["A", "B", "C", "D", "E"]
#
# comb = []
#
# count = 0
# for
import copy

listaA = [1, 2]
listaB = copy.copy(listaA)
listaB[0] = 2
listaB[1] = 1

print(listaA, listaB)