# ----------------------------------------------------------------------------------------------------- 
#---------------------------------------- INICIO SEMÁNTICO --------------------------------------------
# -----------------------------------------------------------------------------------------------------

from cst import Nodo

grafo = ""
contador = 0

#  --------------------------------COSOS DE MUESTRA--------------------------------------------------
#----------------------------------------------------------------------------------------------------

def incrementarContador():
    global contador
    contador = contador +1
    return str(contador)

class produccion(Nodo):

    def __init__(self, nombre): # el constructor va en plan self, hijo 1, hijo2 ... nombre
        self.name = nombre

    def imprimir():
        self.son1.imprimir()

    def traducir(self):
        global grafo
        id = incrementarContador()
        return id