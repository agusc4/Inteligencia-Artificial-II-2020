import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

CONSTANTE_M = 2 # Masa del carro
CONSTANTE_m = 1 # Masa de la pertiga
CONSTANTE_l = 1 # Longitud dela pertiga

# Simula el modelo del carro-pendulo.
# Parametros:
#   t_max: tiempo maximo (inicia en 0)
#   delta_t: incremento de tiempo en cada iteracion
#   theta_0: Angulo inicial (grados)
#   v_0: Velocidad angular inicial (radianes/s)
#   a_0: Aceleracion angular inicial (radianes/s2)

# Calcula la aceleracion en el siguiente instante de tiempo dado el angulo y la velocidad angular actual, y la fuerza ejercida
def calcula_aceleracion(theta, v, f):
    numerador = constants.g * np.sin(theta) + np.cos(theta) * ((-f - CONSTANTE_m * CONSTANTE_l * np.power(v, 2) * np.sin(theta)) / (CONSTANTE_M + CONSTANTE_m))
    denominador = CONSTANTE_l * (4/3 - (CONSTANTE_m * np.power(np.cos(theta), 2) / (CONSTANTE_M + CONSTANTE_m)))
    return numerador / denominador

class fuz:
  def __init__(self,dominio):
    self.dominio=dominio
    self.conjunto=list
    self.PF=list

  def fuzyfy(self): #el dominio esta considerado con solapamiento de 50% 
    intervalo=(self.dominio[1]-self.dominio[0])/5 #defino 5 intervalos Ng,np,z,pp,pg
    Z=[-intervalo,intervalo]
    PP=[0,2*intervalo]
    PG=[intervalo,self.dominio[1]]
    NP=[-2*intervalo,0]
    NG=[self.dominio[0],-intervalo]
    self.conjunto=[NG,NP,Z,PP,PG]
    return self.conjunto



  def valor_pertenencia(self,x):
    i=0
    pertenencia=[0,0,0,0,0]
    for intr in self.conjunto: #analiza en orden NG,NP,Z,PP,PG para saber en cuales esta numero y les asigna su valor de pertenencia. 
      a=intr[0] #extremo menor
      c=intr[1] #extremo mayor
      b=(a+c)/2 #centro
      if x<a:
        pertenencia[i]=0
      if a<=x<=b:
        if i==0:
          pertenencia[0]=1
        else:
          pertenencia[i]=(x-a)/(b-a)
      if b<x<=c:
        if i==4:
          pertenencia[4]=1
        else:
          pertenencia[i]=(x-c)/(b-c)
      if x>c:
        pertenencia[i]=0
      i=i+1    
    return pertenencia



  def tabla(self,ptita,pomega): #ingreso el valor de pertenencia de tita y tita' para obtener los valores de pertenencia de la Fuerza
    F=[0,0,0,0,0]
    #las 25 sentencias de mi tabla FAM
    #columna de tita NG
    if ptita[0]!=0 and pomega[0]!=0: #NG
      minimo=min(ptita[0],pomega[0])
      F[4]=max(minimo,F[4])
    if ptita[0]!=0 and pomega[1]!=0: #NP
      minimo=min(ptita[0],pomega[1])
      F[4]=max(minimo,F[4])
    if ptita[0]!=0 and pomega[2]!=0: #Z
      minimo=min(ptita[0],pomega[2])
      F[4]=max(minimo,F[4])
    if ptita[0]!=0 and pomega[3]!=0: #PP
      minimo=min(ptita[0],pomega[3])
      F[3]=max(minimo,F[3])
    if ptita[0]!=0 and pomega[4]!=0: #PG
      minimo=min(ptita[0],pomega[4])
      F[2]=max(minimo,F[2])
    
    #columna de tita NP
    if ptita[1]!=0 and pomega[0]!=0: #NG
      minimo=min(ptita[1],pomega[0])
      F[4]=max(minimo,F[4])
    if ptita[1]!=0 and pomega[1]!=0: #NP
      minimo=min(ptita[1],pomega[1])
      F[4]=max(minimo,F[4])
    if ptita[1]!=0 and pomega[2]!=0: #Z
      minimo=min(ptita[1],pomega[2])
      F[3]=max(minimo,F[3])
    if ptita[1]!=0 and pomega[3]!=0: #PP
      minimo=min(ptita[1],pomega[3])
      F[2]=max(minimo,F[2])
    if ptita[1]!=0 and pomega[4]!=0: #PG
      minimo=min(ptita[1],pomega[4])
      F[4]=max(minimo,F[4])

    #columna de tita Z
    if ptita[2]!=0 and pomega[0]!=0: #NG
      minimo=min(ptita[2],pomega[0])
      F[4]=max(minimo,F[4])
    if ptita[2]!=0 and pomega[1]!=0: #NP
      minimo=min(ptita[2],pomega[1])
      F[4]=max(minimo,F[4])
    if ptita[2]!=0 and pomega[2]!=0: #Z
      minimo=min(ptita[2],pomega[2])
      F[2]=max(minimo,F[2])
    if ptita[2]!=0 and pomega[3]!=0: #PP
      minimo=min(ptita[2],pomega[3])
      F[1]=max(minimo,F[1])
    if ptita[2]!=0 and pomega[4]!=0: #PG
      minimo=min(ptita[2],pomega[4])
      F[0]=max(minimo,F[0])

   #columna de tita PP
    if ptita[3]!=0 and pomega[0]!=0: #NG
      minimo=min(ptita[3],pomega[0])
      F[3]=max(minimo,F[3])
    if ptita[3]!=0 and pomega[1]!=0: #NP
      minimo=min(ptita[3],pomega[1])
      F[2]=max(minimo,F[2])
    if ptita[3]!=0 and pomega[2]!=0: #Z
      minimo=min(ptita[3],pomega[2])
      F[1]=max(minimo,F[1])
    if ptita[3]!=0 and pomega[3]!=0: #PP
      minimo=min(ptita[3],pomega[3])
      F[0]=max(minimo,F[0])
    if ptita[3]!=0 and pomega[4]!=0: #PG
      minimo=min(ptita[3],pomega[4])
      F[0]=max(minimo,F[0])

    #columna de tita PG
    if ptita[4]!=0 and pomega[0]!=0: #NG
      minimo=min(ptita[4],pomega[0])
      F[2]=max(minimo,F[2])
    if ptita[4]!=0 and pomega[1]!=0: #NP
      minimo=min(ptita[4],pomega[1])
      F[0]=max(minimo,F[0])
    if ptita[4]!=0 and pomega[2]!=0: #Z
      minimo=min(ptita[4],pomega[2])
      F[0]=max(minimo,F[0])
    if ptita[4]!=0 and pomega[3]!=0: #PP
      minimo=min(ptita[4],pomega[3])
      F[0]=max(minimo,F[0])
    if ptita[4]!=0 and pomega[4]!=0: #PG
      minimo=min(ptita[4],pomega[4])
      F[0]=max(minimo,F[0])
    PF=F
    aux1=[0,0,0,0,0]
    #calculo por media de centros
    for i in range(5):
      if PF[i]!=0:
        conjunto=self.conjunto[i]
        centro=(conjunto[0]+conjunto[1])/2
        aux1[i]=centro*PF[i]
    if sum(aux1)!=0 and sum(PF)!=0:
      mediadc=sum(aux1)/sum(PF)
    else:
      mediadc=0
    return mediadc
   
def simular(t_max, delta_t, theta_0, v_0, a_0):
  theta = (theta_0 * np.pi) / 180
  v = v_0
  a = a_0
  vel=[]
  fuerza=[]
  dom = (120 * np.pi) / 180
  theta_dominio=(-dom,dom)
  theta_prima_dominio=(-6,6)
  fuerza_dominio=(-300,300)
  D1=fuz(theta_dominio)
  D2=fuz(theta_prima_dominio)
  D3=fuz(fuerza_dominio)
  CD1=D1.fuzyfy()
  CD2=D2.fuzyfy()
  CD3=D3.fuzyfy()
 
  # Simular
  y = []
  x = np.arange(0, t_max, delta_t)
  f=0
  for t in x:
    a = calcula_aceleracion(theta, v, -f)
    v = v + a * delta_t
    vel.append(v)
    theta = theta + v * delta_t + a * np.power(delta_t, 2) / 2
    y.append(theta*180/np.pi)
    aux1=D1.valor_pertenencia(theta)
    aux2=D2.valor_pertenencia(v)
    f=D3.tabla(aux1,aux2)
    fuerza.append(f)
  
  plt.figure(1)
  plt.plot(x,y)
  plt.grid()
  plt.title("Valor de posicion")
  plt.xlabel("tiempo (s)")
  plt.ylabel("tita")
  plt.figure(2)
  plt.plot(x,fuerza)
  plt.xlabel("tiempo (s)")
  plt.ylabel("tita_p")
  plt.grid()
  plt.title("Valor de fuerza")
  plt.figure(3)
  plt.title("Valor de velocidad")
  plt.xlabel("tiempo (s)")
  plt.ylabel("F")
  plt.plot(x,vel)
  plt.grid()

  plt.show()
  



simular(10, 0.0001, 65, -1, 0)
