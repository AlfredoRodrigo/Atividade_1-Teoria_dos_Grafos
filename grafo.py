class VerticeInvalidoException(Exception):
    pass

class ArestaInvalidaException(Exception):
    pass

class Grafo:

    QTDE_MAX_SEPARADOR = 1
    SEPARADOR_ARESTA = '-'

    def __init__(self, N=[], A={}):
        '''
        Constrói um objeto do tipo Grafo. Se nenhum parâmetro for passado, cria um Grafo vazio.
        Se houver alguma aresta ou algum vértice inválido, uma exceção é lançada.
        :param N: Uma lista dos vértices (ou nodos) do grafo.
        :param V: Uma dicionário que guarda as arestas do grafo. A chave representa o nome da aresta e o valor é uma string que contém dois vértices separados por um traço.
        '''
        self.arestas = []
        self.comb = []
        qtd_A = []
        self.matriz = []
        count = -1

        for v in N:
            if not(Grafo.verticeValido(v)):
                raise VerticeInvalidoException('O vértice ' + v + ' é inválido')

        self.N = N

        for a in A:
            if not(self.arestaValida(A[a])):
                raise ArestaInvalidaException('A aresta ' + A[a] + ' é inválida')

        self.A = A

        for x in A:
            self.arestas.append(A[x].split("-"))
        for x in range(len(N)):
            for y in range(len(N)):
                string = [N[x], N[y]]
                self.comb.append(string)
        for x in self.comb:
            c1 = self.arestas.count(x)
            aux = []
            if x[0] != x[1]:
                aux.append(x[1])
                aux.append(x[0])
            c2 = self.arestas.count(aux)
            c3 = c1 + c2
            qtd_A.append(c3)

        for i in range(len(N)):
            start = int(i * len(self.comb) / len(N))
            end = int((i + 1) * len(self.comb) / len(N))
            self.matriz.append(qtd_A[start:end])

        for x in self.matriz:
            count += 1
            for y in range(count):
                x[y] = "-"

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
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])):
                if self.matriz[i][j] == 0:
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
        for i in range(len(self.matriz)):
            if self.matriz[i][i] != 0:
                return True
        return False

    def existeArestaParalela(self):
        '''
        Verifica se existe alguma aresta paralela.
        A função percorre a matriz em busca de qualquer número que seja maior que 1, significando que entre os vértices
        daquela posição existem mais de uma aresta, ou seja, que existem arestas paralelas.
        :return: um valor booleano que indica ou não a presença de arestas paralelas na matriz de adjacência.
        '''
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz)):
                if self.matriz[i][j] != "-":
                    if self.matriz[i][j] > 1:
                        return True
        return False

    def calculaGrauVertice(self, vertice):
        '''
        Calcula o grau de um vértice passado como parametro, ou seja, quantas arestas têm conectadas a este vértice.
        A função retorna o índice na lista de vértices de um vértice passado como parametro, e então, para aquele índice
        correspondente a linha na matriz de adjacência, a função soma todas as arestas encontradas naquela linha.
        :param vertice: um vértice que se deseja calcular o seu grau
        :return: um valor inteiro referente ao grau do vértice
        '''
        indice = self.N.index(vertice)
        grau = 0
        for x in range(len(self.matriz)):
            if type(self.matriz[indice][x]) == int:
                grau += self.matriz[indice][x]
        return grau

    def encontraArestasIncidentes(self, vertice):
        nomeArestas = []
        nomeArestasIncidentes = []
        for x in self.A:
            nomeArestas.append(x)
        for x in range(len(self.arestas)):
            if vertice in self.arestas[x]:
                nomeArestasIncidentes.append(nomeArestas[x])
        return nomeArestasIncidentes

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
        O String contém um sequência dos vértices separados por vírgula, seguido de uma sequência das arestas no formato padrão.
        :return: Uma string que representa o grafo
        '''
        grafo_str = ''
        # count2 = 0

        for v in range(len(self.N)):
            grafo_str += self.N[v]
            if v < (len(self.N) - 1):  # Só coloca a vírgula se não for o último vértice
                grafo_str += ", "

        grafo_str += '\n---\n'

        for i, a in enumerate(self.A):
            grafo_str += self.A[a]
            if not(i == len(self.A) - 1): # Só coloca a vírgula se não for a última aresta
                grafo_str += ", "

        grafo_str += '\n---\n'

        # for y in range(len(self.N)):
        #     grafo_str += " "
        #     grafo_str += self.N[y]
        #     grafo_str += " "
        # grafo_str += "\n"

        for x in self.matriz:
            # a = self.N[count2]
            # grafo_str += a + " "
            for y in x:
                grafo_str += "|"
                grafo_str += str(y)
                grafo_str += "|"
            grafo_str += "\n"
            # count2 += 1
        return grafo_str
