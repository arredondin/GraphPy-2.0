from gi.repository import Gtk

class HelpUi:

	def __init__(self):
		"""CONSTRUCTOR"""
		self.__builder = Gtk.Builder();
		self.__builder.add_from_file("helpBox/ui/helpui.ui")
		self.__window = self.__builder.get_object("helpWindow")
		self.__textView = self.__builder.get_object("textoAyuda")
		self.__themes = self.__builder.get_object("temas")
		self.__builder.connect_signals(self)
		self.init_chooser()

	def init_chooser(self):
		"""METODO INICIALIZA EL MENU DE TEMAS A PARTIR DE UN LIST STORE"""
		store=Gtk.ListStore(str,str)
		store.append(["Nuevos nodos","nodos.txt"])
		store.append(["Nuevas Conexiones","aristas.txt"])
		store.append(["Cambiar Etiquta Nodos y Etiquetas","etiquetas.txt"])
		store.append(["Mover Nodos","mover.txt"])
		store.append(["Algoritmos","algoritmos.txt"])
		self.__themes.set_model(store)
		texto = Gtk.CellRendererText()
		self.__themes.pack_start(texto,True)
		self.__themes.add_attribute(texto,"text",0)
		self.__themes.set_active(0)

	def get_content(self, nameHelp):
		file = open("helpBox/helps/"+nameHelp,"r")
		str = ""
		for i in file.readlines():
			str += i;
		self.load_content(str)

	def load_content(self, content):
		buffer = self.__textView.get_buffer()
		buffer.set_text(content)
		self.__textView.set_buffer(buffer)

	def throw_help(self):
		self.__window.show_all()

	def on_close_btn(self,widget,data=None):
		self.__window.destroy()

	def on_change(self, widget, data = None):
		store = widget.get_model()
		select = widget.get_active()
		self.get_content(store[select][1])