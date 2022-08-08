from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import numpy as np

raw_data = open('Dat9500.csv', 'rt') #abro el archivo
data_set = np.loadtxt(raw_data, delimiter=",") #lo cargo y defino que los datos estan separados por ,
x_cen=data_set-data_set.mean(axis=0) #
data_set=x_cen/x_cen.max(axis=0)
x=data_set[:,0:4]
t=data_set[:,4]
print(x.shape)
print(t.shape)

model= Sequential() #se define a model como una red neuronal secuencial
model.add(Dense(8, input_dim=4, activation='sigmoid')) #se define a la entrada de 4 variables y la primer capa oculta tendra 8 neuronas con funcion de activacion relu
model.add(Dense(1)) #se define 1 salida
model.compile(loss='mean_squared_error') #definimos cual sera el loss para nuetras red
history=model.fit(x,t,validation_split=0.2,epochs=50) #entrenamos el modelo dando los datos, los targets, diciendo que un 20% de los ejemplos sean usados para validacion y el numero de epochs
scores=model.evaluate(x,t)

#grafica de variacion de loss entre training y validacion para cada epoch

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['Entrenamiento','Validacion'])
plt.show()