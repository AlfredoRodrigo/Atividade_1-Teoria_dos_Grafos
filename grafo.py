from collections import defaultdict
from heapq import *
import copy

class VerticeInvalidoException(Exception):
    pass

class ArestaInvalidaException(Exception):
    pass

class Grafo:

    QTDE_MAX_SEPARADOR = 1
    SEPARADOR_ARESTA = '-'

    def __init__(self, N=[], A={}, P={}):
        '''
        Constrói um objeto do tipo Grafo. Se nenhum parâmetro for passado, cria um Grafo vazio.
        Se houver alguma aresta ou algum vértice inválido, uma exceção é lançada. Caso tudo esteja
        em conformidade com as regras, uma matriz de adjascência é criada.
        :param N: Uma lista dos vértices (ou nodos) do grafo.
        :param V: Um dicionário que guarda as arestas do grafo. A chave representa o nome da aresta
        e o valor é uma string que contém dois vértices separados por um traço.
        '''
        self.arestas = []
        self.comb = []
        qtd_A = []
        self.matriz_adjacencia = []
        count = -1

        for v in N:
            if not(Grafo.verticeValido(v)):
                raise VerticeInvalidoException('O vértice ' + v + ' é inválido')

        self.N = N

        for a in A:
            if not(self.arestaValida(A[a])):
                raise ArestaInvalidaException('A aresta ' + A[a] + ' é inválida')

        self.A = A

        # A partir deste ponto até o final desta função, o código cria a matriz de adjacência.
        # Cada bloco de comentários é referente ao "for" imediatamente seguinte a este bloco.

        # Primeiramente, na lista self.arestas são inseridas listas com os vértices que são conectados no grafo.
        # Este "for" cria listas a partir dos valores das chaves do dicionário, os separando pelo traço.
        # Exemplo: Se o grafo receber três vértices, A, B e C, e duas arestas, a1(A-B) e a2(B-C), então a lista
        # self.arestas receberá [[A, B], [B, C]].
        for x in A:
            aresta = A[x].split("-")
            auxiliar = [aresta[1], aresta[0]]
            self.arestas.append(aresta)
            self.arestas.append(auxiliar)


        self.arestas_valoradas = []

        for x in self.arestas:
            nome_aresta = str(x[0]) + "-" + str(x[1])
            temp1 = []
            temp2 = []
            if nome_aresta in P:
                temp1.append(x[0])
                temp1.append(x[1])
                temp1.append(P[nome_aresta])
                temp1[2] = int(temp1[2])
                tupla1 = tuple(temp1)
                temp2.append(x[1])
                temp2.append(x[0])
                temp2.append(P[nome_aresta])
                temp2[2] = int(temp2[2])
                tupla2 = tuple(temp2)
                self.arestas_valoradas.append(tupla1)
                self.arestas_valoradas.append(tupla2)

        # Cria uma lista self.comb com todas as combinações possíveis de ligações dos vértices
        # passados como parâmetro ao grafo. Exemplo: Se o grafo receber dois vértices, A e B, será criada uma
        # lista self.comb igual a [[A, A], [A, B], [B, A], [B, B]].
        for x in range(len(N)):
            for y in range(len(N)):
                aux1 = [N[x], N[y]]
                self.comb.append(aux1)

        # Conta a quantidade de arestas para inserção na matriz de adjacência por meio da comparação
        # das listas self.comb e self.arestas. Percorrendo a lista self.comb, ele verifica quantas vezes o iésimo
        # elemento da mesma pertence também a self.arestas, e adiciona esta quantidade à lista qtd_A.
        # Como o grafo é do tipo não direcionado, ele também faz as considerações necessárias para este caso,
        # como por exemplo, o tratamento da ocorrência de [B, A] e de [A, B]. Cada posição de qtd_A está relacionada
        # com a matriz de adjacência.

        for x in self.comb:
            c1 = self.arestas.count(x)
            qtd_A.append(c1)

        # Transforma a lista qtd_A em uma matriz de adjacência.
        for i in range(len(N)):
            inicio = int(i * len(self.comb) / len(N))
            fim = int((i + 1) * len(self.comb) / len(N))
            self.matriz_adjacencia.append(qtd_A[inicio:fim])

        self.matriz_adjacencia_pesos = copy.deepcopy(self.matriz_adjacencia)

        for x in range(len(N)):
            for y in range(len(N)):
                a = N[x] + "-" + N[y]
                if a in P:
                    self.matriz_adjacencia_pesos[x][y] = P[a]

    def encontraNaoAdjacentes(self):
        '''
        Verifica os vértices não adjacentes, ou seja, os vértices que não possuem ligação entre si.
        Trabalhando em cima da matriz de adjacência, esta função retorna uma matriz chamada naoAdjacentes,
        onde cada linha desta matriz é encarada como um par ordenado de vértices não adjacentes. Com base na matriz
        de adjacência, a função verifica em quais posições da mesma estão localizados os zeros, significando que não
        há ligação entre aqueles vértices daquela posição. Quando encontrado algum zero, a função insere dentro da
        matriz naoAdjacentes uma linha, onde o primeiro índice correponde a um vértice que não possui ligação
        com o vértice do segundo índice.
        :return: uma matriz com pares ordenados de vértices não adjacentes.
        '''
        naoAdjacentes = []
        for i in range(len(self.matriz_adjacencia)):
            for j in range(len(self.matriz_adjacencia[i])):
                if self.matriz_adjacencia[i][j] == 0:
                    naoAdjacentes.append([self.N[i], self.N[j]])
        return naoAdjacentes

    def existeLaço(self):
        '''
        Verifica a existeência de laços, ou seja, vértices adjacentes a ele mesmo.
        Através do "for" com o intervalo do tamanho da matriz, a função percorre todas as linhas da mesma,
        a procura de laços. Utilizando índices iguais em self.matriz ([i][i]), a função percorre somente a
        diagonal principal. Neste caso, só nos interessa a diagonal principal, pois ela é quem relaciona um vértice
        com ele mesmo. Quando a funçã encontra algum número diferente de zero, então ela returna True, significando
        que nessa matriz de adjacência há pelo menos um laço. Quando ela não encontra, ou seja, quando todos os
        números da diagonal principal são zero, a função retorna False, significando que a mesma não encontrou
        nenhum laço.
        :return: um valor booleano que indica a existência ou não de pelo menos um laço na matriz de adjacência.
        '''
        for i in range(len(self.matriz_adjacencia)):
            if self.matriz_adjacencia[i][i] != 0:
                return True
        return False

    def existeArestaParalela(self):
        '''
        Verifica se existe alguma aresta paralela.
        A função percorre a matriz em busca de qualquer número que seja maior que 1, significando que entre os vértices
        daquela posição existem mais de uma aresta, ou seja, que existem arestas paralelas.
        :return: um valor booleano que indica ou não a presença de arestas paralelas na matriz de adjacência.
        '''
        for i in range(len(self.matriz_adjacencia)):
            for j in range(len(self.matriz_adjacencia)):
                if i < j:
                    if self.matriz_adjacencia[i][j] > 1:
                        return True
        return False

    def calculaGrauVertice(self, vertice):
        '''
        Calcula o grau de um vértice passado como parâmetro, ou seja, quantas arestas têm conectadas a este vértice.
        A função retorna o índice na lista de vértices de um vértice passado como parâmetro, e então, para aquele índice
        correspondente a linha na matriz de adjacência, a função soma todas as arestas encontradas naquela linha. Em
        seguida, o processo é repetido, mas desta vez com as colunas, ignorando somente o elemento pertencente a
        diagonal principal, pois este já foi contabilizado na contagem anterior. Ao final, a função retorna a soma
        de tudo.
        :param vertice: um vértice que se deseja calcular o seu grau
        :return: um valor inteiro referente ao grau do vértice
        '''
        indice = self.N.index(vertice)
        grau = 0
        for x in range(len(self.matriz_adjacencia)):
            if type(self.matriz_adjacencia[indice][x]) == int:
                grau += self.matriz_adjacencia[indice][x]
        for y in range(len(self.matriz_adjacencia)):
            if y != indice:
                if type(self.matriz_adjacencia[y][indice]) == int:
                    grau += self.matriz_adjacencia[y][indice]
        return grau

    def encontraArestasIncidentes(self, vertice):
        '''
        Verifica e encontra as arestas que incidem sobre o vertice passado como parâmetro.
        A função coleta do dicionário as chaves, que são as arestas do grafo, e as coloca na lista nomeArestas.
        Em seguida, é verificado se o vértice passado como parâmetro se encontra em alguma das posições da lista
        self.arestas, significando que existe uma ligação dele com outro. Encontrada uma ligação, então é feita uma
        correspondência entre o índice da lista self.arestas e o índice da lista nomeArestas, e a lista
        nomeArestasIncidentes recebe o elemento correspondente na lista nomeArestas.
        Ao final, a função retorna uma lista com os nomes das arestas que se conectam com o vértice passado como
        parâmetro.
        :param vertice: um vértice que se deseja obter o nome de suas arestas.
        :return: uma lista com o nome das arestas incidentes sobre este vértice.
        retorna 0 se nenhuma aresta incidente for encontrada for encontrada.
        '''
        nomeArestas = []
        nomeArestasIncidentes = []
        for x in self.A:
            nomeArestas.append(x)
        for x in range(len(self.arestas)):
            if vertice in self.arestas[x]:
                nomeArestasIncidentes.append(nomeArestas[x])
        if (len(nomeArestasIncidentes) != 0):
            return nomeArestasIncidentes
        return 0

    def verificaGrafoCompleto(self):
        '''
        Verifica se o grafo criado é ou não completo. Para um grafo ser classificado como completo, é
        necessário existir pelo menos uma ligação entre um vértice qualquer a outro vértice qualquer.
        Sabendo disto, é possível determinar se um grafo é compelto ou não somente olhando para a matriz.
        Ignorando a diagonal principal e tudo abaixo dela, se em alguma posição restante existir algum zero,
        significa que aquela ligação entre os respectivos vértices não existe, classificando o grafo como
        incompleto. E é isto que a função faz. Ela realiza diversos testes afim de encontrar algum zero e
        retornar um resultado negativo. Uma vez passado por todos os testes, significa que o grafo é completo,
        retornando um resultado positivo.
        :return: um valor booleano que indica se o grafo é ou não completo.
        '''

        for i in range(len(self.matriz_adjacencia)):
            for j in range(len(self.matriz_adjacencia)):
                if (i < j) and (i != j):
                    if (self.matriz_adjacencia[i][j] == 0):
                        return False
        return True

    def warshall(self):
        '''
        Este algoritmo é chamado de algoritmo de Warshall, e serve para ancontrar a matriz de alcançabilidade
        de um grafo, ou seja, uma matriz que determina se é possível chegar de um vértice X a um vértice Y de
        alguma maneira. Este algoritmo foi escrito seguindo exatamente o pseudocódigo fornecido pelo professor.
        :return: uma matriz de alcançabilidade.
        '''
        matrizCopia = list(self.matriz_adjacencia)

        for i in range(len(matrizCopia)):
            for j in range(len(matrizCopia)):
                if matrizCopia[i][j] > 0:
                    matrizCopia[i][j] = 1

        for i in range(len(matrizCopia)):
            for j in range(len(matrizCopia)):
                if matrizCopia[j][i] == 1:
                    for k in range(len(matrizCopia)):
                        matrizCopia[j][k] = max(matrizCopia[j][k], matrizCopia[i][k])
        return matrizCopia

    def arestaValida(self, aresta=''):
        '''
        Verifica se uma aresta passada como parâmetro está dentro do padrão estabelecido.
        Uma aresta é representada por um string com o formato a-b, onde:
        a é um substring de aresta que é o nome de um vértice adjacente à aresta.
        - é um caractere separador. Uma aresta só pode ter um único caractere como esse.
        b é um substring de aresta que é o nome do outro vértice adjacente à aresta.
        Além disso, uma aresta só é válida se conectar dois vértices existentes no grafo.
        :param aresta: A aresta que se quer verificar se está no formato correto.
        :return: Um valor booleano que indica se a aresta está no formato correto.
        '''

        # Não pode haver mais de um caractere separador
        if aresta.count(Grafo.SEPARADOR_ARESTA) != Grafo.QTDE_MAX_SEPARADOR:
            return False

        # Índice do elemento separador
        i_traco = aresta.index(Grafo.SEPARADOR_ARESTA)

        # O caractere separador não pode ser o primeiro ou o último caractere da aresta
        if i_traco == 0 or aresta[-1] == Grafo.SEPARADOR_ARESTA:
            return False

        if not(self.existeVertice(aresta[:i_traco])) or not(self.existeVertice(aresta[i_traco+1:])):
            return False

        return True

    def dijkstra(self, v_inicio, v_destino):
        g = defaultdict(list)
        for l, r, c in self.arestas_valoradas:
            g[l].append([c, r])
        q, seen = [[0, v_inicio, []]], set()
        while q:
            [cost, v1, path] = heappop(q)
            if v1 not in seen:
                seen.add(v1)
                path = [v1, path]
                if v1 == v_destino:
                    return [cost, path]
                for c, v2 in g.get(v1, []):
                    if v2 not in seen:
                        heappush(q, [cost + c, v2, path])

        return [0, "Sem caminho"]

    @classmethod
    def verticeValido(self, vertice=''):
        '''
        Verifica se um vértice passado como parâmetro está dentro do padrão estabelecido.
        Um vértice é um string qualquer que não pode ser vazio e nem conter o caractere separador.
        :param vertice: Um string que representa o vértice a ser analisado.
        :return: Um valor booleano que indica se o vértice está no formato correto.
        '''
        return vertice != '' and vertice.count(Grafo.SEPARADOR_ARESTA) == 0

    def existeVertice(self, vertice=''):
        '''
        Verifica se um vértice passado como parâmetro pertence ao grafo.
        :param vertice: O vértice que deve ser verificado.
        :return: Um valor booleano que indica se o vértice existe no grafo.
        '''
        return Grafo.verticeValido(vertice) and self.N.count(vertice) > 0

    def existeAresta(self, aresta=''):
        '''
        Verifica se uma aresta passada como parâmetro pertence ao grafo.
        :param aresta: A aresta a ser verificada
        :return: Um valor booleano que indica se a aresta existe no grafo.
        '''
        existe = False
        if Grafo.arestaValida(self, aresta):
            for k in self.A:
                if aresta == self.A[k]:
                    existe = True

        return existe

    def adicionaVertice(self, v):
        if self.verticeValido(v):
            self.N.append(v)
        else:
            raise VerticeInvalidoException('O vértice ' + v + ' é inválido')

    def adicionaAresta(self, nome, a):
        if self.arestaValida(a):
            self.A[nome] = a
        else:
            ArestaInvalidaException('A aresta ' + self.A[a] + ' é inválida')

    def __str__(self):
        '''
        Fornece uma representação do tipo String do grafo.
        O String contém um sequência dos vértices separados por vírgula, seguido de uma sequência
        das arestas no formato padrão e de uma matriz de adjacência.
        :return: Uma string que representa o grafo.
        '''
        grafo_str = ""

        for v in range(len(self.N)):
            grafo_str += self.N[v]
            if v < (len(self.N) - 1):  # Só coloca a vírgula se não for o último vértice.
                grafo_str += ", "

        grafo_str += '\n'

        for i, a in enumerate(self.A):
            grafo_str += self.A[a]
            if not(i == len(self.A) - 1): # Só coloca a vírgula se não for a última aresta.
                grafo_str += ", "

        grafo_str += '\nMatriz de adjacência:\n'

        for x in self.matriz_adjacencia:
            for y in x:
                grafo_str += "|"
                grafo_str += str(y)
                grafo_str += "|"
            grafo_str += "\n"
        return grafo_str