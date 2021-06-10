from abstract.Instruccion import Instruccion

class Primitivos(Instruccion):
    def __init__(self, tipo, valor, fila, columna):
        self.tipo=tipo
        self.valor=valor
        self.fila= fila
        self.columna = columna

    def interpreter(self, tree, table):
        return self.valor