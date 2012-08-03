from model import graph , algorithms
from view import gui
from helpBox import help
import datatypes
import copy

class Controller:
	"""Controlador del Sistema"""
	def __init__(self):
		self.__viewGraph = datatypes.Graph()
		self.__viewGraph.set_type(True)
		self.__modelGraph = graph.Graph(0)
		self.__view = gui.Ui(self.__viewGraph)
		self.__view.connect_signals(self)
		self.__areaSel = False
		self.__tmp = False 		#Variable Temporal que se utiliza para la arista
		
		self.__undo_stack = algorithms.Actions()
		self.__redo_stack = algorithms.Actions()
		
		self.__clipboard_nodes = None
		self.__clipboard_edges = None
		self.__option = 0
		
		self.__openBox = None
		self.__saveBox = None
		
		self.__saveStatus = False
		
	#
	#  PRIVATE METHODS
	#
	
	def __set_graph(self):
		"""Para un grafo 'g', obtenido desde view
		Sincroniza (solo inicialmente) el grafo de view con el grafo de model
		Retorna el nuevo grafo de model"""
		nodes = self.__viewGraph.get_nodes()
		edges = self.__viewGraph.get_edges()
		self.__modelGraph = graph.Graph( len(nodes) )
		for i in xrange( len(edges) ):
			origin = self.__viewGraph.get_position_node(edges[i].get_connection()[0])
			dest = self.__viewGraph.get_position_node(edges[i].get_connection()[1])
			weight = edges[i].get_weight()
			if self.__viewGraph.get_type():
				self.__modelGraph.add_edge_dir(origin, dest, weight)
			else:
				self.__modelGraph.add_edge_ndir(origin, dest, weight)
		
	#
	#  PUBLIC METHODS
	#
	
	def throw_app(self):
		self.__view.throw_ui()
	
	def on_close(self,widget,data=None):
		self.__view.stop_ui()
	
	def on_cursor(self, widget,data=None): #Accede al Cursor
		self.__view.change_operation(2, "Cursor")
		self.__areaSel = False
	
	def on_node(self,widget,data=None): #Accede a Crear el Nodo
		self.__view.change_operation(1, "Crear Nodos")
		self.__areaSel = False
	
	def on_add_edge(self, widget, data=None): #Accede a Crear el Arco
		self.__view.change_operation(3, "Crear Arista")
		self.__areaSel = False
	
	def on_select(self, widget, data=None): #Accede a Seleccion
		self.__view.change_operation(4, "Seleccionar Area")
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

	def on_redo(self,widget,data=None):
		tmp = self.__redo_stack.pop()
		print "deshaciendo en redo con grafo igual a ",tmp
		if tmp is not None:
			self.__undo_stack.push(copy.deepcopy(self.__viewGraph))
			self.__viewGraph= copy.deepcopy(tmp)
			self.__set_graph()
			self.__view.get_draw().set_graph(self.__viewGraph)

	def on_undo(self, widget, data=None):
		tmp = self.__undo_stack.pop()
		if tmp is not None:
			self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
			self.__viewGraph = copy.deepcopy(tmp)
			self.__set_graph()
			self.__view.get_draw().set_graph(self.__viewGraph)
	
	def option_clicked(self, data = None):
		if self.__view.get_draw_status() == 1:
			if data.button == 1:
				self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
				self.__viewGraph.new_node(data)
				self.__modelGraph.add_node()

		if self.__view.get_draw_status() == 2:
			#self.__redo_stack.push(copy.deepcopy(self.__view.get_draw_graph()))
			pass
			
		if self.__view.get_draw_status() == 3:
			if data.button == 1:
				if self.__tmp == False:
					self.__tmp = self.__view.get_over_node(data)
				else:
					other = self.__view.get_over_node(data)
					if other == False:
						self.__tmp = False
					else:
						if self.__tmp.get_id() == other.get_id():
							self.__tmp = False
						else:
							self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
							connection = (self.__tmp.get_id(), other.get_id())	
							self.__viewGraph.new_edge(connection)
							posi = self.__viewGraph.get_position_node(self.__tmp.get_id())
							posd = self.__viewGraph.get_position_node(other.get_id())
							if self.__viewGraph.get_type():
								self.__modelGraph.add_edge_dir(posi, posd, 1)
							else:
								self.__modelGraph.add_edge_ndir(posi,posd, 1)
							self.__tmp = False			

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
		self.__view.get_draw().set_graph(self.__viewGraph)

	def option_moved(self, data = None):
		if self.__view.get_draw_status() == 1:
			return True
		if self.__view.get_draw_status() == 2:
			self.__view.move_node(data)
		if self.__view.get_draw_status() == 3:
			return True
		if self.__view.get_draw_status() == 4:
			if self.__areaSel:
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
				if self.__view.get_draw_selected() == 2:
					self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
					self.__areaSel = self.__view.select_area_end()
		self.__view.get_draw().set_graph(self.__viewGraph)

	def del_nodo(self, widget, data = None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		pos = self.__view.del_nodo(self.__viewGraph) 
		print pos
		self.__modelGraph.del_node(pos)
		self.__view.get_draw().set_graph(self.__viewGraph)

	def del_edge(self, widget, data = None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		ni, nf = self.__view.del_edge(self.__viewGraph)
		self.__modelGraph.del_edge(ni,nf)
		self.__view.get_draw().set_graph(self.__viewGraph)

	def set_coordenates(self, widget, data=None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		self.__view.set_coordenates()
		self.__view.get_draw().set_graph(self.__viewGraph)

	def show_label_node(self, widget, data = None):
		self.__view.show_label_node()
	
	def show_label_edge(self, widget, data = None):
		self.__view.show_label_edge()

	def set_label_node(self, widget, data = None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		self.__view.set_new_label_node()
		self.__view.get_draw().set_graph(self.__viewGraph)
		
	def set_label_edge(self, widget, data = None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		self.__view.set_new_label_edge(self.__modelGraph, self.__viewGraph)
		self.__view.get_draw().set_graph(self.__viewGraph)

	def set_tamanio(self, widget, data=None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		self.__view.set_tamanio()
		self.__view.get_draw().set_graph(self.__viewGraph)

	def hide_label(self, widget, data = None):
		self.__view.hide_label()

	def show_color(self, widget, data = None):
		self.__view.show_color()

	def hide_color(self, widget, data = None):
		self.__view.hide_color()

	def set_color(self, widget, data = None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		self.__view.set_new_color()
		self.__view.get_draw().set_graph(self.__viewGraph)

	def set_forma_nodo(self, widget, data=None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		self.__view.set_forma_nodo()
		self.__view.get_draw().set_graph(self.__viewGraph)

	def set_forma_arista(self, widget, data=None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		self.__view.set_forma_arista()
		self.__view.get_draw().set_graph(self.__viewGraph)

	def show_malla(self, widget, data=None):
		self.__view.set_malla(widget.get_active())

	def show_coordenates(self, widget, data=None):
		self.__view.show_coordenates()

	def hide_coordenates(self, widget, data = None):
		self.__view.hide_coordenates()

	def show_tamanio(self, widget, data=None):
		self.__view.show_tamanio()

	def hide_tamanio(self, widget, data = None):
		self.__view.hide_tamanio()
		
	def show_forma_nodo(self, widget, data=None):
		self.__view.show_forma_nodo()

	def hide_forma_nodo(self, widget, data = None):
		self.__view.hide_forma_nodo()

	def show_forma_arista(self, widget, data=None):
		self.__view.show_forma_arista()

	def hide_forma_arista(self, widget, data = None):
		self.__view.hide_forma_arista()

	def show_matriz(self, widget, data=None):
		self.__view.show_matriz(self.__modelGraph, self.__viewGraph)
	
	def set_type(self, widget, data=None):
		self.__viewGraph.set_type(self.__view.set_type())
		
	def hide_matriz(self, widget, data=None):
		self.__view.hide_matriz(self.__modelGraph)
	
	def show_all_node(self, widget, data=None):
		self.__view.show_all_node(self.__viewGraph)
		
	def set_all_node(self, widget, data=None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		self.__view.set_all_node(self.__viewGraph)
	
	def show_list_node(self, widget, data=None):
		self.__view.show_list_node(self.__viewGraph)
	
	def show_list_edge(self, widget, data=None):
		self.__view.show_list_edge(self.__viewGraph)
	
	def show_all_edge(self, widget, data=None):
		self.__view.show_all_edge(self.__viewGraph)
		
	def set_all_edge(self, widget, data=None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		self.__view.set_all_edge(self.__viewGraph)
		
	def hide_alert(self, widget, data=None):
		self.__view.hide_alert()
	
	def show_directed(self, widget, data=None):
		self.__view.show_directed(self.__modelGraph)
	
	def show_grades(self, widget, data=None):
		self.__view.show_grades(self.__modelGraph)
		
	def show_complete(self, widget, data=None):
		self.__view.show_complete(self.__modelGraph)
	
	def show_bipartite(self, widget, data=None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		self.__view.show_bipartite(self.__modelGraph, self.__viewGraph)
	
	def show_connected(self, widget, data=None):
		self.__view.show_connected(self.__modelGraph)
	
	def show_euler(self, widget, data=None):
		self.__view.show_euler(self.__modelGraph, self.__viewGraph)
	
	def show_hamilton(self, widget, data=None):
		self.__view.show_hamilton(self.__modelGraph, self.__viewGraph)
	
	def show_draw_complement(self, widget, data=None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		self.__view.draw_complement(self.__modelGraph, self.__viewGraph)
		self.__set_graph()
	
	def show_complement(self, widget, data=None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		self.__view.show_complement(self.__modelGraph, self.__viewGraph)
		self.__set_graph()
	
	def show_dijkstra(self, widget, data=None):
		self.__view.show_dijkstra(self.__modelGraph, self.__viewGraph)
	
	def show_kruskal(self, widget, data=None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		self.__view.show_kruskal(self.__modelGraph, self.__viewGraph)
	
	def colored(self, widget, data=None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		self.__view.colored(self.__modelGraph, self.__viewGraph)

	def on_copy(self, widget, data=None):
		if self.__view.on_copy(self.__viewGraph) != False:
			self.__clipboard_nodes  = self.__view.on_copy(self.__viewGraph)[0]
			self.__clipboard_edges = self.__view.on_copy(self.__viewGraph)[1]
			self.__view.set_new_position(self.__clipboard_nodes, self.__clipboard_edges)
			self.__option = 1

	def on_cut(self, widget, data=None):
		if self.__view.on_copy(self.__viewGraph) != False:
			self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
			self.__clipboard_nodes  = self.__view.on_copy(self.__viewGraph)[0]
			self.__clipboard_edges = self.__view.on_copy(self.__viewGraph)[1]
			self.__view.cut_repeat(self.__clipboard_nodes, self.__clipboard_edges, self.__viewGraph)
			self.__set_graph()
			self.__option = 2

	def on_paste(self, widget, data=None):
		if self.__clipboard_edges != None and self.__clipboard_nodes != None:
			self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
			self.__view.paste_selected(self.__clipboard_nodes, self.__clipboard_edges, self.__viewGraph)
			self.__set_graph()
			if self.__option == 2:
				self.__clipboard_nodes = None
				self.__clipboard_edges = None
				
	
	def show_help(self, widget, data=None):
		helpPop = help.HelpUi()
		helpPop.throw_help() 
	
	def show_about(self, widget, data=None):
		self.__view.show_dialog()
	
	def hide_about(self, widget, data=None):
		self.__view.hide_dialog()
	
	def show_align(self, widget, data=None):
		self.__view.show_align()
	
	def align_graph(self, widget, data=None):
		self.__redo_stack.push(copy.deepcopy(self.__viewGraph))
		self.__view.align_graph(self.__viewGraph)
		
	def show_open(self, widget, data=None):
		self.__view.show_open()
	
	def hide_open(self, widget, data=None):
		self.__view.hide_open()
	
	def show_save(self, widget, data=None):
		self.__view.show_save()
	
	def hide_save(self, widget, data=None):
		self.__view.hide_save()
	