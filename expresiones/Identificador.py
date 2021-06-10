from parser.Excepcion import Excepcion
from abstract.Instruccion import Instruccion

class Identificador(Instruccion):
    def __init__(self, identificador, fila, columna):
        self.identificador=identificador
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpreter(self, tree, table):
        simbolo = table.getTabla(self.identificador.lower())

        if simbolo == None:
            return Excepcion("Semantico", "Variable "+ self.identificador  + " no encontrada.", self.fila, self.columna )

        self.tipo = simbolo.getTipo()

        return simbolo.getValor()