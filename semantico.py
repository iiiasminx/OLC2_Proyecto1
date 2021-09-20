# ----------------------------------------------------------------------------------------------------- 
#---------------------------------------- INICIO SEMÁNTICO --------------------------------------------
# -----------------------------------------------------------------------------------------------------
from cst import NodoSimbolo

txt = ""
contador = 0


#para el semántico
contascope = 0
condicion = True
asignaciones = []
cambios = []

def incrementarscope():
    global contascope
    contascope += 1
    return contascope

class Nodo:
    pass #no contiene nada pero tengo que heredar de acá 

#  -----------------------------------INSTRUCCIONES--------------------------------------------------
#----------------------------------------------------------------------------------------------------

#el plan general es tener un array de instrucciones de modo tipo_instruccion, scope, *params
#el tipo instruccion es un switch case, donde 1 es print, 2 if ...
#el scope es un contador, donde entre mas anidado esté, peor gg entonces si una funcion es false, 
#solo sigo recorriendo el array hasta que el scope sea uno mas

class Instruccion:

    id = 0
    def __init__(self, tipo: int, scope: int, parametros = []):
        self.tipo = tipo
        self.scope = scope
        self.parametros = parametros #los params son lo que necesito para interpretar
        #de acá termino con un objeto con tipo, scope y parpametros

class Impresion:
    def __init__(self, scope, parametros):
        self.scope = scope
        self.parametros = parametros


#  ------------------------------------------INICIO--------------------------------------------------
#----------------------------------------------------------------------------------------------------



class Semantico:

    pilahijos = []  #pila de arrays de nodos [[[], [],[]],[],[],[]] lista de listas if u may

    contador = 0
    pilaimpresion = []
    pilaAsignacion = []

    #Interpreta los padres en funcion de los ultimos datos en la pila de Hijos
    def interpretarPadres(self, posicion, instruccionPadre: Instruccion):
        posicion -= 1
        ultimoshijos = self.pilahijos.pop()
        
        if instruccionPadre.tipo == 3: #CAMBIAR ESTO, PERO SUPONTGAMOS QUE ES UN IF
            if instruccionPadre.parametros[0] == True:
                for hijo in ultimoshijos:
                    if hijo.tipo == 1 or hijo.tipo == 2: #si es un print o asignacion
                        self.interpretarhijos([hijo])


    #genra las operaciones planas Y las operaciones que ya están anidadas (?)
    #Este solo sirve para guardar las instrucciones, para saber que están allí. cuando esté 
    # interpretando padres, entoonces ya las interpreto
    def interpretarhijos(self, instrucciones = [] ): 

        hijos = []
        for instruccion in instrucciones: #por cada instruccion en lista de instrucciones
            
            #acá estoy metiendo la instruccion en la lista de hijos
            hijos.append(instruccion)              #lista de hijos del padre

            instruccion.id = self.contador

            self.contador += 1
        
        self.pilahijos.append(hijos) #pila de arrays de nodos [[],[],[],[]] lista de listas if u may


    #cada cosa entra acá cuando se termina de leer toda la instruccion
    #COMO ES TEXTO PLANO SE GUARDA EN EL DE LOS HIJOS
    def interpretar(self, instruccion: Instruccion):
        if instruccion.tipo == 1:
                self.pilaAsignacion.append(instruccion)
                print('asignacion')
        elif instruccion.tipo == 2:
                self.pilaimpresion.append(instruccion)
                print('impresion')


    def terminar(self):
        print('Pila de impresion', self.pilaimpresion)
        print('Pila de Asignaciones', self.pilaAsignacion)