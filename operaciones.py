from enum import Enum

class OPERACION_ARITMETICA(Enum) :
    MAS = 1
    MENOS = 2
    ASTERISCO = 3
    DIVIDIDO = 4
    MODULO = 5
    ELEVADO = 6

class OPERACION_LOGICA(Enum) :
    AND = 1
    OR = 2
    MAYORQUE = 3
    MENORQUE = 4
    MAYORIWAL = 5
    MENORIWAL = 6
    IWAL = 7
    DISTINTO = 8

# Numeros -------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

class Expnum:
    pass


class OPBinaria(Expnum) :
    def __init__(self, term1, operador, term2) :
        self.term1 = term1
        self.term2 = term2
        self.operador = operador

class OPNeg(Expnum) :

    def __init__(self, term) :
        self.term = term

class OPNativa(Expnum) : #log10, sin, cos, tan, sqrt

    def __init__(self, term, tipo) :
        self.term = term
        self.tipo = tipo

class OPNativaLog(Expnum) : #log10, sin, cos, tan, sqrt

    def __init__(self, term1, term2) :
        self.term1 = term1
        self.term2 = term2

class OPArray(Expnum) :

    def __init__(self, val = []) :
        self.val = val

class OPNum(Expnum) :

    def __init__(self, val = 0) :
        self.val = val

# Cadenas -------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

class ExpCadena:
    pass

class OPMergeString(ExpCadena) :

    def __init__(self, term1, term2) :
        self.term1 = term1
        self.term2 = term2

class OPElevarString(ExpCadena) :

    def __init__(self, term1, term2) :
        self.term1 = term1
        self.term2 = term2

class OPUppercase(ExpCadena) :

    def __init__(self, term1) :
        self.term1 = term1

class OPLowercase(ExpCadena) :

    def __init__(self, term1) :
        self.term1 = term1

class OPLength(ExpCadena) : #este está tentativo acá

    def __init__(self, term1) :
        self.term1 = term1


class OPCadena(ExpCadena) :

    def __init__(self, id = "") :
        self.id = id


# Bool ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

class ExpBool:
    pass

class OPBool(ExpBool) : #si viene un id, de qué hereda? :c

    def __init__(self, id = True) :
        self.id = id


# Otros ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------------


class OPLogica() :
    def __init__(self, term1, operador, term2) :
        self.term1 = term1
        self.term2 = term2
        self.operador = operador

class OPID(Expnum) : #si viene un id, de qué hereda? :c

    def __init__(self, id = "") :
        self.id = id