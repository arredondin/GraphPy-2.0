class Node:
	"""Clase Nodo, generada para la vista"""
	def __init__(self, data):
		self.__color = (0,0,0)
		self.__shape = 1 		#Puede Ser 1 o 2
		self.__label = "new"
		self.__size = 10
		self.__id = random.randint(1,1000)
		self.__position = (data.x, data.y) 		#Posicion del Mouse
	
	def set_color(self, newColor):
		"""Modifica el Color del Nodo"""
		self.__color = newColor
	
	def get_color(self):
		"""Obtiene el Color del Nodo"""
		return self.__color
	
	def set_shape(self, newShape):
		"""Modifica la Forma del Nodo"""
		self.__shape = newShape
		
	def get_shape(self):
		"""Obtiene la Forma del Nodo"""
		return self.__shape
	
	def set_label(self, newLabel):
		"""Modifica el texto del Nodo"""
		self.__label = newLabel
	
	def get_label(self):
		"""Obtiene el texto del Nodo"""
		return self.__label
	
	def set_size(self, newSize):
		"""Modifica el Tamanio del Nodo"""
		self.__size = newSize
	
	def get_size(self):
		"""Obtiene el Tamanio del Nodo"""
		return self.__size
		
	def set_id(self, newId):
		"""Modifica el ID del Nodo"""
		self.__id = newId
	
	def get_id(self):
		"""Obtiene el ID del Nodo"""
		return self.__id
		
	def set_position(self, newPosition):
		"""Modifica la Posicion del Nodo"""
		self.__size = newSize
	
	def get_position(self):
		"""Obtiene la Posicion del Nodo"""
		return self.__position
		
class Edge:
	"""Clase Edge (Arista) generada para la vista"""
	def __init__(self, connection):
		self.__color = (0,0,0)
		self.__shape = 1
		self.__weight = 1
		self.__wide = 5
		self.__connection = connection
	
	def set_color(self, newColor):
		"""Modifica el Color de la Arista"""
		self.__color = newColor
	
	def get_color(self):
		"""Obtiene el Color de la Arista"""
		return self.__color
	
	def set_shape(self, newShape):
		"""Modifica la Forma de la Arista"""
		self.__shape = newShape
		
	def get_shape(self):
		"""Obtiene la Forma de la Arista"""
		return self.__shape
	
	def set_weight(self, newWeight):
		"""Modifica el peso de la Arista"""
		self.__weight = newWeight
	
	def get_weight(self):
		"""Obtiene el peso de la Arista"""
		return self.__label
	
	def set_wide(self, newWide):
		"""Modifica el Grosor de la Arista"""
		self.__wide = newWide
	
	def get_wide(self):
		"""Obtiene el Grosor de la Arista"""
		return self.__wide

	def set_connection(self, newConnection):
		"""Modifica la Coneccion de la Arista"""
		self.__connection = newConnection
	
	def get_connection(self):
		"""Obtiene la Coneccion de la Arista"""
		return self.__connection
	
class Graph:

	def __init__(self):
		"""Constructor del Grafo, genera una Lista de nodos y de Arcos"""
		self.__nodes = []
		self.__edges = []
	
	def new_node(self, pos):
		"""Inserta un nuevo Nodo en el Grafo, recibe el ID, Etiqueta y la Posicion (x,y)"""
		try:
			tmp = Node(pos)
			self.__nodes.append(tmp)
			return True
		except:
			return False
	
	def new_edge(self, connection):
		"""Inserta una Arista al Grafo, recibe el Peso de la arista y la Conexion 
		(ID Nodo Origen, ID Nodo Destino)"""
		try:
			tmpEdge = Edge(connection)
			self.__edges.append(tmpEdge)
			return True
		except:
			return False
	
	def get_nodes(self):
		"""Obtiene la Lista de Nodos del Grafo"""
		return self.__nodes

	def get_edges(self):
		"""Obtiene la Lista de Aristas del Grafo"""
		return self.__edges
	
	def del_node(self, idTarget):
		"""Elimina un Nodo del grafo por su ID"""
		for i in range(len(self.__nodes)):
			if(self.__nodes[i].get_id() == idTarget):
				var = i
		for i in self.__nodes:
			if i.get_id() == idTarget:
				for j in self.__edges:
					if j.get_connection()[0] == idTarget or j.get_connection()[1] == idTarget:
						self.__edges.remove(j)
				self.__nodes.remove(i)
				return var
		return None

	def del_edge(self, connection):
		"""Elimina una Arista del Grafo por su Conexion"""
		for i in self.__edges:
			if i.get_connection() == connection:
				self.__edges.remove(i)
				return True
		return False
	
	def get_node(self, idTarget):
		"""Obtiene un Nodo del Grafo por su ID"""
		try:
			for i in self.__nodes:
				if idTarget == i.get_id():
					return i
		except:
			return None
	
	def exist_edge(self, connection):
		"""Verifica si existe una Arista que Une a 2 Nodos (Conexion) en el Grafo"""
		for i in self.__edges:
			if i.get_connection() == connection:
				return True
		return False