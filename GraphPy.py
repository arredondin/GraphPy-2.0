#!/usr/bin/python2

import controller

def main():
	print 'Iniciando GraphPy utilizando el interprete local de python'
	print '...'
	GraphPy = controller.Controller()
	GraphPy.throw_app()
	print 'GraphPy se ha ejecutado correctamente'

if __name__ == "__main__":
    main()
