	#
	#  STACK ACTIONS (UNDO-REDO)
	#


class Actions:
	"""Pila que maneja las acciones, para deshacer y rehacer"""
	
	def __init__(self):
		self.__count_actions = 0
		self.__actions = []
	
	def push(self, action):
		"""Agrega una accion"""
		if self.__count_actions <= 20:
			self.__actions.append(action)
			self.__count_actions += 1
		else:
			self.__actions.pop(0)
			self.__actions.append(action)
	
	def pop(self):
		"""Elimina la ultima accion"""
		if self.__count_actions == 0:
			return None
		self.__count_actions -= 1
		return self.__actions.pop()


	#
	#  FILE MANAGEMENT
	#



class Files:
	def __init__(self,name,state=True):
		self.__state = state
		if state:
			self.__file = open(name,"w")
		else:
			self.__file = open(name,"r")
	
	def new_open_file(self,name,mode):
		self.__file = open(name,mode)
		self.__state = True
	
	def open_from_file(self,module):
		if not self.__state:
			design = module
			tmp = design.Graph()
			type= bool(self.__file.readline())
			tmp.set_type(type)
			cnt_nodes = int(self.__file.readline())
			for i in xrange(cnt_nodes):
				id = int(self.__file.readline())
				label = str(self.__file.readline())
				positionx = float(self.__file.readline())
				positiony = float(self.__file.readline())
				position = (positionx,positiony)
				color_r = int(self.__file.readline())
				color_g = int(self.__file.readline())
				color_b = int(self.__file.readline())
				tamanio = int(self.__file.readline())
				forma = int(self.__file.readline())
				tmpNode = design.Node()
				tmpNode.set_id(id)
				tmpNode.set_label(label)
				tmpNode.set_position(position)
				tmpNode.set_color((color_r,color_g,color_b))
				tmpNode.set_size(tamanio)
				tmpNode.set_shape(forma)
				tmp.add_node(tmpNode)
			cnt_edges = int(self.__file.readline())
			print "aristas",cnt_edges
			for i in xrange(cnt_edges):
				weight = int(self.__file.readline())
				connectionx = int(self.__file.readline())
				connectiony = int(self.__file.readline())
				color_r = int(self.__file.readline())
				color_g = int(self.__file.readline())
				color_b = int(self.__file.readline())
				tamanio = int(self.__file.readline())
				forma = int(self.__file.readline())
				tmpEdge = design.Edge()
				tmpEdge.set_weight(weight,(connectionx,connectiony))
				tmpEdge.set_color((color_r,color_g,color_b))
				tmpEdge.set_size(forma)
				tmpEdge.set_shape(tamanio)
				tmp.add_edge(tmpNode)
			self.__file.close()
			self.__state = False
			return tmp
		else:
			return False
	
	def save_on_file(self,graph):
		if self.__state:
			self.__file.write(str(graph.get_type())+"\n")
			self.__file.write(str(len(graph.get_nodes()))+"\n");
			for i in graph.get_nodes():
				self.__file.write(str(i.get_id())+"\n")
				self.__file.write(str(i.get_label())+"\n")
				pos = i.get_position()
				self.__file.write(str(pos[0])+"\n")
				self.__file.write(str(pos[1])+"\n")
				color = i.get_color()
				self.__file.write(str(color[0])+"\n")
				self.__file.write(str(color[1])+"\n")
				self.__file.write(str(color[2])+"\n")
				self.__file.write(str(i.get_size())+"\n")
				self.__file.write(str(i.get_shape())+"\n")
			self.__file.write(str(len(graph.get_edges()))+"\n")
			for i in graph.get_edges():
				self.__file.write(str(i.get_weight())+"\n")
				connection = i.get_connection()
				self.__file.write(str(connection[0])+"\n")
				self.__file.write(str(connection[1])+"\n")
				color = i.get_color()
				self.__file.write(str(color[0])+"\n")
				self.__file.write(str(color[1])+"\n")
				self.__file.write(str(color[2])+"\n")
				self.__file.write(str(i.get_tam())+"\n")
				self.__file.write(str(i.get_form())+"\n")
			self.__file.close()
			self.__state = False


	#
	#  DATA MANAGEMENT
	#