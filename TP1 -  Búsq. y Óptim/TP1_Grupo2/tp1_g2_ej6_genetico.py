import math
import random
from matplotlib import pyplot as plt
import numpy as np

class Node:
    def __init__(self, pos, meta, padre=None):  # el nodo esta compuesto de su ubicacion, cual es su padre, y los valores de f,g y h
        self.pos = pos
        self.padre = padre

        if self.padre == None:
            self.g = 0
            self.meta = tuple(meta)
        else:
            self.g = self.padre.g + 1
            self.meta = self.padre.meta

        self.h = distancia(self.pos, self.meta)
        self.f = self.g + self.h


def distancia(a, b):  ## se calcula la distancia euclidiana entre dos puntos

    var0 = (a[0] - b[0]) ** 2
    var1 = (a[1] - b[1]) ** 2
    resultado = math.sqrt(var0 + var1)
    return resultado


class aestrella:
    def __init__(self, inicio, meta, entorno):
        self.inicio = inicio
        self.var = entorno
        self.meta = (meta[0],meta[1])
        self.listb = []
        self.listaa = []
        self.listac = []


    def bloqueado(self, filas, columnas):
        a = 1
        for j in range(columnas):
            b=1
            for i in range(filas):
                self.listb.append((a, b))
                self.listb.append((a + 1, b))
                self.listb.append((a, b + 1))
                self.listb.append((a + 1, b + 1))
                self.listb.append((a, b + 2))
                self.listb.append((a + 1, b + 2))
                self.listb.append((a, b + 3))
                self.listb.append((a + 1, b + 3))
                b = b + 6

            a = a + 4


    def iniciar(self):

        self.listac.append(Node(self.inicio, self.meta))
        self.listaa += self.crearhijo(Node(self.inicio, self.meta, self.listac[0]))
        
        while self.final():
            self.buscar()
                    
        self.camino = self.desplazamiento()
        return len(self.camino)

    def crearhijo(self, node):  ##Expande un nodo analizando sus vecinos en sus posiciones verticales y horizontales. No busca en diagonal.
        vecinospos=[]
        vecinos=[]
        for v in [(-1,0),(1,0),(0,-1),(0,1)]:
            vecinospos.append((node.pos[0] + v[0], node.pos[1] + v[1]))

        for pos in vecinospos:
            if pos in self.listb:
                vecinospos.remove(pos)

        for pos in vecinospos:
            if pos[0] < 0 or pos[1] < 0:
                vecinospos.remove(pos)

        for pos in vecinospos:
            if pos[0] > self.var[0] or pos[1] > self.var[1]:
                vecinospos.remove(pos)

        for pos in vecinospos:
            vecinos.append(Node(pos, self.meta, node))

        return vecinos

    def repetidos(self, node, lista):  # revisa si un nodo en particular esta en una lista. devolviendo true (1) o false (0)
        for i in range(len(lista)):
            if node.pos == lista[i].pos:
                return 1

        return 0

    def fmenor(self):  # el llamado a la funcion analiza la lista abierta, busca el nodo con menor valor de f, lo agrega a la lista cerrada y lo borra de la lista abierta.
        a = self.listaa[0]  # esta funcion se utiliza en buscar
        n = 0
        for i in range(1, len(self.listaa)):
            if self.listaa[i].f < a.f:
                a = self.listaa[i]
                n = i
        self.listac.append(a)  # se agrega a lista cerrada
        del self.listaa[n]  # se borra de lista abierta

    def final(self):  # si la meta esta dentro de la lista abierta devuelve false para romper el while
        for i in range (len(self.listaa)):
            if self.meta == self.listaa[i].pos:
                return 0

        return 1

    def trayectoria(self):  # se utiliza en la funcion buscar

        for i in range(len(self.candidatos)):  # con la lista de nodos vecinos al ultimo elemento de la listac
            if self.repetidos(self.candidatos[i],
                              self.listac):  # si uno de estos vecinos ya se encuentra en la listac se continua el programa
                continue
            elif not self.repetidos(self.candidatos[i],
                                    self.listaa):  # si uno de los candidatos no esta en la lista abierta se lo agrega a ella
                self.listaa.append(self.candidatos[i])
            else:
                if self.ultimolc.g + 1 < self.candidatos[i].g:  # si ya esta en la lista abierta, se compara el valor de los candidatos con el de el ultimolc+1
                    for j in range(len(self.listaa)):
                        if self.candidatos[i].pos == self.listaa[j].pos:
                            del self.listaa[j]
                            self.listaa.append(self.candidatos[i])
                            break

    def buscar(self):  # se pone en lista cerrada el elemento de menor f de la lista abierta
        # self.youshouldnotpass1()
        self.fmenor()
        self.ultimolc = self.listac[-1]  # se identifica el ultimo elemento de la lsita cerrada
        self.candidatos = self.crearhijo(self.ultimolc)  # se analizan los nodos vecinos y son llamados candidatos para seguir la busqueda
        # self.youshouldnotpass2()
        self.trayectoria()  # es el camino de todos los nodos visitados no el directo

    def desplazamiento(self):
        for i in range(len(self.listaa)):
            if self.meta == self.listaa[i].pos:
                objetivo = self.listaa[i]

        camino = []

        while objetivo.padre != None:
            camino.append(objetivo.pos)
            objetivo = objetivo.padre
        camino.reverse()
        return camino

class Recolector:
    def __init__(self, objetos, filas, columnas,ordenamientonew=None):  #le ingreso las dimensiones de los estantes para saber forma del mapa
        self.listobj = objetos #lista con los objetos a recolectar por su numero de estante
        self.filas=filas
        self.columnas=columnas
        self.listestantes =[]
        self.articulos=[] #lista que tiene los objetos por numero de estante y la posicion de ese estante
        self.target=[] #lista de las posiciones que tiene que ser recorrida para caer frente al numero de estante
        self.mapa = [4*columnas, 6*filas]
        self.ordenamientonew=ordenamientonew


    def calcd(self):
        self.estantes(self.filas, self.columnas)
        self.calcpos()
        caminod = 0


        for i in range(len(self.target)):
            if i == 0:
                meta=self.target[i]
                a = aestrella([0, 0], meta, self.mapa)
                a.bloqueado(self.filas, self.columnas)
                caminod = a.iniciar() + caminod
            if i > 0:
                meta=self.target[i]
                a = aestrella(self.target[i-1], meta, self.mapa)
                a.bloqueado(self.filas, self.columnas)
                caminod = a.iniciar() + caminod
            if i == len(self.target):
                meta=(0,0)
                a = aestrella(self.target[i], meta, self.mapa)
                a.bloqueado(self.filas, self.columnas)
                caminod = a.iniciar() + caminod
        return caminod
    
    def calcdgenetico(self):
        self.estategenetico()
        self.calcpos()
        caminod = 0


        for i in range(len(self.target)):
            if i == 0:
                meta=self.target[i]
                a = aestrella([0, 0], meta, self.mapa)
                a.bloqueado(self.filas, self.columnas)
                caminod = a.iniciar() + caminod
            if i > 0:
                meta=self.target[i]
                a = aestrella(self.target[i-1], meta, self.mapa)
                a.bloqueado(self.filas, self.columnas)
                caminod = a.iniciar() + caminod
            if i == len(self.target):
                meta=(0,0)
                a = aestrella(self.target[i], meta, self.mapa)
                a.bloqueado(self.filas, self.columnas)
                caminod = a.iniciar() + caminod
        return caminod

    def calcpos(self):
        aux=[]
        for n in self.listobj:
            for elemento in self.listestantes:
                if n in elemento:
                    self.articulos.append(elemento)   #partiendo de los numeros de objeto obtengo su posicion

        for n in self.articulos:
            if n[0][0] % 2 == 0:
                aux = n[0]
                aux =(aux[0] + 1, aux[1])
                self.target.append(aux)

            if n[0][0] % 2 != 0:
                aux = n[0]
                aux = (aux[0] - 1, aux[1])
                self.target.append(aux)

    def estategenetico(self): #los estantes ya no tienen el orden normal lo tienen en funcion del nuevo individuo ordenamientonew
        a = 1
        d=0
        h=self.ordenamientonew
        for j in range(self.columnas):
            b=1
            for i in range(self.filas):
                self.listestantes.append(((a, b), h[d])) #la posicion corresponde al antiguo 1 (para la primer iteracion) pero ahora en su lugar tendra el numero del h[d]
                self.listestantes.append(((a + 1, b), h[d+1]))
                self.listestantes.append(((a, b + 1), h[d+2]))
                self.listestantes.append(((a + 1, b + 1), h[d+3]))
                self.listestantes.append(((a, b + 2), h[d+4]))
                self.listestantes.append(((a + 1, b + 2), h[d+5]))
                self.listestantes.append(((a, b + 3), h[d+6]))
                self.listestantes.append(((a + 1, b + 3), h[d+7]))
                b = b + 6
                d = d + 8
            a = a + 4

    def estantes(self, filas, columnas):
        a = 1
        n = 1
        for j in range(columnas):
            b=1
            for i in range(filas):
                self.listestantes.append(((a, b), n))
                self.listestantes.append(((a + 1, b), n + 1))
                self.listestantes.append(((a, b + 1), n + 2))
                self.listestantes.append(((a + 1, b + 1), n + 3))
                self.listestantes.append(((a, b + 2), n + 4))
                self.listestantes.append(((a + 1, b + 2), n + 5))
                self.listestantes.append(((a, b + 3), n + 6))
                self.listestantes.append(((a + 1, b + 3), n + 7))
                b = b + 6
                n = n + 8
            a = a + 4

class Temple:

    def __init__(self, Ti, Si, enfriamiento, tfinal):
        self.soluini = Si
        self.tempi = Ti
        self.enfriamiento = enfriamiento
        self.tfinal = tfinal
        
    def parametrosrecolector(self, filas, columnas,individuo):
        self.filas = filas
        self.columnas = columnas
        self.individuo=individuo

    def calculo(self, evaluar):
        self.evaluar = evaluar
        q = Recolector(self.evaluar, self.filas, self.columnas, self.individuo)
        costo=q.calcdgenetico()
        return costo

    def permutacion(self, x, n):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        while i == j:
            j = random.randint(0, n - 1)

        aux = x[j]
        x[j] = x[i]
        x[i] = aux

        return x


    def iniciar(self):
        temp = self.tempi
        j = 0
        vecinos=[]
        permutado=self.soluini
        vecinos.append(permutado)
        s1 = self.calculo(vecinos[0])
        while temp >= self.tfinal:
            j=j+1
            permutado = self.permutacion(permutado, len(permutado))
            vecinos.append(permutado)
            s2 = self.calculo(vecinos[j])
            if s1 >= s2:
                s1 = s2
            else:
                e=math.exp((s1-s2)/temp)
                if e > random.random():
                    s1 = s2
            
            temp=temp*self.enfriamiento
        return s1


class Genetico:
    def __init__(self, poblacion,nordenes,nobjetos,mapa):
        self.size_poblacion=poblacion #tamaño que deseo que tenga la poblacion
        self.poblacion=[] #se compone de los individuos que son los estantes en un distinto orden de numeracion
        self.nordenes=nordenes #cuantas ordenes deseo que tenga el calcula
        self.nobjetos=nobjetos #cuantos objetos quiero que tenga cada orden
        self.map=mapa #filas y columnas de estantes, el entorno es creado en base a estos parametros
        self.list_ordenes=[]#adentro de esta lista hay tuplas que cada una se compone de los numeros de los elementos a recolectar
        self.oldgeneration=[]
    def obyord(self): #objetos y ordenes
        limite=self.map[0]*self.map[1]*8 #estoy calculando el numero max de objeto
             
        for j in range(self.nordenes): #por la cantidad de ordenes las crea 
            orden=[]
            for i in range(self.nobjetos): #por la cantidad de objetos crea una orden con numeros random entre 1 y limite
                flag=True
                while flag:
                    aux=random.randint(0,limite) #numero random entre 0 y limite
                    if aux not in orden: #si el numero todavia no esta en la orden lo agrega
                        orden.append(aux)
                        flag=False
            self.list_ordenes.append(orden)#la orden se agrega al pedido que tendra guardada el conjunto de las n ordenes
            #print(len(self.list_ordenes))
    
    def armado_poblacion(self): #numero de estantes en otro orden cantidad igual a la que yo le pido en poblacion
        original=[]
        for i in range (self.map[0]*self.map[1]*8): #numeracion de estantes en orden original
            original.append(i+1)
        
        for i in range(self.size_poblacion): #parametro del tamaño de la poblacion
            copia=original.copy()
            self.poblacion.append(copia)
            random.shuffle(original)


    def fitness(self): #para cada pedido le calcula el costo de camino, devuelve la suma de todos los pedidos (poblacion)
        self.fitnes_poblacion=[]
        for individuo in self.poblacion: #lista con cada combinacion de nueva distribucion de estantes
            sumatoria=0
            for orden in self.list_ordenes: #a cada orden en la lista se le calcula el costo con la distribucion 
                a=Temple(300,orden,0.8,0.00001)#de estantes del individuo.
                a.parametrosrecolector(self.map[0],self.map[1],individuo)
                sumatoria=a.iniciar()+sumatoria
            self.fitnes_poblacion.append(sumatoria) #en esta lista se almacena el costo total de la lista de ordenes para una un individuo determinado.  fitnes_poblacion[n] corresponde a poblacion[n]
        return sum(self.fitnes_poblacion)

    def crossover(self):
        cantidad = self.size_poblacion/2 #al tamaño de la poblacion lo divido a la mitad seran mis nuevos padres
        i=0
        j=0
        seleccionados=[] #aca guardo los indices que corresponden a los individuos de la poblacion seleccionados
        if cantidad % 2 !=0:
            cantidad= cantidad + 0.5 #si la cantidad no es par la hago par
        pob_orden = sorted(self.fitnes_poblacion)
        while len(seleccionados)<cantidad: #hasta que la lista de seleccionados no sea igual a la cantidad requerida se sigue
            if i==len(self.fitnes_poblacion):  #en caso de que se haya dado la vuelta y no esten seleccionados todos
                i=0 #se empieza nuevamente del comienzo a seleccionar
            if pob_orden[i] == self.fitnes_poblacion[j]:
                seleccionados.append(j)
                i = i + 1
                j=0
            else:
                j=j+1

        p=0
        newgeneration=[]
        for b in range(int(cantidad)):
            padre1=self.poblacion[seleccionados[p]]
            padre2=self.poblacion[seleccionados[p+1]]
            dim = len(padre1)
            corte1 = random.randint(0, dim - 1)
            corte2 = random.randint(0, dim - 1)
            int_corte1 = []
            int_corte2 = []
            hijo1 = [None] * dim
            hijo2 = [None] * dim

            while corte2 == corte1:
                corte2 = random.randint(0, dim - 1)
            if corte1 > corte2:  # Me aseguro que corte1 sea menor que corte2
                temp = corte1
                corte1 = corte2
                corte2 = temp

            for pos in range(corte1 + 1,corte2 + 1):
                hijo1[pos] = padre2[pos]
                int_corte1.append(padre2[pos])
                hijo2[pos] = padre1[pos]
                int_corte2.append(padre1[pos])

            q = corte2 + 1
            i = 0
            h = corte2 + 1
            while (h <= dim) and (q <= dim) and (i < len(int_corte1)):
                if q == dim:
                    q = 0
                if padre1[q] == int_corte1[i]:
                    q = q + 1
                    i = 0
                else:
                    i = i + 1
                    if i == len(int_corte1):
                        if h == dim:
                            h = 0
                        if hijo1[h] == None:
                            hijo1[h] = padre1[q]
                            h = h + 1
                            q = q + 1
                            i = 0
                        else:
                            break

            q = corte2 + 1
            i = 0
            h = corte2 + 1
            while (h <= dim) and (q <= dim) and (i < len(int_corte2)):
                if q == dim:
                    q = 0
                if padre2[q] == int_corte2[i]:
                    q = q + 1
                    i = 0
                else:
                    i = i + 1
                    if i == len(int_corte2):
                        if h == dim:
                            h = 0
                        if hijo2[h] == None:
                            hijo2[h] = padre2[q]
                            h = h + 1
                            q = q + 1
                            i = 0
                        else:
                            break

            t=Temple(300,[0,0],0.8,0.00001)
            hijo1_mutado = t.permutacion(hijo1, len(hijo1))
            hijo2_mutado = t.permutacion(hijo2, len(hijo2))

            newgeneration.append(hijo1_mutado)
            newgeneration.append(hijo2_mutado)

        self.oldgeneration=self.poblacion.copy()
        self.poblacion=newgeneration

    def graficar(self, vector):
        it = np.linspace(0,1,len(vector))

        plt.plot(it, vector)
        plt.xlabel("ITERACIONES")
        plt.ylabel("FITNESS")
        plt.text(70, 0.8, "POBLACION DE 4 INDIVIDUOS")
        plt.text(65, 0.8, "10 GENERACIONES")
        plt.grid()
        plt.show()


    def iniciar(self):
        #introducir parametros.
        self.obyord()
        self.armado_poblacion()
        prom_fit = []
        i=0
        comparar=[0,0]
        comparar[1]=self.fitness() #guardo el valor antes de  hacer el primer cruzamiento
        j=0
        flag=True
        while i<100 or flag:
            comparar[0]=comparar[1]
            self.crossover() #realizo el primer cruzamiento como resultado la poblacion se va a ver alterada
            comparar[1]=self.fitness()#calculo el fitness de la nueva poblacion
            diferencia=(abs(comparar[0]-comparar[1]))/(comparar[0]+comparar[1]) #calculo en cuanto variaron la poblacion pre y pos cruce
            if diferencia<5: #si ha variado menos del n % detengo el algoritmo
                flag=False
            fit=0
            for f in self.fitnes_poblacion:
                fit = fit + f
            fit = fit/len(self.fitnes_poblacion)
            prom_fit.append(fit)
            i=i+1

        mejor_sol_fit = min(self.fitnes_poblacion)
        mejor_sol = []
        m=0
        while len(mejor_sol)==0:
            if self.fitnes_poblacion[m] == mejor_sol_fit:
                mejor_sol = self.poblacion[m]
            m=m+1

        resultado=[]
        resultado.append(mejor_sol)
        resultado.append(mejor_sol_fit)
        self.graficar(prom_fit)

        print("La última generción es {} y cada una tiene un fitness de {}" .format(self.poblacion, self.fitnes_poblacion))
        return resultado


if __name__ == "__main__":
    resultado = []
    a=Genetico(4,4,3,[2,2])
    resultado = a.iniciar()

    print("La mejor solución es {} y tiene un valor de fitness de {}" .format(resultado[0],resultado[1]))

