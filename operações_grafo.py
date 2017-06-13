from grafo import *

condition = 1

while True:
    while condition == 1:
        temp_v = input("Informe os vértices separados por vírgula e espaço (ex.: A, B, C...): ")
        vértices = temp_v.split(", ")
        vértices_incorretos = []
        for f1 in vértices:
            if Grafo.verticeValido(f1) == True and "(" not in f1 and ")" not in f1 and " " not in f1:
                pass
            else:
                vértices_incorretos.append(f1)
        if vértices_incorretos != []:
            print("O(s) seguinte(s) vértice(s) é(são) inválido(s):")
            for vi in vértices_incorretos:
                print(vi)
            print("Por favor, informe todos os vértices novamente, e certifique-se de não colocar traços, espaços e parênteses.")
            vértices = []
            vértices_incorretos = []
        else:
            condition = 2

    while condition == 2:
        temp_g = []
        temp_a = input("Informe as arestas e, entre parênteses, os vértices que essa aresta conecta, em ordem, separados por vírgula e espaço (ex.: aresta1(vértice1-vértice2)): ")
        temp_g = temp_a.split(", ")
        nome_da_aresta = []
        vértice1 = []
        vértice2 = []
        for A in range(len(temp_g)):
            temp_g[A] = temp_g[A].replace("(", " ")
            temp_g[A] = temp_g[A].replace("-", " ")
            temp_g[A] = temp_g[A].replace(")", " ")
            temp_g[A] = temp_g[A].split(" ")
        for A in range(len(temp_g)):
            nome_da_aresta.append(temp_g[A][0])
            vértice1.append(temp_g[A][1])
            vértice2.append(temp_g[A][2])
        count = 0
        for A in nome_da_aresta:
            if A == "":
                print("Nome da aresta não informado.")
                count += 1
        for V1 in vértice1:
            if V1 not in vértices:
                print('O vértice "', V1, '" não existe.')
                count += 1
        for V2 in vértice2:
            if V2 not in vértices:
                print('O vértice "', V2, '" não existe.')
                count += 1
        if count == 0:
            condition = 3
        else:
            print("Por favor, informe novamente as arestas, seguindo expressamente as recomendações.")

    dicionário = {}

    if condition == 3:
        for x in temp_g:
            dicionário[x[0]] = x[1] + "-" + x[2]
        grafo = Grafo(vértices, dicionário)
        print(grafo)

    #a): Encontra todos os pares de vértices não adjacentes:
    print("a): Vértices não adjacentes: ", grafo.encontraNaoAdjacentes())

    #b): Verifica se existe algum laço, ou seja, um vértice adjacente a ele mesmo:
    print("b): Existe laço?: ", grafo.existeLaço())

    #c): Verifica se existe alguma aresta paralela:
    print("c): Existe aresta paralela?: ", grafo.existeArestaParalela())

    #d): Verifica o grau de um vértice:
    vertice1 = input("Informe um vértice que deseja obter o grau: ")
    print("d): Grau do vértice", vertice1, ": ", grafo.calculaGrauVertice(vertice1))

    #e): Encontra arestas incidentes sobre um dado vértice:
    vertice2 = input("Informe um vértice que deseja obter as arestas incidentes sobre o mesmo: ")
    print("e): Arestas incidentes sobre o vértice", vertice2, ": ", grafo.encontraArestasIncidentes(vertice2))

    #f): Verifica se o grafo é completo:
    print("f): O grafo é completo?: ", grafo.verificaGrafoCompleto())

    #Verifica conexo:
    print("Comb: ", grafo.verificaGrafoConexo())

    break

# a1(A-B), a2(B-C), a3(A-C)
