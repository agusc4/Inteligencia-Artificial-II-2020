import random
import matplotlib.pyplot as plt

#El codigo en un principio fue implementado para funcionar con tareas que involucren mas de una maquina, es decir multiples pasos para poder terminarlas.
#Durante el proceso esto cambio y solo resuelve tareas que usan una sola maquina. Pero el codigo todavia posee estructuras del codigo viejo que lo pueden hacer ver confuso. 

class PSR:
    def __init__(self,lt,lm):
        self.lt=lt #lista de tareas formato (tipo,duracion)
        self.lm=lm #lista de maquinas formato(tipo,hasta cuando estan ocupadas)
        self.ordenaseguir=[] #todos los pasos se guardan aca en formato [maquina, tarea, paso de la tarea]
        self.tordenadas=self.lt.copy()
        self.espera=[]
    
    def ordenar(self):
        index=0  
        elemento=[]
        tordenadas2=[]
        AA=[]
        BB=[]
        CC=[]
        DD=[]
        aux1=[]
        aux=[0,0,0,0]
        self.tordenadas.sort() #ordenamos primero de mayor a menor duracion
        for i in self.tordenadas:#ordenamos por tipo de tareas de mayor a menor
            if i[0][1]=='A':
                AA.append(i)
            if i[0][1]=='B':
                BB.append(i)
            if i[0][1]=='C':
                CC.append(i)
            if i[0][1]=='D':
                DD.append(i)
        aux[0]=len(AA)
    
        aux[1]=len(BB)
       
        aux[2]=len(CC)
        
        aux[3]=len(DD)
        i=0
        flag=True
        while flag:
            if i==len(aux):         
                i=0
            if aux[i]==max(aux):
                if i==0 and aux[i]!=0:
                    tordenadas2+=AA
                    aux[i]=0
                if i==1 and aux[i]!=0:
                    tordenadas2+=BB
                    aux[i]=0
                if i==2 and aux[i]!=0:
                    tordenadas2+=CC
                    aux[i]=0
                if i==3 and aux[i]!=0:
                    tordenadas2+=DD
                    aux[i]=0
            if sum(aux)==0:
                flag=False
            i=i+1

        self.tordenadas=tordenadas2

            
    def restaurar(self,periodo):
        aux0=[] #las tareas que estan en maquinas y todavia faltan pasos por terminar. Estan en espera hasta que la maquina termina
        for i in self.espera: #cuando la maquina termino sale de espera y vuelve a la lista de tareas para ser ordenada
            if i[0]==periodo:
                self.tordenadas.append(i[1]) #la devuelve a la lista
                aux0.append(i)

        for i in aux0:
            self.espera.remove(i) #la saca de la lista de espera
  
    def ini(self):  #donde la magia sucede
        periodo=-1 #elemento que define el periodo de nuestro problema
        flag=True #flag para hacer doble break. 
       
        while len(self.tordenadas)!=0 or len(self.espera)!=0: #mientras haya alguna tarea en espera o en la lista ordenada el loop continua
            periodo=periodo+1 #avanza el tiempo
            self.restaurar(periodo) #revisamos si hay algo por restaurar
            self.ordenar() #ordenamos la lista de tareas
            aux3=[]
            for i in range(len(self.tordenadas)):
                for maquina in self.lm: #para cada maquina de la lista
                    if flag==False:
                        flag=True
                        break
                    for paso in self.tordenadas[i]: #comparo todas las maquinas con los pasos de la primer tarea en prioriedad
                        if maquina[1]<=periodo: #si la maquina esta disponible para el periodo actual sigo
                            if maquina[0]==paso[1] or maquina[2]==paso[1] or maquina[3]==paso[1]: #si la maquina es del tipo de la tarea que analizo sigo
                                rt=[]
                                rt.append((maquina,self.tordenadas[i],paso))
                                self.ordenaseguir.append((maquina[0], self.tordenadas[i], paso, periodo))#info por si se quiere hacer seguimiendo dle orden de tareas
                                maquina[1]=periodo+paso[0] #le ponemos hasta que periodo va a estar ocupada la maquina
                                aux1=self.tordenadas[i].copy() #creo una copia de la tarea
                                aux1.remove(paso) #a la copia le saco el paso que esta en proceso
                                aux3.append(i) #agrego indice de tarea a sacar de la lista, lo hago al final de todo
                                if aux1: #una lista con algo siempre tira true
                                    self.espera.append((maquina[1],aux1)) #ingreso a la cola de espera los pasos restantes de la tarea con el valor de cuando volveran a la lista de tareas.
                                flag=False
                                break
            aux3.sort(reverse=True)
            for i in aux3:
                self.tordenadas.pop(i) #sacamos las tareas q pasaron a espera
        
        frodo=self.lm.copy() #frodo controla las maquinas que todavia no terminaron su tarea.

        while len(frodo)!=0: 
            sam=[] #sam fiel compañero de frodo
            for ring in frodo: #por cada ring (maquina) que lleva frodo
                if ring[1]<=periodo:#revisamos si es el periodo de darselo a su portador
                   sam.append(ring) #sam va a llevar los anillos, pues frodo tiene la dificil tarea de llevar el anillo unico
            for ring in sam: 
                frodo.remove(ring)#sam se queda con los anillos
            periodo=periodo+1 #avanzan los dias               
        #for orden in self.ordenaseguir: 
            #print(orden)
        #print("La ultima maquina se ha liberado en el periodo: ", periodo)
        return periodo

        
if __name__ == "__main__":
    
    
    cantidad=int(input("Cuantas tareas aleatorias desea resolver?: "))
    duraciones=[]
    resultado=[]
    k=[]
    for j in range(100):
        k.append(j)
        tarea=[]
        for i in range(cantidad):
            tipos=['A','B','C','D']
            aux=1
            pasos=[]
            for i in range(aux):
                aux1=random.randint(1,10)
                aux2=random.choice(tipos)
                tipos.remove(aux2)      
                pasos.append((aux1,aux2))
                tarea.append(pasos)
                print(i)
        Aa=Bb=Cc=Dd=0
        for ww in tarea:
            for www in ww:
                if www[1]=='A':
                    Aa=Aa+www[0]
                if www[1]=='B':
                    Bb=Bb+www[0]
                if www[1]=='C':
                    Cc=Cc+www[0]
                if www[1]=='D':
                    Dd=Dd+www[0]

        duraciones.append(max(Aa,Bb,Cc,Dd))

        lt=tarea
        lm=[['A',0,'A','A'],['B',0,'C','A'], ['C',0,'D','D'],['D',0,'D','D']]
        y=PSR(lt,lm)
        resultado.append(y.ini())
    suma1=sum(resultado)/100
    suma2=sum(duraciones)/100
    plt.plot(k,resultado)
    plt.plot(k,duraciones)
    
    plt.legend(["resultado","mayor duracion"])
    
    print("promedio de resultados",suma1)
    print("promedio de valores maximos",suma2)
    plt.show()
