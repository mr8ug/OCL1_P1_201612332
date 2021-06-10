from parser.Excepcion import Excepcion
from abstract.Instruccion import Instruccion
from parser.Simbolo import Simbolo

class Asignacion(Instruccion):
    def __init__(self, identificador, expresion, fila, columna):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpreter(self, tree, table):
        value = self.expresion.interpreter(tree, table)
        if isinstance(value, Excepcion): return value

        simbolo = Simbolo(self.identificador, self.expresion, self.fila, self.columna, value)

        result = table.actualizarTabla(simbolo)
        
        if isinstance(result, Excepcion): return result
        return  None