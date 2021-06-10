from parser.Excepcion import Excepcion
from abstract.Instruccion import Instruccion
from parser.Simbolo import Simbolo

class Declaracion(Instruccion):
    def __init__(self, tipo, indentificador, fila, columna, expresion=None):
        self.identificador = indentificador
        self.tipo = tipo
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpreter(self, tree, table):
        value = self.expresion.interpreter(tree, table)
        if isinstance(value, Excepcion): return value

        if self.tipo != self.expresion.tipo:
            return Excepcion("Semantico", "Tipo de dato diferente en Declaracion", self.fila, self.columna)

        simbol = Simbolo(str(self.identificador), self.tipo, self.fila, self.columna, value)

        result = table.setTabla(simbol)

        if isinstance(result, Excepcion): return result
        return None