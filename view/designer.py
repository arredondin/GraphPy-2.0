import math
import random
import time
import cairo
from gi.repository import Gtk,Gdk
import copy
from PIL import Image

class Designer:
	"""Se encarga de Dibujar el Grafo en la Vista drawArea"""
	
	def __init__(self, drawArea):
		"""Constructor de Designer, recibe el area donde se puede Dibujar"""
		self.__drawArea = drawArea
		self.__connect_signals_draw()
		self.__status = 1 		# Status del Menu Lateral
		self.__sf = None
		self.__cntx = None
		self.__net = True
		
		# Variables de Seleccion
		self.__selected = 0
		self.__tmpSelection = None
		self.__temp = []
		self.__frameInicio = (0,0) 
		self.__frameFinal = (0,0)
		self.__deltaI = (0,0)
		self.__deltaF = (0,0)
	
	#
	#  PRIVATE METHODS
	#
	
	def __connect_signals_draw(self):
		"""Conecta las Seniales de los Eventos"""
		self.__drawArea.connect("draw",self.repaint)
		self.__drawArea.add_events(Gdk.ModifierType.BUTTON1_MASK)
		self.__drawArea.add_events(Gdk.EventMask.BUTTON1_MOTION_MASK)
		self.__drawArea.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
	
	def __draw(self, grafos, edges, printer = False):
		"""Dibuja en Pantalla o en Archivo el Grafo que se esta Creando"""
			self.__sf=cairo.ImageSurface(cairo.FORMAT_ARGB32,740,500)
			self.__drawArea.queue_draw()
		if printer == False:
			self.__cntx = cairo.Context(self.__sf)
		self.__cntx.set_source_rgb(1,1,1)
		self.__cntx.rectangle(0,0, 740, 500)
		self.__cntx.fill()
		if self.__net == True :
			self.__cntx.set_source_surface(cairo.ImageSurface.create_from_png("view/cuadricula.png"))
			self.__cntx.paint()
		for i in self.__graph.get_edges():
			self.__cntx.set_source_rgb(i.get_color()[0], i.get_color()[1], i.get_color()[2])
			tmpx1 = self.__graph.get_node(i.get_connection()[0]).get_position()[0]
			tmpy1 = self.__graph.get_node(i.get_connection()[0]).get_position()[1]
			tmpx2 = self.__graph.get_node(i.get_connection()[1]).get_position()[0]
			tmpy2 = self.__graph.get_node(i.get_connection()[1]).get_position()[1]

			self.__cntx.move_to(tmpx1,tmpy1)
			self.__cntx.set_line_width(i.get_tam())
			if i.get_form() == 1:
				self.__cntx.line_to(tmpx2,tmpy2)	
			if i.get_form() == 2:
				self.__cntx.set_dash([i.get_tam()*2,10], 0);
				self.__cntx.line_to(tmpx2,tmpy2)	
			if i.get_form() == 3:
				self.__cntx.set_dash([i.get_tam()*4, 10], 0);
				self.__cntx.line_to(tmpx2,tmpy2)	
			if i.get_form() == 4: 
				self.__cntx.set_dash([i.get_tam(),i.get_tam()], 2);
				self.__cntx.line_to(tmpx2,tmpy2)	
			if i.get_directed() == True:
				#self.__cntx.move_to((tmpx1+tmpx2)/2, (tmpy1+tmpy2)/2)
				arrow_len = i.get_tam()+30
				angle = math.atan2(tmpy2 - tmpy1, tmpx2 - tmpx1) + math.pi
				x1 = tmpx2 + arrow_len * math.cos(angle - 75)
				y1 = tmpy2 + arrow_len * math.sin(angle - 75)
				x2 = tmpx2 + arrow_len * math.cos(angle + 75)
				y2 = tmpy2 + arrow_len * math.sin(angle + 75)
				self.__cntx.move_to(tmpx2,tmpy2)
				self.__cntx.line_to(x1,y1)
				self.__cntx.stroke()
				self.__cntx.move_to(tmpx2,tmpy2)
				self.__cntx.line_to(x2,y2)
				self.__cntx.stroke()
				self.__cntx.move_to((x2+x1)/2, (y2+y1)/2)
			else:
				self.__cntx.move_to(((tmpx1+tmpx2)/2)+i.get_tam()+10,((tmpy1+tmpy2)/2)+i.get_tam()+10)
			self.__cntx.show_text(str(i.get_label()))
			self.__cntx.stroke()
		for i in self.__graph.get_nodes():
			self.__cntx.set_source_rgb(i.get_color()[0], i.get_color()[1], i.get_color()[2])
			if i.get_form() == 1:
				self.__cntx.arc(i.get_position()[0],i.get_position()[1], i.get_tam(), 0, 2*math.pi)
				self.__cntx.fill()
			if i.get_form() == 2:
				self.__cntx.rectangle(i.get_position()[0]-i.get_tam(), i.get_position()[1]-i.get_tam(),i.get_tam()*2,i.get_tam()*2)
				self.__cntx.fill()
			self.__cntx.move_to(i.get_position()[0]+i.get_tam(),i.get_position()[1]-i.get_tam())
			self.__cntx.show_text(i.get_label())
		if self.__selected == 2:
			self.__cntx.set_source_rgba 0, 255, 0.3)
			self.__change_delta()
			tmpx = self.__frameFinal[0] - self.__frameInicio[0]
			tmpy = self.__frameFinal[1] - self.__frameInicio[1]
			self.__cntx.rectangle(self.__frameInicio[0], self.__frameInicio[1], tmpx, tmpy)
			self.__cntx.fill()
		return self.__sf

	def __over_nodes(self,x ,y ):
		"""Obtiene el Nodo que esta en la Posicion x,y"""
		for i in self.__graph.get_nodes():
			if i.get_form() == 1:
				resultado = (x-i.get_position()[0])*(x-i.get_position()[0]) + (y-i.get_position()[1])*(y-i.get_position()[1])
				if resultado <= (i.get_tam())*(i.get_tam()):
					return i
			if i.get_form() == 2:
				if x >= i.get_position()[0]-i.get_tam()/2 and x <= i.get_position()[0]+i.get_tam()/2:
					if y >= i.get_position()[1]-i.get_tam()/2 and y <= i.get_position()[1]+i.get_tam()/2:
						return i
		return False

	def __over_select(self):
		"""Agrega a una Lista todos los nodos que estan sobre un Area Seleccionada"""
		for i in self.__graph.get_nodes():
			pos = i.get_position()
			if(pos[0] >= self.__frameInicio[0] and pos[0] <= self.__frameFinal[0]):
				if(pos[1] >= self.__frameInicio[1] and pos[1] <= self.__frameFinal[1]):
					self.__temp.insert(len(self.__temp), i)
	
	def __over_edge(self, x, y ):
		"""Funcion que obtiene el Arco que esta sobre el punto x,y"""
		for i in self.__graph.get_edges():
			id_nodos = i.get_connection()
			for j in self.__graph.get_nodes():
				if j.get_id() == id_nodos[0]:
					tmpInicio = j.get_position()
				if j.get_id() == id_nodos[1]:
					tmpFinal = j.get_position()
			pend = ( tmpInicio[1] - tmpFinal[1] )/( tmpInicio[0] - tmpFinal[0])
			resultado = (pend*(x - tmpInicio[0]))-(y - tmpInicio[1])
			if resultado <= i.get_tam() and resultado >= -i.get_tam():
				if tmpInicio[0] < x and tmpFinal[0] > x:
					return i
				if tmpFinal[0] < x and tmpInicio[0] > x:
					return i
		return False
	
	def __selectMove(self, data=None):
		"""Mueve todos los nodos que estan en la lista de seleccionados"""
		for i in self.__temp:
			i.set_position((i.get_position()[0]+(data.x - self.__deltaI[0]),i.get_position()[1]+(data.y - self.__deltaI[1])))
	
	def __change_delta(self):
		"""Funcion que cambia deltas del area de seleccion"""
		x, y = self.__frameInicio
		w, z = self.__frameFinal
		if w < x:
			aux = w
			w = x
			x = aux
		aux = z
		z = y
		y = aux
		self.__frameInicio = (x,y)
		self.__frameFinal = (w,z) 	
	
	#
	#  PUBLIC METHODS
	#
	
	def get_context(self):
		"""Obtiene el Area de Dibujo"""
		return cairo.Context(self.__sf)
	
	def get_graph(self):
		"""Obtiene una Copia del Grafo"""
		return copy.deepcopy(self.__graph)
	
	def set_status(self, newStatus):
		"""Cambia el estado de Designer:
		1.- Crear Nodo
		2.- Cursor
		3.- Crear Arista
		4.- Seleccionar (mover, copiar y pegar)"""
		self.__tmpSelection = None
		self.__status = newStatus
	
	def get_status(self):
		"""Obtiene el Estado de Designer"""
		return self.__status
	
	def set_graph( self, newGraph):
		"""Funcion que asigna un nuevo grafo al grafo actual
		OBS: se utiliza para botones rehacer y deshacer"""
		self.__graph = copy.deepcopy(newGraph)
		print "seteando grafo",self.__graph
		self.__drawArea.queue_draw()
	
	def get_selected(self):
		"""Obtiene un valor que indica si se esta Seleccionando un Area (1)
		y si no se esta seleccionando (0)"""
		return self.__selected
	
	def set_malla(self):
		"""Asigna a Designer si en la vista se quiere ver una malla de Ayuda en el Dibujo
		TRUE or FALSE"""
		self.__net = newState
	
	def select_area(self, data=None):
		"""Funcion que setea el punto de inicio del area de seleccion
		y ademas sirve para obtener el punto de inicio del delta de Movimiento"""
		if self.__selected == 0:
			self.__frameInicio = self.__drawArea.get_pointer()
			self.__selected = 2
		if self.__selected == 1:
			self.__deltaI = self.__drawArea.get_pointer()

	def select_area_end(self):
		"""Funcion que setea el punto final del area de seleccion"""
		self.__selected = 1
		self.__drawArea.queue_draw()

	def reset(self):
		"""Funcion que aplica un reset a variables que se utilizan de diferentes maneras
		en cada Estado de Designer"""
		print "reset"
		self.__selected = 0
		self.__tmpSelection = None
		del self.__temp[:]
	
	def move_node(self, data=None):
		"""Funcion que mueve un Nodo Seleccionado"""
		self.__tmpSelection = None
		if self.__over_nodes(data.x,data.y) != False:
			self.__over_nodes(data.x,data.y).set_position((data.x,data.y))
		self.__drawArea.queue_draw()
	
	def move_selected(self, data=None):
		"""Funcion que mueve todos los Nodos que se encuentran en un Area Seleccionada"""
		if self.__selected == 1:
			if self.__tmpSelection == None:
				self.__over_select()
				self.__tmpSelection = True
			self.__selectMove(data)
			self.__drawArea.queue_draw()
			self.__deltaI = (data.x, data.y)
	
	def get_node(self, x,y):
		"""Obtiene la Funcion over_nodes"""
		return self.__over_nodes(x,y)
	
	
	def get_edge(self, data):
		"""Funcion que invoca a over_edge"""
		return self.__over_edge(data.x, data.y)
	
	def repaint(self, widget, event):
		"""Funcion que redibuja el area, UTILIZADA POR EVENTOS"""
		self.canvas = widget.get_window().cairo_create()
		self.canvas.set_source_surface(self.__draw())
		self.canvas.paint()
	
	def redrawing(self):
		"""Funcion utilizada para aplicar cambios en la vista, redibuja el Area"""
		self.__drawArea.queue_draw()

	def create_file(self, direction, format):
		"""Funcion que especifica que tipo de archivo se desea exportar o guardar"""
		self.__folder = direction
		self.__format = format
		if(format == '.pdf'):
			self.__sf = cairo.PDFSurface(self.__folder + self.__format,740,500)	
		if(format == '.png'):
			self.__sf.write_to_png(self.__folder + self.__format)
		if(format == '.jpg' or format == '.gif'):
			self.__sf.write_to_png("tmp.png")
			Image.open("tmp.png").convert("RGB").save(self.__folder + self.__format)

	def get_over(self, data=None):
		"""Funcion que devuelve un valor al senialar en que posicion se encuentra el Mouse
		1.- Si esta en un Nodo
		2.- Si esta en una arista
		3.- Si esta en cualquier otra posicion"""
		if self.__over_nodes(data.x, data.y) != False:
			return 1
		if self.__over_edge(data.x, data.y) != False:
			return 2
		return 3

	def status_temp(self):
		self.__over_select()
		if len(self.__temp) != 0:
			return True
		else:
			return False

	def get_temp(self):
		return self.__temp
			
	def set_data(self):	
		self.__frameFinal = self.__drawArea.get_pointer()
		self.__drawArea.queue_draw()		
	
	def draw_extern(self, surface):
		self.__cntx = surface
		self.__draw(False, False, False, False, True)
		return self.__cntx
