from abstract.Instruccion import Instruccion
from parser.Excepcion import Excepcion
from parser.Tipo import TIPO

class Imprimir(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpreter(self, tree, table):
        value = super().interpreter(tree, table)

        if isinstance(value, Excepcion):
            return value
        if self.expresion.tipo == TIPO.ARREGLO:
            return Excepcion("Semantico", "No se puede imprimir un arreglo completo", self.fila, self.columna)

        tree.updateConsola(value)
        return None
