class Vertice: # classe vértice
	def __init__(self,name):
		self.name = name
		self.weight = -1
		self.predEdge = -1

class Graph: #classe grafo
	def __init__(self):
		self.vertices = {} #dicionario de vertices com o nome do vertice como chave
		self.edges = [] #lista de arestas

	def addVertice(self,vertice): #adiciona um vertice novo
		self.vertices[vertice] = Vertice(vertice)

	def addEdge(self,v1,v2,weight): #adiciona uma aresta nova
		self.edges.append([v1,v2,weight])
	
	def addEdge2(self,v1,v2,weight,ind): #adiciona uma aresta nova em um indice especifico
		self.edges.insert(ind,[v1,v2,weight])

	def prim(self,v): #devolve a MST do grafo
		foundVertices = []
		MSTEdges = []
		for i in self.vertices: #reseta os valores
			self.vertices[i].weight=-1
			self.vertices[i].predEdge=-1

		self.vertices[v].weight=0
		verticeAtual=v #seta o primeiro vertice como vertice atual
		foundVertices.append(verticeAtual) #adiciona o vertice atual como achado

		while(len(foundVertices)<len(self.vertices)):#para quando achar todos os vértices
			
			for ind,i in enumerate(self.edges): # atualiza os pesos do vertice atual

				whichOne=-1

				if(i[0]==verticeAtual):
					whichOne=0
				if(i[1]==verticeAtual):
					whichOne=1

				if(whichOne!=-1):

					nameVerticeMudar = self.vertices[i[1-whichOne]].name
					pesoAtualVertice = self.vertices[nameVerticeMudar].weight
					if(pesoAtualVertice == -1 or pesoAtualVertice > i[2]): # se o peso novo for maior que o peso anterior atualiza o peso

						self.vertices[nameVerticeMudar].weight = i[2]
						self.vertices[nameVerticeMudar].predEdge = ind

			verticeAtual = -1
			for i in self.vertices: # checa todos os vertices
				
				if(i in foundVertices): # se ja tiver sido achado ignora
					continue
				
				if(verticeAtual == -1): # se não tiver nenhum vertice atual pega o primeiro
					verticeAtual = i
				else:
					pesoAtual = self.vertices[verticeAtual].weight
					peso = self.vertices[i].weight
					if(pesoAtual==-1 or pesoAtual>peso): #se achar um vértice com peso menor usa ele como vertice atual
						verticeAtual=i
			foundVertices.append(verticeAtual)
			MSTEdges.append(self.vertices[verticeAtual].predEdge) #adiciona a aresta que achou esse vértice
		return MSTEdges # retorna as arestas da MST

	def twiceAround(self,v): # implementa o twice around
		MSTEdgeIndexes = self.prim(v)
		MSTEdges = []
		for i in MSTEdgeIndexes:
			MSTEdges.append(self.edges[i])
			MSTEdges.append(self.edges[i])
		print(MSTEdges) # printa a MST com as arestas duplicadas
		grafo = Graph()
		for i in self.vertices:
			grafo.addVertice(i)
		
		for i in MSTEdges: #cria um grafo só com as arestas da MST duplicadas
			grafo.addEdge(i[0],i[1],i[2])
		grafo.printAll()
		caminhoRepetido = self.fleury(grafo,v) #retorna o caminho que usa todas as arestas do grafo
		print(caminhoRepetido)
		caminho=[]
		for i in caminhoRepetido:#adiciona os vertices não repetidos desse caminho
			if(i not in caminho):
				caminho.append(i)
		caminho.append(caminhoRepetido[len(caminhoRepetido)-1]) #adiciona o vertice inicial denovo
		print(caminho) # printa os vertices do caminho
		caminhoFinal = []
		for i in range(len(caminho)):
			if(i<len(caminho)-1):
				for j in self.edges:
					if(j[0]==caminho[i] and j[1]==caminho[i+1]) or (j[0]==caminho[i+1] and j[1]==caminho[i]):
						caminhoFinal.append(j)
						break
		print(caminhoFinal)# printa as arestas do caminho


	def fleury(self,grafo,v): # implementa o fleury e retorna o caminho
		caminho = []
		caminho.append(v)
		return self.fleuryRecursivo(grafo,v,caminho)

	def fleuryRecursivo(self,grafo,v,caminho): # recursivamente cria o caminho usando o fleury 
		for ind,i in enumerate(grafo.edges):
			
			if(i[0]==v or i[1]==v):# checa se a aresta usa o vertice atual
				print(v,i)
				if(i[0]==v):
					u=i[1]
				if(i[1]==v):
					u=i[0]
				if(grafo.isValidNextEdge(ind,v)):# checa se a aresta é valida
					print("valido")
					grafo.rmvEdge(ind)
					caminho.append(u)
					self.fleuryRecursivo(grafo,u,caminho)
		return caminho
		
	def isValidNextEdge(self,ind,v): # checa se a aresta pode ser usada
		numeroArestas = 0
		aresta = self.edges[ind]
		for i in self.edges:
			if(i[0]==v or i[1]==v):
				numeroArestas+=1
		if(numeroArestas<=1): # se tiver só uma aresta usa aquela
			return True
		else: # checa se a aresta é uma ponte 
			visited = {}
			for i in self.vertices:
				visited[i]=False
			num1 = self.DFSCount(v,visited)

			self.rmvEdge(ind)

			for i in self.vertices:
				visited[i]=False
			num2 = self.DFSCount(v,visited)

			self.addEdge2(aresta[0],aresta[1],aresta[2],ind)

			return num1==num2

	def DFSCount(self,v,visited):
		#visited são os vertices ja visitados(para não contar duas vezes)
		count = 1
		#seta o visited do vertice atual como true
		visited[v] = True
		for i in self.edges:
			#print(i)
			if(i[0]==v or i[1]==v):
				if(i[0]==v):
					u=i[1]
				if(i[1]==v):
					u=i[0]
				if visited[u] ==False:
					#roda a própria função recursivamente e adiciona o count do vizinho no count atual
					count = count + self.DFSCount(u,visited)
		#retorna o numero de vertices visitados
		return count

	def rmvEdge(self,ind): # remove aresta de certo indice
		self.edges.pop(ind)

	def printAll(self):#printa o grafo
		print("comeca printar grafo")
		print("vertices:")
		for i in self.vertices:
			print(self.vertices[i].name)
		print("arestas:")
		for i in self.edges:
			print(i)
		print("termina printar grafo")


grafo = Graph()

grafo.addVertice("v1")
grafo.addVertice("v2")
grafo.addVertice("v3")
grafo.addVertice("v4")

grafo.addEdge("v1", "v2", 2)
grafo.addEdge("v1", "v3", 5)
grafo.addEdge("v1", "v4", 1)

grafo.addEdge("v2", "v3", 4)
grafo.addEdge("v2", "v4", 3)

grafo.addEdge("v3", "v4", 2)

grafo.printAll()

grafo.twiceAround("v1")