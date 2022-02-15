import random
import os
def bienvenida():
    limpiarPantalla()
    print(""" \033[94m
            ░█████╗░░░░░░██╗███████╗██████╗░██████╗░███████╗███████╗
            ██╔══██╗░░░░░██║██╔════╝██╔══██╗██╔══██╗██╔════╝╚════██║
            ███████║░░░░░██║█████╗░░██║░░██║██████╔╝█████╗░░░░███╔═╝
            ██╔══██║██╗░░██║██╔══╝░░██║░░██║██╔══██╗██╔══╝░░██╔══╝░░
            ██║░░██║╚█████╔╝███████╗██████╔╝██║░░██║███████╗███████╗
            ╚═╝░░╚═╝░╚════╝░╚══════╝╚═════╝░╚═╝░░╚═╝╚══════╝╚══════╝
            \033[0m
    """)

def limpiarPantalla():
    """IMPRIME 50 SALTOS DE LINEA """
    print("\n" * 50)
def error(error):
    print("\033[91m",error,"\033[0m")

######### CARGA Y GUARDADO DE CODIGO ############################################################
def guardarDiccionario(partidasGuardadas):
    """GUARDA EL DICCIONARIO DE LAS PARTIDAS EN CURSO EN UN ARCHIVO DE TEXTO"""
    try:
        archivo=open("partidasGuardadas.txt","w")
        linea=""
        for elem in list(partidasGuardadas.keys()):
            linea+=elem
            linea+=","
            linea+=partidasGuardadas[elem]
            linea+="\n"
            archivo.write(linea)
    finally:
        try:
            archivo.close()
        except NameError as mensaje:
            print("Error",mensaje)
            pass

def guardarTablero(tablero,numeroRonda,turno,path):
    """GUARDA EL TABLERO EN UN ARCHIVO DE TEXTO"""
    try:
        archivo=open(path,"w")
        archivo.write(str(numeroRonda) +","+ turno+"\n")
        for x in tablero:
            linea=""
            for y in x:
                linea+=str(ord(y))+","
            archivo.write(linea[:-1]+"\n")
        print("¡Partida guardada correctamente!")
    except FileNotFoundError:
        error("Archivo no encontrado")

    finally:
        try:
            archivo.close()
            print("Gracias por jugar. El tablero se guardo asi: ")
        except NameError as mensaje:
            error("Error: El archivo no pudo ser generado")
            print(mensaje)
            pass

def mainGuardar(partidasGuardadas,tablero,numeroRonda,turno):
    """FUNCION PRINCIPAL DEL GUARDADO DE ARCHIVOS.
    PRIMERO CREA UNA RUTA ALEATORIA EN DONDE GUARDAR LA INFORMACION DEL TABLERO.
    LUEGO PIDE EL INGRESO DEL NOMBRE PARA IDENTIFICAR LA PARTIDA

    PARA FINALIZAR LLAMA A LAS FUNCIONES DE GUARDADO DE TABLERO Y GUARDADO DEL DICCIONARIO DONDE SE GUARDA LAS INFO DE LAS PARTIDAS
    """
    valido = False
    path=""
    abc=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"
         ,"A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"
         ,"0","1","2","3","4","5","6","7","8","9"]
    for i in range (0,14):
        path+=str(abc[random.randint(0,len(abc)-1)])
    path+=".txt"

    while not valido:
        name = input("Ingrese el nombre de la partida: ")
        if name in list(partidasGuardadas.keys()):
            error("Ya existe una partida guardada con ese nombre.")
            sobrescribir=input("¿Desea sobrescribir la partida? S/N :")
            if sobrescribir.upper()=="S":
                partidasGuardadas[name] = path
                guardarDiccionario(partidasGuardadas)
                guardarTablero(tablero, numeroRonda, turno, path)
                valido=True
            else:
                pass


        else:
            partidasGuardadas[name]=path
            guardarDiccionario(partidasGuardadas)
            guardarTablero(tablero,numeroRonda,turno,path)
            valido=True


def cargarTablero(tablero,blancas,negras,path,partidasGuardadas):
    """ RECIBE LA UBICACION DE UN ARCHIVO Y LO ABRE PARA CARGAR EL TABLERO DE LA PARTIDA A REANUDAR """
    numeroRonda=1
    turno="jugador blanco"
    try:
        archivo = open(path, "r")
        numeroRonda,turno = archivo.readline().rstrip("\n").split(",")
        numeroRonda=int(numeroRonda)
        for elemento in tablero:
            linea=archivo.readline().split(",")
            for i in range (0,8):
                elemento[i]=chr(int(linea[i]))
    except ValueError as mensaje:
        print("Error: El archivo se encuentra alterado", mensaje)
        llenarTableroInicial(tablero, blancas, negras)
        guardarTablero(tablero,1,"jugador blanco",path)
        numeroRonda=0
        turno="jugador blanco"


        return numeroRonda,turno
    except FileNotFoundError as mensaje:
        llenarTableroInicial(tablero, blancas, negras)
        guardarTablero(tablero,1,"jugador blanco",path)
        print("Error: El archivo no se encontro", mensaje)
        error("Se inicio una partida nueva")
    except OSError as mensaje:
        llenarTableroInicial(tablero, blancas, negras)
        guardarTablero(tablero, 1, "jugador blanco",path)
        print("Error: No se pudo leer el archivo",mensaje)
        error("Se inicio una partida nueva")
    finally:
        try:
            archivo.close()
        except NameError:
            pass
    return numeroRonda,turno

def mergePartidas(partidasGuardadas):
    """ABRE EL ARCHIVO PARTIDASGUARDAS, LO ANALIZA COMO SI FUERA UN CSV Y RELLENA EL DICCIONARIO PARTIDASGUARDADAS
    CON LA CLAVE "NOMBRE DE LA PARTIDA" Y VALOR "LA UBICACION DEL ARCHIVO QUE GUARDA EL TABLERO" """
    try:
        arch=open("partidasGuardadas.txt","r")
        linea=arch.readline()
        while linea:
            nombre,path=linea.rstrip("\n").split(",")
            partidasGuardadas[nombre]=path
            linea=arch.readline()
    except FileNotFoundError as mensaje:
        print("Error: No se encontro el directorio de partidas guardadas",mensaje)
    except OSError as mensaje:
        print("Error: No se puede leer el archivo: ",mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass

##################### CREAR EL TABLERO####################################################

def crearMatriz():
    """"DEVUELVE UNA MATRIZ LLENA DE "ㅡ" """
    matriz = [["ㅡ"] * 8 for i in range(8)]
    return matriz

def imprimirTablero(matriz):
    """IMPRIME EN PANTALLA EL TABLERO, CON UN COLOR DISTINTO PARA CADA EQUIPO"""
    fichasBlancas = ["♙", "♖", "♘", "♗", "♔", "♕", "♗", "♘", "♖"]
    fichasNegras = ["♟", "♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"]
    filas=len(matriz)
    columnas=len(matriz[0])
    abc = [" A", "B", "C", "D", "E", "F", "G", "H"]
    for elem in abc:
        print("%3s" %elem,end=" ")
    print("")
    for f in range (filas):
        print(f+1,end="")
        for c in range (columnas):
            if matriz[f][c] in fichasNegras:
                print("\033[91m","%3s" %matriz[f][c],"\033[0m",end="",sep="")
            elif matriz[f][c] in fichasBlancas:
                print("\033[94m", "%3s" %matriz[f][c],"\033[0m", end="",sep="")
            else:
                print("%3s" %matriz[f][c],end="")
        print()

def llenarTableroInicial(matriz, blancas, negras):
    """RECIBE UNA MATRIZ Y LA COMPLETA CON LAS PIEZAS EN LAS POSICIONES INICIALES PARA COMENZAR EL JUEGO"""
    for i in range(0, 8):
            matriz[1][i] = "♟"
            matriz[6][i] = "♙"
    for i in range(0, 8):
            matriz[0][i] = negras[i + 1]
            matriz[7][7 - i] = blancas[i + 1]

############# MOVIMIENTOS DE PIEZAS ####################################################

def reemplazarPieza(tablero,pieza,x,y,xfinal,yfinal):
    """REALIZA EL MOVIMIENTO DE LA PIEZA EN EL TABLERO"""
    tablero[y][x]="ㅡ"
    tablero[yfinal][xfinal]=pieza
    return True

def noreste(tablero,x,y,xfinal,yfinal,pieza,piezas): #X INCREMENTA Y DECRECE. MOVIMIENTO ARRIBA A LA DERECHA
    #VERIFICAR Q NO SALTE PIEZAS
    #VERIFICAR SI SE PUEDE COMER A ALGUNA FICHA
    xparcial=int(x)
    for i in range(y - 1, yfinal, -1):
        xparcial+=1
        if queHayEnPosicion(tablero, xparcial, i) != "ㅡ":
            error("No puedes saltear piezas")
            return False
    if queHayEnPosicion(tablero,xfinal,yfinal) in piezas:
        error("Movimiento invalido: Ya hay una pieza tuya en esa posicion")
        return False
    else:
        return reemplazarPieza(tablero, pieza, x, y, xfinal, yfinal)

def noroeste(tablero,x,y,xfinal,yfinal,pieza,piezas): #X INCREMENTA Y DECRECE. MOVIMIENTO ARRIBA A LA DERECHA
    xparcial=int(x)
    for i in range(y - 1, yfinal, -1):
        xparcial-=1
        if queHayEnPosicion(tablero, xparcial, i) != "ㅡ":
            error("No puedes saltear piezas")
            return False
    if queHayEnPosicion(tablero,xfinal,yfinal) in piezas:
        error("Movimiento invalido: Ya hay una pieza tuya en esa posicion")
        return False
    else:
        return reemplazarPieza(tablero, pieza, x, y, xfinal, yfinal)

def suroeste(tablero,x,y,xfinal,yfinal,pieza,piezas): #X INCREMENTA Y DECRECE. MOVIMIENTO ARRIBA A LA DERECHA
    xparcial=int(x)
    for i in range(y + 1, yfinal, +1):
        xparcial-=1
        if queHayEnPosicion(tablero, xparcial, i) != "ㅡ":
            error("No puedes saltear piezas")
            return False
    if queHayEnPosicion(tablero,xfinal,yfinal) in piezas:
        error("Movimiento invalido: Ya hay una pieza tuya en esa posicion")
        return False
    else:
        return reemplazarPieza(tablero, pieza, x, y, xfinal, yfinal)

def sureste(tablero,x,y,xfinal,yfinal,pieza,piezas): #X INCREMENTA Y DECRECE. MOVIMIENTO ARRIBA A LA DERECHA
    xparcial=int(x)
    for i in range(y + 1, yfinal, +1):
        xparcial+=1
        if queHayEnPosicion(tablero, xparcial, i) != "ㅡ":
            error("No puedes saltear piezas")
            return False
    if queHayEnPosicion(tablero,xfinal,yfinal) in piezas:
        error("Movimiento invalido: Ya hay una pieza tuya en esa posicion")
        return False
    else:
        return reemplazarPieza(tablero, pieza, x, y, xfinal, yfinal)



def movimientoAlfil(tablero,posInicial,posFinal,pieza,x,y,xfinal,yfinal):
    """VERIFICA HACIA QUE DIRECCION SE QUIERE MOVER LA PIEZA Y LLAMA A SU RESPECTIVA FUNCION"""
    fichasBlancas = ["♙", "♖", "♘", "♗", "♔", "♕", "♗", "♘", "♖"]
    fichasNegras = ["♟", "♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"]
    if 0 <= xfinal <= 7 and 0 <= yfinal <= 7:
        if(x!=xfinal) and (y!=yfinal):
            if (x>xfinal) and (y>yfinal):
                if pieza in fichasBlancas:
                    movimientoRealizado=noroeste(tablero,x,y,xfinal,yfinal,pieza,fichasBlancas)

                elif pieza in fichasNegras:
                    movimientoRealizado=noroeste(tablero, x, y, xfinal, yfinal, pieza, fichasNegras)
            elif (x>xfinal) and (y<yfinal):
                if pieza in fichasBlancas:
                    movimientoRealizado=suroeste(tablero, x, y, xfinal, yfinal, pieza, fichasBlancas)
                elif pieza in fichasNegras:
                    movimientoRealizado=suroeste(tablero, x, y, xfinal, yfinal, pieza, fichasNegras)
            elif (x<xfinal) and (y>yfinal):
                if pieza in fichasBlancas:
                    movimientoRealizado=noreste(tablero, x, y, xfinal, yfinal, pieza, fichasBlancas)
                elif pieza in fichasNegras:
                    movimientoRealizado=noreste(tablero, x, y, xfinal, yfinal, pieza, fichasNegras)
            elif (x<xfinal) and (y<yfinal):
                if pieza in fichasBlancas:
                    movimientoRealizado=sureste(tablero, x, y, xfinal, yfinal, pieza, fichasBlancas)
                elif pieza in fichasNegras:
                    movimientoRealizado=sureste(tablero, x, y, xfinal, yfinal, pieza, fichasNegras)
            else:
                error("Error: Movimiento diagonal invalido")
                return False

            if movimientoRealizado==True:
                return True

            return movimientoRealizado
        else:
            error("Movimiento invalido: El alfil solamente se mueve en diagonal")
            return False
    else:
        error("Error: posicion invalida")
        return False

def peonSaltoDoble(tablero,x,y,xfinal,yfinal,pieza,origen):
    """MOVIMIENTO DEL PEON 2 UNIDADES HACIA ADELANTE
    VERIFICA QUE NO SALTE NINGUNA PIEZA"""
    print(origen)
    print(y)
    if y == origen:
        if pieza=="♙":
            if (queHayEnPosicion(tablero, xfinal, yfinal) == "ㅡ") and (
                    queHayEnPosicion(tablero, xfinal, yfinal + 1) == "ㅡ"):  # MOVER 2 POSICIONES SIN SALTAR FICHAS
                tablero[yfinal][xfinal] = pieza
                tablero[y][x] = "ㅡ"
                print("Exito: Jugada realizada")
                return True
            else:
                error("Movimiento invalido: Los peones no pueden saltar piezas 2a")
                return False
        else:
                if (queHayEnPosicion(tablero, xfinal, yfinal) == "ㅡ") and (
                        queHayEnPosicion(tablero, xfinal, yfinal - 1) == "ㅡ"):  # MOVER 2 POSICIONES SIN SALTAR FICHAS
                    tablero[yfinal][xfinal] = pieza
                    tablero[y][x] = "ㅡ"
                    print("Exito: Jugada realizada")
                    return True
                else:
                    error("Movimiento invalido: Los peones no pueden saltar piezas 22")
                    return False

    else:
        error(
            "Movimiento invalido: Los peones solamente se pueden mover 2 unidades en el primer movimiento de la pieza")
        return False

def peonSimple(tablero,x,y,xfinal,yfinal,pieza,fichas):
    """MOVIMIENTO DEL PEON 1 UNIDAD HACIA ADELANTE
    VERIFICA SI PUEDE MATAR LATERALMENTE"""

    if xfinal == x - 1 or xfinal == x + 1:
        if queHayEnPosicion(tablero, xfinal, yfinal) in fichas:
            tablero[yfinal][xfinal] = pieza
            tablero[y][x] = "ㅡ"
            print("Exito: Jugada realizada")
            return True
        else:
            error("Movimiento invalido: Los peones solo pueden moverse en diagonal para matar una pieza enemiga")
            return False
    elif xfinal == x:
        if queHayEnPosicion(tablero, xfinal, yfinal) == "ㅡ":
            print("Exito: Jugada realizada")
            tablero[yfinal][xfinal] = pieza
            tablero[y][x] = "ㅡ"
            return True
        else:
            error("Movimiento invalido: Los peones no pueden saltar piezas 1")
            return False
    else:
        error("Error: Movimiento no registrado")
        return True

def coronar(tablero,pieza,xfinal,yfinal):
    """SI UN PEON LLEGA AL FINAL DEL TABLERO, PUEDE ELEGIR UNA PIEZA PARA AGREGAR AL TABLERO"""
    fichasBlancas = ["♖", "♘", "♗", "♔"]
    fichasNegras = ["♜", "♞", "♝", "♚"]
    if yfinal==0:
        opcion=0
        while not 1<=opcion<=5:
            print("Elige una pieza")
            for elem in fichasBlancas:
                print(fichasBlancas.index(elem)+1,"-",elem)
            opcion=int(input("Ingrese el numero de la pieza a agregar:"))
        piezaAgregar = fichasBlancas[opcion - 1]

    else:
        opcion=0
        while not 1 <= opcion <= 5:
            print("Elige una ficha")
            for elem in fichasNegras:
                print(fichasNegras.index(elem) + 1, "-", elem)
            opcion = int(input("Ingrese el numero de la pieza a agregar:"))
        piezaAgregar=fichasNegras[opcion-1]
    tablero[yfinal][xfinal] = piezaAgregar
    print("Se agrego la ficha: ", piezaAgregar)





def movimientoPeon(tablero,posInicial,posFinal,pieza,x,y,xfinal,yfinal):
    """VERFICAN QUE VAYAN SIEMPRE HACIA ADELANTE
    SI SE MUEVE 2 HACIA ADELANTE VERIFICA QUE LA POSICION INICIAL SEA LA DE ARRANQUE
    SI EL MOVIMIENTO ES 1 UNIDAD HACIA ADELANTE VERIFICA QUE NO SALTE PIEZAS
    Y SI EL MOVIMIENTO ES 1 HACIA ADELANTE Y UNO HACIA LA IZQUIERDA/DERECHA VERIFICA QUE PUEDA MATAR A UNA PIEZA"""
    fichasBlancas = ["♙", "♖", "♘", "♗", "♔", "♕", "♗", "♘", "♖"]
    fichasNegras = ["♟", "♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"]
    movimientoRealizado=False
    if pieza=="♟": #negras #estas van para abajo por ende el Y sube
        if 0 <= xfinal <= 7 and 0 <= yfinal <= 7:
            if yfinal > y:
                if yfinal == y +2:
                    if x == xfinal:
                        #movimientoRealizado=peonSaltoDoble(tablero,x,y,xfinal,yfinal,pieza,1)
                        movimiento=peonSaltoDoble(tablero,x,y,xfinal,yfinal,pieza,1)
                        if movimiento and (yfinal==7 or yfinal==0):
                            ## CORONAR PIEZA
                            coronar(tablero, pieza, xfinal, yfinal)
                            movimientoRealizado=True
                        else:
                            movimientoRealizado = True
                    else:
                        error("Movimiento invalido: Si los peones se mueven 2 unidades para adelante, no pueden realizar un movimiento en diagonal")
                        return False
                elif yfinal == y + 1: #PEON MOVIMIENTO DIAGONAL
                    #movimientoRealizado=peonSimple(tablero,x,y,xfinal,yfinal,pieza,fichasBlancas)
                    movimiento=peonSimple(tablero,x,y,xfinal,yfinal,pieza,fichasBlancas)

                    if movimiento and (yfinal == 7 or yfinal == 0):
                        ## CORONAR PIEZA
                        coronar(tablero, pieza, xfinal, yfinal)
                        movimientoRealizado = True
                    elif movimiento:
                        movimientoRealizado = True
                    else:
                        return False
                else:
                    error("Movimiento invalido: Los peones no pueden moverse mas de 2 posiciones por turno")
                    return False
                if movimientoRealizado:
                    return True
            else:
                error("Movimiento invalido: El movimiento de los peones siempre tiene que ser para adelante")
                return False

        else:
            error("Error: Jugada fuera del tablero")
            return False

    elif pieza=="♙": #blancas #van para arriba, por ende el Y baja
        if 0<=xfinal<=7 and 0<=yfinal<=7:
            if yfinal < y:
                if yfinal==y-2:
                    if x==xfinal:
                        movimiento = peonSaltoDoble(tablero, x, y, xfinal, yfinal, pieza, 6)
                        if movimiento and (yfinal == 7 or yfinal == 0):
                            ## CORONAR PIEZA
                            coronar(tablero, pieza, xfinal, yfinal)
                            movimientoRealizado = True
                        else:
                            movimientoRealizado = True
                    else:
                        error(
                            "Movimiento invalido: Si los peones se mueven 2 unidades para adelante, no pueden realizar un movimiento en diagonal")
                        return False
                elif yfinal==y-1: #PEON MOVIMIENTO 1 U ADELANTE
                    movimiento=peonSimple(tablero,x,y,xfinal,yfinal,pieza,fichasNegras)
                    if movimiento and (yfinal == 7 or yfinal == 0):
                        ## CORONAR PIEZA
                        coronar(tablero,pieza,xfinal,yfinal)
                        movimientoRealizado = True
                    elif movimiento:
                        movimientoRealizado = True
                    else:
                        return False

                else:
                    error("Movimiento invalido: Los peones no pueden moverse mas de 2 posiciones por turno")
                    return False
                if movimientoRealizado:
                    return True
            else:
                error("Movimiento invalido: El movimiento de los peones siempre tiene que ser para adelante")
                return False

        else:
            error("Error: Jugada fuera del tablero")
            return False

def movimientoAprobado(tablero,x,y,xfinal,yfinal,fichas,pieza):
    """REALIZA EL REMPLAZO EN EL TABLERO SI ES POSIBLE. RETORNA TRUE O FALSE"""
    if queHayEnPosicion(tablero, xfinal, yfinal) in fichas:
        print("Exito: Jugada realizada")
        tablero[yfinal][xfinal] = pieza
        tablero[y][x] = "ㅡ"
        return True
    elif queHayEnPosicion(tablero, xfinal, yfinal) == "ㅡ":
        print("Exito: Jugada realizada")
        tablero[yfinal][xfinal] = pieza
        tablero[y][x] = "ㅡ"
        return True
    else:
        error("Movimiento invalido: En esa posicion hay una pieza tuya")
        return False

def movimientoArriba(tablero,x,y,xfinal,yfinal,fichas,pieza):
    """PERMITE MOVER LA PIEZA HACIA ARRIBA, VERIFICANDO QUE NO SALTE NINGUNA OTRA PIEZA"""
    for i in range(y - 1, yfinal, -1):
        if queHayEnPosicion(tablero, x, i) != "ㅡ":
            error("Movimiento invalido: No puedes saltear piezas")
            return False
    return movimientoAprobado(tablero, x, y, xfinal, yfinal, fichas, pieza)

def movimientoAbajo(tablero,x,y,xfinal,yfinal,fichas,pieza):
    """PERMITE MOVER LA PIEZA HACIA ABAJO, VERIFICANDO QUE NO SALTE NINGUNA OTRA PIEZA"""
    for i in range(y + 1, yfinal, 1):
        if queHayEnPosicion(tablero, x, i) != "ㅡ":
            error("Movimiento invalido: No puedes saltear piezas")
            return False
    return movimientoAprobado(tablero, x, y, xfinal, yfinal, fichas, pieza)

def movimientoIzquierda(tablero,x,y,xfinal,yfinal,fichas,pieza):
    """PERMITE MOVER LA PIEZA HACIA LA IZQUIERDA, VERIFICANDO QUE NO SALTE NINGUNA OTRA PIEZA"""
    for i in range(x - 1, xfinal, -1):
        if queHayEnPosicion(tablero, i, y) != "ㅡ":
            error("Movimiento invalido: No puedes saltear piezas")
            return False
    return movimientoAprobado(tablero, x, y, xfinal, yfinal, fichas, pieza)

def movimientoDerecha(tablero,x,y,xfinal,yfinal,fichas,pieza):
    """PERMITE MOVER LA PIEZA HACIA LA DERECHA, VERIFICANDO QUE NO SALTE NINGUNA OTRA PIEZA"""
    for i in range(x +1, xfinal,1):
        if queHayEnPosicion(tablero, i, y) != "ㅡ":
            error("Movimiento invalido: No puedes saltear piezas")
            return False
    return movimientoAprobado(tablero, x, y, xfinal, yfinal, fichas, pieza)

def movimientoTorre(tablero,posInicial,posFinal,pieza,x,y,xfinal,yfinal):
    """VERIFICA Q SE MUEVA O EN EL EJE Y O EN EL EJE X
    LUEGO LLAMA A LA FUNCION INDICADA PARA CADA TIPO DE MOVIMIENTO
    """

    fichasBlancas = ["♙", "♖", "♘", "♗", "♔", "♕", "♗", "♘", "♖"]
    fichasNegras = ["♟", "♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"]
    realizado=False
    if 0 <= xfinal <= 7 and 0 <= yfinal <= 7:
        if x==xfinal or y==yfinal:
            if x==xfinal: #SE MUEVE PARA ARRIBA O PARA ABAJO
                if y>yfinal: #SE MUEVE PARA ARRIBA
                    if pieza in fichasNegras:# negras
                        realizado=movimientoArriba(tablero,x,y,xfinal,yfinal,fichasBlancas,pieza)
                    elif pieza in fichasBlancas:#blancas
                        realizado=movimientoArriba(tablero,x,y,xfinal,yfinal,fichasNegras,pieza)

                elif y < yfinal:  # SE MUEVE PARA ABAJO
                    if pieza in fichasNegras:  # negras
                        realizado=movimientoAbajo(tablero,x,y,xfinal,yfinal,fichasBlancas,pieza)
                    elif pieza in fichasBlancas:#blancas
                        realizado=movimientoAbajo(tablero,x,y,xfinal,yfinal,fichasNegras,pieza)
                if realizado:
                    return True
                else:
                    return False

            elif y==yfinal: #SE MUEVE PARA LOS COSTADOS
                if x > xfinal:  # SE MUEVE PARA IZQUIERDA
                    if pieza in fichasNegras:  # negras
                        realizado = movimientoIzquierda(tablero, x, y, xfinal, yfinal, fichasBlancas, pieza)
                    elif pieza in fichasBlancas:  # blancas
                        realizado = movimientoIzquierda(tablero, x, y, xfinal, yfinal, fichasNegras, pieza)

                    if realizado:
                        return True
                    else:
                        return False

                elif x < xfinal:  # SE MUEVE PARA DERECHA
                    if pieza in fichasNegras:  # negras
                        realizado = movimientoDerecha(tablero, x, y, xfinal, yfinal, fichasBlancas, pieza)
                    elif pieza in fichasBlancas:  # blancas
                        realizado = movimientoDerecha(tablero, x, y, xfinal, yfinal, fichasNegras, pieza)
                    if realizado:
                        return True
                    else:
                        return False

        else:
            error("Movimiento invalido: La torre no se puede mover en horizontal y en vertical al mismo tiempo")
            return False
    else:
        error("Error: Jugada fuera del tablero")
        return False

def movimientoReina(tablero,posInicial,posFinal,pieza,x,y,xfinal,yfinal):
    """VERIFICA QUE SE MUEVA EN AUNQUE SEA UNA DIRECCION
    LUEGO SI EL MOVIMIENTO ES EN LATERAL, LLAMA A LA FUNCION ALFIL QUE TIENE EL MISMO MOVIMIENTO SIMILAR
    O SI EL MOVIENTO ES EN UN SOLO EJE, LLAMA A LA FUNCION TORRE QUE TIENE EL MISMO MOVIMIENTO"""
    fichasBlancas = ["♙", "♖", "♘", "♗", "♔", "♕", "♗", "♘", "♖"]
    fichasNegras = ["♟", "♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"]
    if 0 <= xfinal <= 7 and 0 <= yfinal <= 7:
        if (x != xfinal) and (y != yfinal): #Movimiento es lateral se llama a la funcion alfil
            movimientoRealizado=movimientoAlfil(tablero,posInicial,posFinal,pieza,x,y,xfinal,yfinal)
        elif x==xfinal or y==yfinal: #Tiene el movimiento de una torre
            movimientoRealizado=movimientoTorre(tablero, posInicial, posFinal, pieza, x, y, xfinal, yfinal)
        if movimientoRealizado:
            return True

        return movimientoRealizado
    else:
        error("Error: posicion invalida")
        return False

def movimientoRey(tablero,posInicial,posFinal,pieza,x,y,xfinal,yfinal):
    """ VERIFICA QUE SOLAMENTE SE MUEVA UNA POSICION EN CUALQUIER DIRECCION
    LUEGO PARA CONTUNAR EL MOVIMIENTO LLAMA A LA FUNCION MOVIMIENTO REINA YA QUE ESTA TIENE EL MISMO MOVIMIENTO"""
    #XFINAL = X o X-1 o X+1  x-1<=xfinal=<x+1
    #Y FINAL = Y o Y-1 o Y+1
    if (x-1<=xfinal<=x+1) and (y-1<=yfinal<=y+1):
        movimientoRealizado=movimientoReina(tablero, posInicial, posFinal, pieza, x, y, xfinal, yfinal)
    else:
        error("Error:El rey solo puede moverse una unidad")
        movimientoRealizado=False
    if movimientoRealizado:
        return True
    else:
        return False

def movimientoCaballo(tablero,posInicial,posFinal,pieza,x,y,xfinal,yfinal):
    """VERIFICA SI EL MOVIMIENTO DESEADO ES POSIBLE
    RETORNA TRUE O FALSE
    CASO DE TRUE, REALIZA EL MOVIMIENTO

    VERIFICA: QUE EL MOVIMIENTO SEA EN 2X y 1EN Y  o 2 EN Y  y 1 EN X
    VERFICIA: QUE EN LA POSICION DESEADA NO HAYA UNA PIEZA TUYA
    """
    #(2X y 1Y) o (1X y 2Y)
    #puede saltar piezas
    fichasBlancas = ["♙", "♖", "♘", "♗", "♔", "♕", "♗", "♘", "♖"]
    fichasNegras = ["♟", "♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"]
    if 0 <= xfinal <= 7 and 0 <= yfinal <= 7:
        if ((xfinal==x+1 or xfinal==x-1) and (yfinal==y+2 or yfinal==y-2)) or ((xfinal==x+2 or xfinal==x-2) and (yfinal==y+1 or yfinal==y-1)):
            movimientoRealizado=False
            #Verificar q no haya una pieza tuya en esa
            if pieza in fichasBlancas:
                if queHayEnPosicion(tablero,xfinal,yfinal) in fichasBlancas:
                    error("Movimiento invalido: Ya hay una pieza tuya en esa posicion")
                    return False
                else:
                    movimientoRealizado=reemplazarPieza(tablero,pieza,x,y,xfinal,yfinal)
            elif pieza in fichasNegras:
                if queHayEnPosicion(tablero,xfinal,yfinal) in fichasNegras:
                    error("Movimiento invalido: Ya hay una pieza tuya en esa posicion")
                    return False
                else:
                    movimientoRealizado=reemplazarPieza(tablero,pieza,x,y,xfinal,yfinal)
            if movimientoRealizado:
                return True

        else:
            error("Movimiento invalido: El caballo solo puede moverse 2 posiciones en un eje y una en el otro")
            return False
    else:
        error("Error: Jugada fuera del tablero")
        return False



##################### ELEGIR PIEZA A MOVER ###################################

def queHayEnPosicion(tablero,x,y):
    """PRE: RECIBE EL TABLERO Y 1 POSICION (X,Y)
    POS: DEVUELVE LA PIEZA QUE SE ENCUENTRA EN ESA POSICION"""
    return tablero[y][x]

def moverPieza(pieza,posIngresada,tablero,abc,x,y):
    """ESTA FUNCION PERMITE MOVER LA PIEZA ELEGIDA, O VOLVER HACIA ATRAS EN CASO DE ARREPENTIRSE
    SI EL INGRESO ES PARA VOLVER, LA FUNCION RETORNA FALSE
    SI SE INGRESA UNA PIEZA VALIDA, LLAMA A LA FUNCION CORRESPONDIENTE A CADA PIEZA PARA REALIZAR EL MOVIMIENTO.

    """
    piezaMovida=False
    while not piezaMovida:
        print("Ustede esta moviendo la ficha: ", pieza, "Ubicada en: ", posIngresada )
        print("\033[94mPara volver al menu anterior ingrese (S1)\033[0m")
        posicionDeseada = input("Ingrese la casilla a la cual se quiere mover (EJ A1): ")

        if len(posicionDeseada) != 2:
            error("Error: El largo maximo de la respuesta esperada es 2 unidades")
            error("Vuelva a intentarlo")
        if posicionDeseada[0].upper()=="S":
            print("➤"*40)
            return False
        else:
            xfinal = posicionDeseada[0]
            yfinal = posicionDeseada[1]
            if xfinal.isalpha():
                try:
                    xfinal = abc.index(xfinal.upper())
                    yfinal = int(yfinal) - 1
                    ##### ELIJO EL MOVIMIENTO A REALIZAR
                    if pieza=="♙" or pieza=="♟":
                            piezaMovida=movimientoPeon(tablero,posIngresada,posicionDeseada,pieza,x,y,xfinal,yfinal)
                            #return True
                    elif pieza=="♖" or pieza=="♜":
                            piezaMovida=movimientoTorre(tablero,posIngresada,posicionDeseada,pieza,x,y,xfinal,yfinal)
                            #return True
                    elif pieza=="♗" or pieza=="♝":
                            piezaMovida=movimientoAlfil(tablero,posIngresada,posicionDeseada,pieza,x,y,xfinal,yfinal)
                            #return True
                    elif pieza=="♔" or pieza=="♚":
                            piezaMovida=movimientoReina(tablero,posIngresada,posicionDeseada,pieza,x,y,xfinal,yfinal)
                            #return True
                    elif pieza=="♕" or pieza=="♛":
                            piezaMovida=movimientoRey(tablero,posIngresada,posicionDeseada,pieza,x,y,xfinal,yfinal)
                            #return True
                    elif pieza=="♘" or pieza=="♞":
                            piezaMovida=movimientoCaballo(tablero,posIngresada,posicionDeseada,pieza,x,y,xfinal,yfinal)
                            #return True
                    return piezaMovida
                except ValueError:
                    error("Error: Se esperaba el ingreso de una letra y un numero. (Ejemplo A1)")
                    error("Vuelva a intentarlo")
            else:
                error("Error: Entrada invalida")

def elegirPieza(tablero,turno,blancas,negras):
    """-ESTA FUNCION PERMITE AL USUARIO ELEGIR QUE PIEZA DEL TABLERO QUIERE MOVER
    ESTA FUNCION REPETIRA EL PROCESO HASTA QUE LA ENTRADA SEA VALIDA.
    -EN CASO DE QUERER RENDIRSE O CERRAR EL JUEGO TAMBIEN VERIFICA ESTAS POSIBILIDADES
    -CUANDO INGRESE UN PIEZA VALIDA, INTENTARA MOVERLA CON LA FUNCION MOVERPIEZA() LA CUAL LE DEVOLVERA TRUE O FALSE
    """
    piezaCorrecta=False
    abc=["A","B","C","D","E","F","G","H"]
    while not piezaCorrecta:
        print("\033[94mPara salir del juego y guardar la partida ingrese (S1)\033[0m")
        print("\033[94mPara rendirse ingrese (R1)\033[0m")
        pieza = input("\033[96mIngrese la pieza que quiera mover (EJ A1): \033[0m")
        posIngresada=str(pieza)
        if len(pieza)!=2:
            error("Error: El largo maximo de la respuesta esperada es 2 unidades")
            print("Vuelva a intentarlo")
        else:
            x= pieza[0]
            y = pieza[1]
            if x.isalpha():
                try:
                    if x.upper()=="S":
                        return "cerrarJuego"
                    if x.upper()=="R":
                        return "rendirse"


                    y = int(y)-1
                    pieza = tablero[y][abc.index(x.upper())]
                    x=abc.index(x.upper())
                    if turno=="jugador blanco":
                        if pieza in blancas:
                                piezaMovida=moverPieza(pieza, posIngresada, tablero, abc, x, y)
                                if piezaMovida==False:
                                    piezaCorrecta=False
                                else:
                                    piezaCorrecta = True
                        else:
                            error("Error: Esa ficha no te pertence")
                    elif turno=="jugador negro":
                        if pieza in negras:
                            piezaMovida = moverPieza(pieza, posIngresada, tablero, abc, x, y)
                            if piezaMovida == False:
                                piezaCorrecta = False
                            else:
                                piezaCorrecta = True
                        else:
                            error("Error: Esa ficha no te pertence")
                except ValueError:
                    error("Error: Se esperaba el ingreso de una letra y un numero. (Ejemplo A1)")
                    error("Vuelva a intentarlo")
            else:
                error("Error: Entrada invalida")

############## juego ###############################################
def finDelJuego(tablero,partidasGuardadas,ganador):
    """FUNCION DE FIN DE JUEGO"""
    print("""\033[91m
░██████╗░░█████╗░███╗░░░███╗███████╗  ░█████╗░██╗░░░██╗███████╗██████╗░
██╔════╝░██╔══██╗████╗░████║██╔════╝  ██╔══██╗██║░░░██║██╔════╝██╔══██╗
██║░░██╗░███████║██╔████╔██║█████╗░░  ██║░░██║╚██╗░██╔╝█████╗░░██████╔╝
██║░░╚██╗██╔══██║██║╚██╔╝██║██╔══╝░░  ██║░░██║░╚████╔╝░██╔══╝░░██╔══██╗
╚██████╔╝██║░░██║██║░╚═╝░██║███████╗  ╚█████╔╝░░╚██╔╝░░███████╗██║░░██║
░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝  ░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝\033[0m""")
    print("\033[93mEl ganador es: \033[0m",ganador)
    mainGuardar(partidasGuardadas,tablero,"","jugador blanco")
    input("Ingrese una tecla para continuar...")
    limpiarPantalla()




def consultaRey(tablero,partidasGuardadas):
    """DEVUELVE FALSE Y TERMINA LA PARTIDA EN CASO DE QUE ALGUNO DE LOS 2 REYES NO ESTE MAS EN EL TABLERO"""
    reyBlanco=False
    reyNegro=False
    consultaEnCurso=True
    while not reyBlanco and not reyNegro and consultaEnCurso:
        for i in range(0,len(tablero)):
            if "♕" in tablero[i]:
                reyBlanco=True
            elif "♛" in tablero[i]:
                reyNegro=True
        consultaEnCurso=False
    if reyBlanco==False:
        finDelJuego(tablero,partidasGuardadas,"Jugador negro.")
        return False
    elif reyNegro==False:
        finDelJuego(tablero,partidasGuardadas,"Jugador blanco.")
        return False
    else:
        return True


def juegoRecursivo(tablero,blancas,negras,numeroRonda,turno,partidasGuardadas):
    """FUNCION PRINICIPAL DEL FLUJO DEL JUEGO"""
    partidaEnCurso = True
    if partidaEnCurso:
        print("\033[93mRonda Numero: ", numeroRonda, "\033[0m")
        if turno=="jugador blanco":
            print("El turno es de: \033[94m", turno.upper(),"(Azul)\033[0m")
        else:
            print("El turno es de: \033[91m", turno.upper(),"(Rojo)\033[0m")
        imprimirTablero(tablero)
        print()
        jugada=elegirPieza(tablero,turno,blancas,negras)
        if jugada!="cerrarJuego":
            if jugada!="rendirse":
                partidaEnCurso = consultaRey(tablero, partidasGuardadas)
                if turno =="jugador blanco" and partidaEnCurso:
                    turno ="jugador negro"
                    limpiarPantalla()
                    juegoRecursivo(tablero, blancas, negras, numeroRonda, turno, partidasGuardadas)
                elif turno =="jugador negro" and partidaEnCurso:
                    turno = "jugador blanco"
                    limpiarPantalla()
                    juegoRecursivo(tablero, blancas, negras, numeroRonda+1, turno, partidasGuardadas)

            else:
                if turno == "jugador blanco":
                    finDelJuego(tablero,partidasGuardadas,"Jugador negro.")
                else:
                    finDelJuego(tablero, partidasGuardadas, "Jugador blanco.")
                partidaEnCurso=False
        else:
            print("Guardando juego...")
            mainGuardar(partidasGuardadas,tablero,numeroRonda,turno)
            partidaEnCurso=False

def crearPartida(partidasGuardadas):
    fichasBlancas = ["♙", "♖", "♘", "♗", "♔", "♕", "♗", "♘", "♖"]
    fichasNegras = ["♟", "♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"]
    tablero=crearMatriz()
    llenarTableroInicial(tablero,fichasBlancas,fichasNegras)
    limpiarPantalla()
    juegoRecursivo(tablero,fichasBlancas,fichasNegras,1,"jugador blanco",partidasGuardadas)


def cargarPartida(path,partidasGuardadas):
    print("Sistema: Cargando partida")
    fichasBlancas = ["♙", "♖", "♘", "♗", "♔", "♕", "♗", "♘", "♖"]
    fichasNegras = ["♟", "♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"]
    tablero = crearMatriz()
    numRonda,turno=cargarTablero(tablero,fichasBlancas,fichasNegras,path,partidasGuardadas)
    numRonda=int(numRonda)
    limpiarPantalla()
    imprimirTablero(tablero)
    juegoRecursivo(tablero, fichasBlancas, fichasNegras,numRonda,turno,partidasGuardadas)




def menuCargarPartida(partidasGuardadas):
    limpiarPantalla()
    print("\033[96mListado de partidas\033[0m")
    print("\033[94mPara volver al menu anterior ingrese 0\033[0m")
    for elem in list(partidasGuardadas.keys()):
        print(list(partidasGuardadas.keys()).index(elem)+1,"-",elem)
    estado=False
    while not estado:
        try:
            opcion = int(input("\033[96mIngrese el numero de partida deseado: \033[0m"))
            if opcion==0:
                estado=True
                limpiarPantalla()
            elif 0<opcion<=len(list(partidasGuardadas.keys())):
                path=partidasGuardadas[list(partidasGuardadas.keys())[opcion-1]]
                cargarPartida(path,partidasGuardadas)
                estado=True
            else:
                error("Error: El numero ingresado no pertenece al listado de partidas guardadas")
        except ValueError as mensaje:
            print("Error: El numero ingresado no pertenece al listado de partidas guardadas",mensaje)
        except TypeError as mensaje:
            print("Error: El numero ingresado no pertenece al listado de partidas guardadas",mensaje)

def menuInicial():
    bienvenida()
    print("""
    \033[96m
    AJEDREZ v1.0 - Grupo 2 \033[0m
    --Recomendamos la ejecucion de este programa en el entorno de desarrollo PyCharm--
    1 - Iniciar una partida nueva
    2 - Cargar una partida vieja
    3 - Salir""")


def iniciarMenu(partidasGuardadas):
    menu=True
    while menu:
        menuInicial()
        if len(list(partidasGuardadas.keys())) > 0:
            print("\033[94m Se han detectado",len(list(partidasGuardadas.keys())),"partidas por terminar. puedes renaudarlas seleccionando la segunda opcion del menu \033[0m")
        opcion=input("\033[96m Seleccione una opcion: \033[0m")
        if opcion=="1":
            crearPartida(partidasGuardadas)
            #menu=False
        elif opcion=="2":
            menuCargarPartida(partidasGuardadas)
            #menu=False
        else:
            error("Error: Opcion invalida")


def main():
    partidasGuardadas={}
    mergePartidas(partidasGuardadas)
    iniciarMenu(partidasGuardadas)

main()