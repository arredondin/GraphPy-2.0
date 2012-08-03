try:
	from gi.repository import Gtk, Gdk
except:
	print "DEPENCENCIAS INSATIFECHAS:  >= GTK3 "
	print "CORRIENDO CON GTK 2.X ... PUEDEN HABER PROBLEMAS"
	try:
		import gtk
	except:
		print "GTK NO DISPONIBLE EN TU SISTEMA"
		exit(1)

import designer
import string
import random
import time

class Ui:

	def __init__(self, graph):

		self.__loader = Gtk.Builder()
		self.__loader.add_from_file("view/view_model/ventanas.ui")
		self.__mainWindow = self.__loader.get_object("principal")
		self.__darea = self.__loader.get_object("workstation")
		self.__exportWindow = self.__loader.get_object("export")
		self.__statusBar = self.__loader.get_object("statusbar1")
		self.__menuGrafo = self.__loader.get_object("menu-grafo")
		self.__menuNodo = self.__loader.get_object("menu-nodo")
		self.__menuArista = self.__loader.get_object("menu-arista")
		self.__labelWindow = self.__loader.get_object("get-label")
		self.__sizeWindow = self.__loader.get_object("get-size")
		self.__menuColor = self.__loader.get_object("color")
		self.__menuCoordenates = self.__loader.get_object("coordenadas")
		self.__menuTamanio = self.__loader.get_object("tamanio")
		self.__menuFormaNodo = self.__loader.get_object("forma-nodo")
		self.__menuFormaArista = self.__loader.get_object("forma-arista")
		self.__menuMatriz = self.__loader.get_object("matriz")
		self.__menuAlert = self.__loader.get_object("algoritmos")
		self.__printWindow = self.__loader.get_object("printdialog")
		self.__pageSetup = self.__loader.get_object("pagesetupdialog")
		self.__defineType = self.__loader.get_object("tipo-grafo")
		self.__optionEditNode = self.__loader.get_object("show-nodes")
		self.__optionEditEdge = self.__loader.get_object("show-edges")
		self.__editNode = self.__loader.get_object("edita-nodo")
		self.__editEdge = self.__loader.get_object("edita-arista")
		self.__exit = self.__loader.get_object("exit")
		self.__draw = designer.Designer(self.__darea, graph)
	
	def connect_signals(self,controller):
		self.__loader.connect_signals(controller)

	def show_elements(self):
		self.__mainWindow.show()
		self.__defineType.show()
	
	def change_operation(self, opId, string):
		self.__draw.set_status(opId)
		self.__statusBar.push(0, string)
		self.__draw.reset()
			
	def throw_ui(self):
		self.show_elements()
		Gtk.main()

	def show_window_export(self):
		self.__exportWindow.show()

	def show_exit(self):
		self.__exit.show()
	
	def hide_exit(self):
		self.__exit.hide()
	
	def hide_option_Edit(self):
		self.__optionEditEdge.hide()
		self.__optionEditNode.hide()
		
	def save_and_exit(self):
		pass

	def show_print(self):
		self.__printWindow = Gtk.PrintOperation()
		self.__printWindow.set_n_pages(1)
		self.__printWindow.connect("draw_page", self.__printArea)
		res = self.__printWindow.run(Gtk.PrintOperationAction.PRINT_DIALOG, self.__mainWindow)
		return

	def __printArea(self, operation=None, context=None, page_nr=None):
		contexted = context.get_cairo_context()
		self.__cairo_context = self.__draw.draw_extern(contexted)
		return

	def to_pdf(self):
		self.__direction = self.__exportWindow.get_filename()
		if self.__direction == None:
			self.__exportWindow.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
		else:
			self.__formatExport = self.__loader.get_object("formato").get_active_text()
			print self.__formatExport
			self.__draw.create_file(self.__direction, self.__formatExport)
			self.__exportWindow.hide()
		
	def stop_ui(self):
		Gtk.main_quit()

	def destroy_export(self):
		self.__exportWindow.hide()

	def insert_new_node(self,data):
		self.__draw.insert_new_node(data)

	def get_over_node(self,data):
		return self.__draw.get_node(data.x,data.y)

	def get_draw_status(self):
		return self.__draw.get_status()

	def call_popup(self,data, valor):
		if valor == 1:
			self.__tmp = self.__draw.get_node(data.x, data.y)
			self.__menuNodo.popup(None, None, None, None, data.button, data.time)
		if valor == 2:
			self.__tmp = self.__draw.get_edge(data)
			self.__menuArista.popup(None, None, None, None, data.button, data.time)
		if valor == 3:
			self.__menuGrafo.popup(None, None, None, None, data.button, data.time)

	def get_draw_over(self,data):
		return self.__draw.get_over(data)

	def get_draw_selected(self):
		return self.__draw.get_selected()

	def get_draw_graph(self):
		return self.__draw.get_graph()

	def set_draw_graph(self,graph):
		self.__draw.set_graph(graph)

	def select_area(self,data):
		self.__draw.select_area(data)

	def select_area_end(self):
		self.__draw.select_area_end()
		return True

	def move_selected(self,data):
		self.__draw.move_selected(data)

	def move_node(self,data):
		self.__draw.move_node(data)

	def reset(self):
		self.__draw.reset()

	def show_label_node(self):
		self.__labelText = self.__loader.get_object("label-nodo")
		self.__labelText.set_text(str(self.__tmp.get_label()))
		self.__labelWindow.show()

	def show_label_edge(self):
		self.__sizeText = self.__loader.get_object("label-edge")
		self.__sizeText.set_text(str(self.__tmp.get_weight()))
		self.__sizeWindow.show()

	def set_new_label_node(self):
		self.__tmp.set_label(self.__labelText.get_text())
		self.__draw.redrawing()
		self.__labelText.set_text("")
		self.__labelWindow.hide()
		self.__tmp = False
		self.__draw.reset()

	def set_new_label_edge(self, grafo, viewgraph):
		self.__tmp.set_weight(self.__sizeText.get_text())
		if viewgraph.get_type():
			grafo.add_edge_dir(viewgraph.get_position_node(self.__tmp.get_connection()[0]),viewgraph.get_position_node(self.__tmp.get_connection()[1]),int(self.__tmp.get_weight()))
		else:
			grafo.add_edge_ndir(viewgraph.get_position_node(self.__tmp.get_connection()[0]),viewgraph.get_position_node(self.__tmp.get_connection()[1]),int(self.__tmp.get_weight()))
		self.__draw.redrawing()
		self.__sizeText.set_text("")
		self.__sizeWindow.hide()
		self.__tmp = False
		self.__draw.reset()

	def show_color(self):
		self.__menuColor.show()
		self.__selectColor = self.__loader.get_object("colorselection")

	def set_new_color(self):
		tmp = self.__selectColor.get_current_rgba()
		print tmp
		self.__tmp.set_color((tmp.red, tmp.green, tmp.blue))
		self.__draw.redrawing()
		self.__menuColor.hide()
		self.__tmp = False
		self.__draw.reset()

	def del_nodo(self, grafo):
		pos = grafo.get_position_node(self.__tmp.get_id())
		grafo.del_node(self.__tmp.get_id())
		return pos

	def del_edge(self, grafo):
		pos1 = self.__tmp.get_connection()[0]
		pos2 = self.__tmp.get_connection()[1]
		pos1 = grafo.get_position_node(pos1)
		pos2 = grafo.get_position_node(pos2)
		grafo.del_edge(self.__tmp.get_connection())
		self.__draw.redrawing()
		return pos1, pos2

	def set_malla(self, boolean):
		self.__draw.set_malla(boolean)
		self.__draw.redrawing()

	def show_coordenates(self):
		self.__coord_x = self.__loader.get_object("coord-x")
		self.__coord_x.set_text(str(self.__tmp.get_position()[0]))
		self.__coord_y = self.__loader.get_object("coord-y")
		self.__coord_y.set_text(str(self.__tmp.get_position()[1]))
		self.__menuCoordenates.show()

	def set_coordenates(self):
		print self.__tmp.get_position()
		self.__tmp.set_position((float(self.__coord_x.get_text()), float(self.__coord_y.get_text())))
		self.__draw.redrawing()
		self.__coord_x.set_text("")
		self.__coord_y.set_text("")
		self.__menuCoordenates.hide()
		self.__tmp = False
		self.__draw.reset()
 
 	def show_tamanio(self):
 		self.__tamanio = self.__loader.get_object("get-tam")
 		self.__tamanio.set_text(str(self.__tmp.get_size()))
 		self.__menuTamanio.show()

 	def set_tamanio(self):
 		self.__tmp.set_size(float(self.__tamanio.get_text()))
 		self.__draw.redrawing()
 		self.__tamanio.set_text("")
 		self.__menuTamanio.hide()
 		self.__tmp = False
 		self.__draw.reset()

 	def show_forma_nodo(self):
 		self.__forma = self.__loader.get_object("formas")
 		self.__menuFormaNodo.show()

 	def set_forma_nodo(self):
 		if self.__forma.get_active_text() == "Circulo":
 			self.__tmp.set_shape(1)
 		if self.__forma.get_active_text() == "Cuadrado":
 			self.__tmp.set_shape(2)
 		self.__draw.redrawing()
 		self.__menuFormaNodo.hide()
 		self.__tmp = False
 		self.__draw.reset()

 	def show_forma_arista(self):
 		self.__forma = self.__loader.get_object("formas_arista")
 		self.__menuFormaArista.show()

 	def set_forma_arista(self):
 		if self.__forma.get_active_text() == "Normal":
 			self.__tmp.set_shape(1)
 		if self.__forma.get_active_text() == "Segmentada 1":
 			self.__tmp.set_shape(2)
 		if self.__forma.get_active_text() == "Segmentada 2":
 			self.__tmp.set_shape(3)
 		if self.__forma.get_active_text() == "Punteada":
 			self.__tmp.set_shape(4)
 		self.__draw.redrawing()
 		self.__menuFormaArista.hide()
 		self.__tmp = False
 		self.__draw.reset()

 	def paste_selected(self, nodes, edges, viewgraph):
 		for i in nodes:
 			viewgraph.get_nodes().append(i)
 		for i in edges:
 			viewgraph.get_edges().append(i)
 		self.__draw.set_temp(nodes)
 		self.__draw.redrawing()
 		
 	def show_matriz(self, datos, grafo):
 		dim = datos.get_nodes()
 		matrix = datos.get_matrix()
 		self.__boxer = self.__loader.get_object("boxer")
 		self.__bufferText = Gtk.Grid()
 		self.__bufferText.set_row_spacing(dim)
 		self.__bufferText.set_column_spacing(dim)
 		for i in xrange(dim):
 			if str(grafo.get_node_for_position(i).get_label()) == "new":
 				label = Gtk.Label(str(grafo.get_node_for_position(i).get_label())+"-"+str(i))
 			else:
 				label = Gtk.Label(str(grafo.get_node_for_position(i).get_label())+"  ")
 			label.show()
 			self.__bufferText.attach(label,i+2,1,1, 1)
 		for i in xrange(dim):
 			if str(grafo.get_node_for_position(i).get_label()) == "new":
 				label = Gtk.Label(str(grafo.get_node_for_position(i).get_label())+"-"+str(i))
 			else:
 				label = Gtk.Label(str(grafo.get_node_for_position(i).get_label())+"  ")
 			label.show()
 			self.__bufferText.attach(label, 1, i+3, 1,1)
 			for j in xrange(dim):
 				label = Gtk.Label(str(matrix[i][j]))
 				label.show()
 				self.__bufferText.attach(label, j+2, i+3, 1,1)	
 		self.__boxer.pack_start(self.__bufferText, True, True, 0)
 		self.__boxer.reorder_child(self.__bufferText, 1) 
 		self.__bufferText.show() 		
 		self.__menuMatriz.show()

 	def hide_matriz(self, datos):
 		self.__bufferText.destroy()
 		self.__menuMatriz.hide()

	def show_directed(self, grafo):
		self.__loader.get_object("titulo_algoritmo").set_text("Grafo Dirigido")
		if grafo.directed():
 			self.__loader.get_object("resultado").set_text("El Grafo es Dirigido")
 		else:
 			self.__loader.get_object("resultado").set_text("El Grafo No es Dirigido")
 		self.__menuAlert.show()
	
	def show_grades(self, grafo):
		self.__loader.get_object("titulo_algoritmo").set_text("Lista de Grados")
		nodes = grafo.get_nodes()
		texto = ""
		c = 0
		for i in xrange(nodes):
			texto = texto + "Nodo "+ str(c) + ": "+ str(grafo.get_degree(i)) + "\n"
			c += 1
		self.__loader.get_object("resultado").set_text(texto)
		self.__menuAlert.show()
	
	def show_complete(self, grafo):
		self.__loader.get_object("titulo_algoritmo").set_text("Grafo Completo")
		if grafo.complete():
			self.__loader.get_object("resultado").set_text("El Grafo si es Completo")
		else:
			self.__loader.get_object("resultado").set_text("El Grafo no es Completo")
		self.__menuAlert.show()
	
	def show_bipartite(self, grafo, viewgraph):
		self.__loader.get_object("titulo_algoritmo").set_text("Grafo Bipartito")
		if grafo.bipartite():
			self.__loader.get_object("resultado").set_text("El Grafo si es Bipartito")
			self.colored(grafo, viewgraph)
		else:
			self.__loader.get_object("resultado").set_text("El Grafo no es Bipartito")
		self.__menuAlert.show()
		
	def show_connected(self, grafo):
		self.__loader.get_object("titulo_algoritmo").set_text("Grafo Conexo")
		if grafo.connected()[0]:
			if grafo.connected()[1] == 'strongly connected':
				self.__loader.get_object("resultado").set_text("El Grafo es fuertemente Conexo")
			if grafo.connected()[1] == 'weakly connected':
				self.__loader.get_object("resultado").set_text("El Grafo es debilmente Conexo")
			if grafo.connected()[1] == 'connected':
				self.__loader.get_object("resultado").set_text("El Grafo es Conexo")
		else:
			self.__loader.get_object("resultado").set_text("El Grafo No es Conexo")
		self.__menuAlert.show()
		
	def show_euler(self, grafo, viewgraph):
		self.__loader.get_object("titulo_algoritmo").set_text("Algoritmo de Euler")
		if grafo.eulerian_paths() == None:
			self.__loader.get_object("resultado").set_text("El Grafo No tiene Caminos Elulerianos")
		else:
			matrix = grafo.eulerian_paths()
			dim1 = len(matrix)
			text = ""
			for i in xrange(dim1):
				text = text + "Camino " + str(i) + ": "
				dim2 = len(matrix[i])
				for j in xrange(dim2):
					text = text + viewgraph.get_node_for_position(int(matrix[i][j])).get_label() + " - "
				text = text + "\n"
			self.__loader.get_object("resultado").set_text(text)
		self.__menuAlert.show()			
	
	def show_hamilton(self, grafo, viewgraph):
		self.__loader.get_object("titulo_algoritmo").set_text("Algoritmo Hamiltoniano")
		if grafo.hamiltonian_paths() == None:
			self.__loader.get_object("resultado").set_text("El Grafo No posee Caminos Hamiltonianos")
		else:
			matrix = grafo.hamiltonian_paths()
			dim1 = len(matrix)
			text = ""
			for i in xrange(dim1):
				text = text + "Camino " + str(i) + ": "
				dim2 = len(matrix[i])
				for j in xrange(dim2):
					text = text + viewgraph.get_node_for_position(int(matrix[i][j])).get_label() + " - "
				text = text + "\n"
			self.__loader.get_object("resultado").set_text(text)
		self.__menuAlert.show()	
	
	def draw_complement(self, grafo, viewgraph):
		self.__loader.get_object("titulo_algoritmo").set_text("Grafo Completado")
		if grafo.get_complementary() == None:
			self.__loader.get_object("resultado").set_text("El Grafo No posee Complemento")
		else:
			matrix = grafo.get_complementary()
			dim1 = len(matrix)
			for i in xrange(dim1):
				dim2 = len(matrix[i])
				for j in xrange(dim2):
					if matrix[i][j] != 0:
						connection = (viewgraph.get_node_for_position(i).get_id(), viewgraph.get_node_for_position(j).get_id())
						viewgraph.new_edge(connection)
						viewgraph.get_edge(connection).set_color((0,0,1))
						self.__loader.get_object("resultado").set_text("Se ha completado el grafo en Pantalla")
 		self.__draw.redrawing()
 		self.__menuAlert.show()
		
	def show_complement(self, grafo, viewgraph):
		self.__loader.get_object("titulo_algoritmo").set_text("Complemento del Grafo")
		if grafo.get_complementary() == None:
			self.__loader.get_object("resultado").set_text("El Grafo No posee Complemento")
		else:
			matrix = grafo.get_complementary()
			dim1 = len(matrix)
			for i in xrange(dim1):
				dim2 = len(matrix[i])
				for j in xrange(dim2):
					connection = (viewgraph.get_node_for_position(i).get_id(), viewgraph.get_node_for_position(j).get_id())
					if matrix[i][j] != 0:
						viewgraph.new_edge(connection)
						viewgraph.get_edge(connection).set_color((0,0,1))
					else:
						viewgraph.del_edge(connection)
		self.__loader.get_object("resultado").set_text("Se ha dibujado el Complemento en Pantalla")
 		self.__draw.redrawing()
 		self.__menuAlert.show()
	
	def show_kruskal(self, grafo, viewgraph):
		self.__loader.get_object("titulo_algoritmo").set_text("Algoritmo Kruskal")	
		if grafo.kruskal() == None:
			self.__loader.get_object("resultado").set_text("No Existe Arbol Recubridor Minimo para este Grafo")
		else:
			matrix = grafo.kruskal()
			dim1 = len(matrix)
			for i in xrange(dim1):
				dim2 = len(matrix[i])
				for j in xrange(dim2):
					if matrix[i][j] != 0:
						id1 = viewgraph.get_node_for_position(i).get_id()
						id2 = viewgraph.get_node_for_position(j).get_id()
						if viewgraph.get_edge((id1,id2)) != False:
							viewgraph.get_edge((id1,id2)).set_color((0,0,1))
						else:
							viewgraph.get_edge((id2,id1)).set_color((0,0,1))
			self.__loader.get_object("resultado").set_text("Arbol Recubridor Minimo Resaltado en Pantalla")
 		self.__draw.redrawing()
 		self.__menuAlert.show()
	
	def show_dijkstra(self, grafo, viewgraph):
		self.__loader.get_object("titulo_algoritmo").set_text("Algoritmo Dijkstra")
		label = self.__tmp.get_label()
		iD = self.__tmp.get_id()
		pos = viewgraph.get_position_node(iD)
		print iD
		matrix = grafo.dijkstra(pos)
		if matrix == None:
			self.__loader.get_object("resultado").set_text("El Nodo Seleccionado no Cumple los requisitos por ponderacion")
		else:
			dim1 = len(matrix)
			text = ""
			for i in xrange(dim1):
				text = text + "De " + label + " " + str(pos) + " a " + viewgraph.get_node_for_position(i).get_label() + " " + str(i) + ": "
				if matrix[i] != None:
					dim2 = len(matrix[i])
					for j in xrange(dim2):
						text = text + viewgraph.get_node_for_position(int(matrix[i][j])).get_label() + "-" + str(matrix[i][j]) + ""
				else:
					text = text + "No hay Camino Especifico"
				text = text + "\n"
			self.__loader.get_object("resultado").set_text(text)
		self.__menuAlert.show()	
		
	def hide_alert(self):
		self.__menuAlert.hide()
	
 	def set_data(self):
 		self.__draw.set_data()
 	
 	def get_draw(self):
 		return self.__draw
 		
 	def set_type(self):
 		if self.__loader.get_object("type").get_active_text() == "Dirigido":
 			self.__defineType.hide()
 			return True
 		else:
 			self.__defineType.hide()
 			return False
 	
 	def show_list_node(self, grafo):
 		self.__loader.get_object("title").set_text("Lista de Nodos")
 		for i in grafo.get_nodes():
 			self.__loader.get_object("listado").append(None, str(i.get_label())+"-"+str(i.get_id()))
 		self.__optionEditNode.show()
 		
 	def show_list_edge(self, grafo):
 		self.__loader.get_object("title1").set_text("Lista de Aristas")
 		for i in grafo.get_edges():
 			self.__loader.get_object("listado1").append(None, str(i.get_connection()[0])+","+str(i.get_connection()[1]))
 		self.__optionEditEdge.show()
 	
 	def show_all_node(self, grafo):
 		tmp = self.__loader.get_object("listado").get_active_text()
 		self.__tmp = grafo.get_node(float(tuple(string.split(tmp, "-"))[1]))
 		self.__loader.get_object("listado").remove_all()
 		self.__optionEditNode.hide()
 		self.__loader.get_object("coord_x").set_text(str(self.__tmp.get_position()[0]))
 		self.__loader.get_object("coord_y").set_text(str(self.__tmp.get_position()[1]))
 		self.__loader.get_object("newlabel").set_text(str(self.__tmp.get_label()))
 		self.__loader.get_object("newtamanio").set_text(str(self.__tmp.get_size()))
 		self.__editNode.show()
 		
 	def set_all_node(self, grafo):
 		x = float(self.__loader.get_object("coord_x").get_text())
 		y = float(self.__loader.get_object("coord_y").get_text())
 		self.__tmp.set_position((x,y))
 		if self.__loader.get_object("newshape").get_active_text() == "Circulo":
 			self.__tmp.set_shape(1)
 		if self.__loader.get_object("newshape").get_active_text() == "Cuadrado":
 			self.__tmp.set_shape(2)
 		self.__tmp.set_label(str(self.__loader.get_object("newlabel").get_text()))
 		self.__tmp.set_size(float(self.__loader.get_object("newtamanio").get_text()))
 		tmp = self.__loader.get_object("newcolor").get_current_rgba()
 		self.__tmp.set_color((tmp.red, tmp.green, tmp.blue))
 		self.__editNode.hide()
 		self.__draw.redrawing()
 	
 	def show_all_edge(self, grafo):
 		tmp = self.__loader.get_object("listado1").get_active_text()
 		self.__tmp = grafo.get_edge((float(tuple(string.split(tmp, ","))[0]), float(tuple(string.split(tmp, ","))[1])))
 		self.__loader.get_object("listado1").remove_all()
 		self.__optionEditEdge.hide()
 		self.__loader.get_object("newlabel1").set_text(str(self.__tmp.get_weight()))
 		self.__loader.get_object("newtamanio1").set_text(str(self.__tmp.get_size()))
 		self.__editEdge.show()
 		
 	def set_all_edge(self, grafo):
 		self.__tmp.set_weight(float(self.__loader.get_object("newlabel1").get_text()))
 		if self.__loader.get_object("newshape1").get_active_text() == "Normal":
 			self.__tmp.set_shape(1)
 		if self.__loader.get_object("newshape1").get_active_text() == "Segmentada 1":
 			self.__tmp.set_shape(2)
 		if self.__loader.get_object("newshape1").get_active_text() == "Segmentada 2":
 			self.__tmp.set_shape(3)
 		if self.__loader.get_object("newshape1").get_active_text() == "Punteada":
 			self.__tmp.set_shape(4)
 		self.__tmp.set_size(float(self.__loader.get_object("newtamanio1").get_text()))
 		tmp = self.__loader.get_object("newcolor1").get_current_rgba()
 		self.__tmp.set_color((tmp.red, tmp.green, tmp.blue))
 		self.__editEdge.hide()
 		self.__draw.redrawing()
 	
 	def colored(self, grafo, viewgraph):
 		array = grafo.color_graph()
 		dim1 = len(array)
 		color = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
 		for i in xrange(dim1):
 			newcolor = (color[random.randint(0,9)], color[random.randint(0,9)], color[random.randint(0,9)])
 			print newcolor
 			dim2 = len(array[i])
 			for j in xrange(dim2):
 				tmp = viewgraph.get_node_for_position(int(array[i][j]))
 				tmp.set_color(newcolor)
 		self.__draw.redrawing()
 	
 	def on_copy(self, viewgraph):
 		if self.__draw.get_status() == 4 and self.__draw.get_selected() == 1:
 			return self.__draw.get_list_selected()
 		else:
 			return False
 			
 	def set_new_position(self, nodes, edges):
 		for i in nodes:
 			i.set_position((i.get_position()[0]+20, i.get_position()[1]+20))
 			iD = i.get_id()
 			for j in edges:
 				if j.get_connection()[0] == iD:
 					tupla = j.get_connection()
 					j.set_connection((iD+100, tupla[1]))
 				if j.get_connection()[1] == iD:
 					tupla = j.get_connection()
 					j.set_connection((tupla[0], iD+100))
 			i.set_id(iD+100)
 			
 	def cut_repeat(self, nodes, edges, viewgraph):
 		if len(nodes) != 0:
 			for i in nodes:
 				viewgraph.del_node(i.get_id())
 		if len(edges) != 0:
 			for i in edges:
 				viewgraph.del_edge(i.get_connection())
 		self.__draw.set_graph(viewgraph)
 		
 	def show_dialog(self):
 		self.__aboutDialog = self.__loader.get_object("aboutdialog1")
 		self.__aboutDialog.show()
 	
 	def hide_dialog(self):
 		self.__aboutDialog.hide()
 	
 	def show_align(self):
 		self.__alignMenu = self.__loader.get_object("align-window")
 		self.__alignMenu.show()
 	
 	def align_graph(self, grafo):
 		if self.__loader.get_object("tipe-align").get_active_text() == "Matriz":
 			dim1 = len(grafo.get_nodes())
 			for i in xrange(dim1):
 				j = 0
 				while j < 4:
 					if (i*4+j) < dim1:
 						grafo.get_nodes()[i*4+j].set_position(((70*(j+1)), (70*(i+1))))
 					j = j+1
 		if self.__loader.get_object("tipe-align").get_active_text() == "Triangular":
 			dim1 = len(grafo.get_nodes())
 			i = 0
 			cont = 0
 			while i < dim1:
 				j = 0
 				while j < (i+1):
 					if (i+j) < dim1:
 						grafo.get_nodes()[i+j].set_position(((70*(j+1)), (70*(cont+1))))
 					j = j+1					
 				cont= cont + 1
 				i = i + j 					
 		self.__alignMenu.hide()
 		self.__draw.set_graph(grafo)

 	def repaint_from_controller(self,graph):
 		self.__draw.set_graph(graph)
 		
 	def get_file_to_save(self):
 		return self.__openWindow.get_filename()
 	
 	def show_open(self):
 		self.__openWindow = self.__loader.get_object("openFile")
 		self.__filter = Gtk.FileFilter()
 		self.__filter.add_pattern("*.gpy")
 		self.__openWindow.set_filter(self.__filter)
 		self.__openWindow.show()
 	
 	def hide_open(self):
 		self.__openWindow.hide()


 	def get_directory_save(self):
 		return  self.__saveWindow.get_filename()
 	
 	def show_save(self):
 		self.__saveWindow = self.__loader.get_object("saveFile")
 		self.__saveWindow.show()
 	
 	def hide_save(self):
 		self.__saveWindow.hide()

 		
