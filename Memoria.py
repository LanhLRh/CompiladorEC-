import numpy
from Simbolos import *

#----------------- DIRECCIONES VIRTUALES -----------------------------

# Diccionario que dada una variable constante te regresa su direccion de memoria virtual
dirConstantes = {}

# registrosMem: Arreglo de contadores enteros. Cada casilla pertenece a un tipo de dato con determinado scope. El valor de la casilla apunta a una direccion libre.
registrosMem = numpy.zeros(16)

# Inicializando registrosMem.
# contadorReg: diccionario que dado un tipo y scope regresa el indice correspondiente. Se usa para facilidad de lectura en el codigo.
# posInicial: diccionario que guarda la primera posicion de memoria de cierto tipo y scope
# posLimite: diccionario que guarda la ultima posicion de memoria de cierto tipo y scope
registrosMem[contadorReg['intGlobal']] = posInicial['intGlobal']
registrosMem[contadorReg['decGlobal']] = posInicial['decGlobal']
registrosMem[contadorReg['stringGlobal']] = posInicial['stringGlobal']
registrosMem[contadorReg['booleanGlobal']] = posInicial['booleanGlobal']

registrosMem[contadorReg['intLocal']] = posInicial['intLocal']
registrosMem[contadorReg['decLocal']] = posInicial['decLocal']
registrosMem[contadorReg['stringLocal']] = posInicial['stringLocal']
registrosMem[contadorReg['booleanLocal']] = posInicial['booleanLocal']

registrosMem[contadorReg['intTemp']] = posInicial['intTemp']
registrosMem[contadorReg['decTemp']] = posInicial['decTemp']
registrosMem[contadorReg['stringTemp']] = posInicial['stringTemp']
registrosMem[contadorReg['booleanTemp']] = posInicial['booleanTemp']

registrosMem[contadorReg['intCTE']] = posInicial['intCTE']
registrosMem[contadorReg['decCTE']] = posInicial['decCTE']
registrosMem[contadorReg['stringCTE']] = posInicial['stringCTE']
registrosMem[contadorReg['booleanCTE']] = posInicial['booleanCTE']

def resetFuncMems():
    registrosMem[contadorReg['intLocal']] = posInicial['intLocal']
    registrosMem[contadorReg['decLocal']] = posInicial['decLocal']
    registrosMem[contadorReg['stringLocal']] = posInicial['stringLocal']
    registrosMem[contadorReg['booleanLocal']] = posInicial['booleanLocal']

def resetTodo():
    registrosMem[contadorReg['intGlobal']] = posInicial['intGlobal']
    registrosMem[contadorReg['decGlobal']] = posInicial['decGlobal']
    registrosMem[contadorReg['stringGlobal']] = posInicial['stringGlobal']
    registrosMem[contadorReg['booleanGlobal']] = posInicial['booleanGlobal']

    registrosMem[contadorReg['intLocal']] = posInicial['intLocal']
    registrosMem[contadorReg['decLocal']] = posInicial['decLocal']
    registrosMem[contadorReg['stringLocal']] = posInicial['stringLocal']
    registrosMem[contadorReg['booleanLocal']] = posInicial['booleanLocal']

    registrosMem[contadorReg['intTemp']] = posInicial['intTemp']
    registrosMem[contadorReg['decTemp']] = posInicial['decTemp']
    registrosMem[contadorReg['stringTemp']] = posInicial['stringTemp']
    registrosMem[contadorReg['booleanTemp']] = posInicial['booleanTemp']

    registrosMem[contadorReg['intCTE']] = posInicial['intCTE']
    registrosMem[contadorReg['decCTE']] = posInicial['decCTE']
    registrosMem[contadorReg['stringCTE']] = posInicial['stringCTE']
    registrosMem[contadorReg['booleanCTE']] = posInicial['booleanCTE']

# getTipo: Regresa el tipo de dato segun la posicion de memoria que tiene asignado (en codigo)
def getTipo(dirMemoria): 
    if dirMemoria <= posLimite['intGlobal']: return code['int']
    if dirMemoria <= posLimite['decGlobal']: return code['dec']
    if dirMemoria <= posLimite['stringGlobal']: return code['string']
    if dirMemoria <= posLimite['booleanGlobal']: return code['boolean']

    if dirMemoria <= posLimite['intLocal']: return code['int']
    if dirMemoria <= posLimite['decLocal']: return code['dec']
    if dirMemoria <= posLimite['stringLocal']: return code['string']
    if dirMemoria <= posLimite['booleanLocal']: return code['boolean']
    
    if dirMemoria <= posLimite['intTemp']: return code['int']
    if dirMemoria <= posLimite['decTemp']: return code['dec']
    if dirMemoria <= posLimite['stringTemp']: return code['string']
    if dirMemoria <= posLimite['booleanTemp']: return code['boolean']
    
    if dirMemoria <= posLimite['intCTE']: return code['int']
    if dirMemoria <= posLimite['decCTE']: return code['dec']
    if dirMemoria <= posLimite['stringCTE']: return code['string']
    if dirMemoria <= posLimite['booleanCTE']: return code['boolean']