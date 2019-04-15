import pandas

from numpy import array

from matplotlib import pyplot

from keras.layers import LSTM, Dense, Dropout
from keras.models import Model
from keras.engine.input_layer import Input
from keras.utils import plot_model
from itertools import chain
from functools import reduce

import keras.backend as K

from sklearn.preprocessing import MinMaxScaler

from copy import deepcopy

timesteps = 24
trteR = 0.9

deltaDay = 1 #Difference in days between day of data inputted and DAQI "forecasted"

root = ""

# load dataset
datasetPM25 = pandas.read_csv(root + 'DataSET-PM252017-2019.csv', header=0, index_col=0)
datasetPM10 = pandas.read_csv(root + 'DataSET-PM102017-2019.csv', header=0, index_col=0)
datasetOzone = pandas.read_csv(root + 'DataSET-Ozone2017-2019.csv', header=0, index_col=0)
datasetNO2 = pandas.read_csv(root + 'DataSET-NO22017-2019.csv', header=0, index_col=0)
datasetSO2 = pandas.read_csv(root + 'DataSET-SO22017-2019.csv', header=0, index_col=0)


def multitask_loss(y_true, y_pred):
	y_pred = K.clip(y_pred, K.epsilon(), 1 - K.epsilon())
	# Multi-task loss
	return K.mean(K.sum(- y_true * K.log(y_pred) - (1 - y_true) * K.log(1 - y_pred), axis=1))

""" #reduce dataset
datasetPM10 = datasetPM10.loc[:,datasetPM25.keys()]
datasetOzone = datasetPM10.loc[:,datasetPM25.keys()]
datasetNO2 = datasetPM10.loc[:,datasetPM25.keys()]
datasetSO2 = datasetPM10.loc[:,datasetPM25.keys()] """

sets = [datasetNO2, datasetOzone, datasetPM10, datasetPM25, datasetSO2]


##DATASET REDUCTION##
keys = set.intersection(*[set(l) for l in sets])

sets = [a.loc[:,keys] for a in sets]

groups = [0, 1, 2, 3, 4 , 5, 6]
groups = [i + 7 for i in groups]

"""
for dataset in sets:
	values = dataset.values
	# specify columns to plot
	i = 1
	# plot each column
	pyplot.figure()
	for group in groups:
		pyplot.subplot(len(groups), 1, i)
		pyplot.plot(values[:, group])
		pyplot.title(dataset.columns[group], y=0.5, loc='right')
		i += 1
	pyplot.show() """

datasetALL = pandas.concat([a.T for a in sets]).T

features = datasetALL.shape[1]
locs = features // 5

data = datasetALL.values

data = data.astype('float32')
# normalize features

d = [[]]*5*locs
for i in range(5):
	scaler = MinMaxScaler(feature_range=(0, 1))
	sec = data.T[i * locs:(i + 1) * locs,:]
	secCon = array(list(reduce(chain, sec)))
	secCon = secCon.reshape(-1, 1)
	scaler = scaler.fit(secCon)
	for j in range(locs):
		d[j + (i * locs)] = list(scaler.transform(array(sec[j]).reshape(-1,1)))

d = array(d)
e = d.reshape(5 * locs,data.shape[0]).T

i = 1
# plot each column
pyplot.figure()
for group in groups:
	pyplot.subplot(len(groups), 1, i)
	pyplot.plot(e[:, group])
	i += 1
pyplot.show()

data = array(e.reshape(round(e.shape[0]/timesteps), timesteps, features))

bigY = array([array([ [max(a[:,(i*locs) + j]) for j in range(locs)] for a in data]) for i in range(5)])


bigY = bigY[:,deltaDay:]

data = data[deltaDay:,:,:]
flag = round(data.shape[0] * trteR)

trainX = data[:flag,:,:]
testX = data[flag:,:,:]

trainY = list(bigY[:,:flag])
testY = list(bigY[:,flag:])

sN = data.shape[1] * data.shape[2]

sharedNet1 = LSTM(sN, input_shape = (data.shape[1], data.shape[2]), return_sequences=True)
sharedNet2 = LSTM(sN//2, input_shape = (data.shape[1], data.shape[2]))

""" sharedNet1 = Dense(sN, input_shape = (timesteps, data.shape[1], data.shape[2]))
sharedNet2 = Dense(sN//2) """


i = Input(shape=(timesteps,datasetALL.shape[1]))
def createModel(dropoutRate=0.5, numNeurons=60, optimizer='adam'):
    x = sharedNet1(i)
    x = sharedNet2(x)
    x = Dropout(dropoutRate)(x) #Used to split MTL into unique layers
    x = Dense(numNeurons)(x)
    x = Dense(numNeurons//2)(x)
    x = Dense(locs, activation='sigmoid')(x)
    return x

outputLayer1 = createModel()
outputLayer2 = createModel()
outputLayer3 = createModel()
outputLayer4 = createModel()
outputLayer5 = createModel()

model = Model(inputs=[i], outputs=[outputLayer1, outputLayer2, outputLayer3, outputLayer4, outputLayer5])
model.compile(loss=multitask_loss, optimizer='adam', metrics=['accuracy'])

#plot_model(model, to_file='model.png')

epochs = 150
batchSize = 32

history = model.fit(
	x = trainX,
	y = trainY,
	batch_size = batchSize,
	epochs = epochs,
	verbose = 2,
	shuffle = False,
	validation_data=(testX, testY)
)

pyplot.plot(history.history['val_dense_6_acc'], label='Ozone')
pyplot.plot(history.history['val_dense_3_acc'], label='NO2')
pyplot.plot(history.history['val_dense_9_acc'], label='PM10')
pyplot.plot(history.history['val_dense_12_acc'], label='PM25')
pyplot.plot(history.history['val_dense_15_acc'], label='SO2')
pyplot.legend()
pyplot.show()

