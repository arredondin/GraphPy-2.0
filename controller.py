from model import graph #, algorithms
from view import gui
import datatypes

class Controller:
	"""Controlador del Sistema"""
	def __init__(self):
		self.__view = gui.Ui()
		self.__view.connect_signals(self)
		self.__viewGraph = datatypes.Graph()
		self.__modelGraph = graph.Graph()
		self.__areaSel = False
		self.__typeGraph = False
		self.__tmp = 0 		#Variable Temporal que se utiliza para eso
	
	#
	#  PRIVATE METHODS
	#
	
	def __set_graph(self):
		"""Para un grafo 'g', obtenido desde view
		Sincroniza (solo inicialmente) el grafo de view con el grafo de model
		Retorna el nuevo grafo de model"""
		nodes = self.__viewGraph.get_nodes()
		edges = self.__viewGraph.get_edges()
		new = graph.Graph( len(nodes) )
		for i in range( len(edges) ):
			origin = edges[i].connections[0]
			dest = edges[i].connections[1]
			weight = edges[i].weight
			if g.get_directed():
				new.set_edge_dir(origin, dest, weight)
			else:
				new.set_edge_ndir(origin, dest, weight)
		return new
		
	#
	#  PUBLIC METHODS
	#
	
	def throw_app(self):
		self.__view.throw_ui()
	
	def on_close(self,widget,data=None):
		self.__view.stop_ui()
	
	def on_cursor(self, widget,data=None): #Accede al Cursor
		self.__view.change_operation(2)
		self.__areaSel = False
	
	def on_node(self,widget,data=None): #Accede a Crear el Nodo
		self.__view.change_operation(1)
		self.__areaSel = False
	
	def on_add_edge(self, widget, data=None): #Accede a Crear el Arco
		self.__view.change_operation(3)
		self.__areaSel = False
	
	def on_select(self, widget, data=None): #Accede a Seleccion
		self.__view.change_operation(4)
		self.__areaSel = False

	def on_to_pdf(self, widget, data=None):
		self.__view.show_window_export()

	def on_print(self, widget, data=None):
		self.__view.show_print()

	def on_export_clicked(self, widget, data=None):
		self.__view.to_pdf()

	def hide_export(self, widget, data=None):
		self.__view.destroy_export()

	def on_clicked(self, widget, data=None):
		self.option_clicked(data)

	def motion_clicked(self, widget, data=None):
		self.option_moved(data)

	def on_click_released(self, widget, data=None):
		self.option_released(data)

	"""	def on_redo(self,widget,data=None):
		tmp = self.__redo_stack.pop()
		print "deshaciendo en redo con grafo igual a ",tmp
		if tmp is not None:
			self.__undo_stack.push(copy.deepcopy(self.__view.get_draw_graph()))
			self.__view.set_draw_graph(copy.deepcopy(tmp))

	def on_undo(self, widget, data=None):
		tmp = self.__undo_stack.pop()
		if tmp is not None:
			self.__redo_stack.push(copy.deepcopy(self.__view.get_draw_graph()))
			self.__view.set_draw_graph(copy.deepcopy(tmp))  """
	
	def option_clicked(self, data = None):
		if self.__view.get_draw_status() == 1:
			if data.button == 1:
				#self.__redo_stack.push(self.__view.get_draw_graph())
				self.__viewGraph.new_node((data.x, data.y))
				self.__modelGraph.add_node()

		if self.__view.get_draw_status() == 2:
			#self.__redo_stack.push(copy.deepcopy(self.__view.get_draw_graph()))

		if self.__view.get_draw_status() == 3:
			if data.button == 1:
				if self.__tmp == 0:
					self.__view.insert_edge(data)
					self.__tmp += 1
				else:	
					#self.__redo_stack.push(self.__view.get_draw_graph())
					self.__view.insert_edge(data)
					self.__tmp = 0
			

		if self.__view.get_draw_status() == 4:
			if data.button == 1:
				if self.__areaSel == False:
					self.__view.set_data()
				self.__view.select_area(data)
			if data.button == 3:
				self.__view.reset()
				self.__areaSel = False

		if data.button == 3:
			if self.__view.get_draw_over(data) == 1:
				self.__view.call_popup(data, 1)
			if self.__view.get_draw_over(data) == 2:
				self.__view.call_popup(data, 2)
			if self.__view.get_draw_over(data) == 3: 
				self.__view.call_popup(data, 3)


	def option_moved(self, data = None):
		if self.__view.get_draw_status() == 1:
			return True
		if self.__view.get_draw_status() == 2:
			self.__view.move_node(data)
		if self.__view.get_draw_status() == 3:
			return True
		if self.__view.get_draw_status() == 4:
			if self.__areaSel == True:
				self.__view.move_selected(data)
			else:
				self.__view.set_data()

	def option_released(self, data = None):
		if self.__view.get_draw_status() == 1:
			return True
		if self.__view.get_draw_status() == 2:
			return True
		if self.__view.get_draw_status() == 3:
			return True
		if self.__view.get_draw_status() == 4:
			if data.button == 1:
				if self.__view.get_draw_ind() == 2:
					#self.__redo_stack.push(copy.deepcopy(self.__view.get_draw_graph()))
					self.__areaSel = self.__view.select_area_end()

	def show_label(self, widget, data = None):
		self.__view.show_label()

	def set_label(self, widget, data = None):
		#self.__redo_stack.push(copy.deepcopy(self.__view.get_draw_graph()))
		self.__view.set_new_label()

	def hide_label(self, widget, data = None):
		self.__view.hide_label()

	def show_color(self, widget, data = None):
		self.__view.show_color()

	def hide_color(self, widget, data = None):
		self.__view.hide_color()

	def set_color(self, widget, data = None):
		#self.__redo_stack.push(copy.deepcopy(self.__view.get_draw_graph()))
		self.__view.set_new_color()

	def del_nodo(self, widget, data = None):
		#self.__redo_stack.push(copy.deepcopy(self.__view.get_draw_graph()))
		pos = self.__view.del_nodo() 
		if pos != None:
			self.__graph.del_node(pos)

	def del_edge(self, widget, data = None):
		#self.__redo_stack.push(copy.deepcopy(self.__view.get_draw_graph()))
		self.__view.del_edge()

	def show_malla(self, widget, data=None):
		self.__view.set_malla(widget.get_active())

	def show_coordenates(self, widget, data=None):
		self.__view.show_coordenates()

	def hide_coordenates(self, widget, data = None):
		self.__view.hide_coordenates()

	def set_coordenates(self, widget, data=None):
		#self.__redo_stack.push(copy.deepcopy(self.__view.get_draw_graph()))
		self.__view.set_coordenates()

	def show_tamanio(self, widget, data=None):
		self.__view.show_tamanio()

	def hide_tamanio(self, widget, data = None):
		self.__view.hide_tamanio()

	def set_tamanio(self, widget, data=None):
		#self.__redo_stack.push(copy.deepcopy(self.__view.get_draw_graph()))
		self.__view.set_tamanio()

	def show_forma_nodo(self, widget, data=None):
		self.__view.show_forma_nodo()

	def hide_forma_nodo(self, widget, data = None):
		self.__view.hide_forma_nodo()

	def set_forma_nodo(self, widget, data=None):
		#self.__redo_stack.push(copy.deepcopy(self.__view.get_draw_graph()))
		self.__view.set_forma_nodo()

	def show_forma_arista(self, widget, data=None):
		self.__view.show_forma_arista()

	def hide_forma_arista(self, widget, data = None):
		self.__view.hide_forma_arista()

	def set_forma_arista(self, widget, data=None):
		#self.__redo_stack.push(copy.deepcopy(self.__view.get_draw_graph()))
		self.__view.set_forma_arista()

	def show_matriz(self, widget, data=None):
		self.__view.show_matriz(self.__graph)
