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

deltaDay = 3 #Difference in days between day of data inputted and DAQI "forecasted"

root = ""

DAQIBands = [
    [67,134,200,267,334,400,467,534,600], #NO2
    [33,66,100,120,140,160,187,213,240], #Ozone
    [16,33,50,58,66,75,83,91,100], #PM10
    [11,23,35,41,47,53,58,64,70], #PM25
    [88,177,266,354,443,532,710,887,1064] #SO2
]

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

def getDAQI(day, pollu):
	d = [a for a in DAQIBands[pollu] if day < a]
	return round(1.0 - (0.1 * len(d)),1)

def removeOutliers(data): ##Removes any extreme Outliers in the data, as some of the datasets
						  ##	are being suppressed by one or two extreme values
	l = len(data)
	datas = sorted(data)
	q0 = datas[0]
	q75 = datas[round(l * 0.75)]
	flag = 2 * (q75 + 3 * (q75 - q0))
	return array([(lambda x: x if x < flag else 0)(x) for x in data])

sets = [datasetNO2, datasetOzone, datasetPM10, datasetPM25, datasetSO2]


##DATASET REDUCTION##
keys = set.intersection(*[set(l) for l in sets])

sets = [a.loc[:,keys] for a in sets]

groups = [0, 1, 2, 3, 4 , 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
groups = [a + 15 for a in groups]

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

dataY = array(data.reshape(round(data.shape[0]/timesteps), timesteps, features))

#bigY = array([array([ [getDAQI(max(a[:,(i*locs) + j]),i) for j in range(locs)] for a in dataY]) for i in range(5)])
scaler = [[]] * 5

d = [[]]*5*locs
for i in range(5):
	scaler[i] = MinMaxScaler(feature_range=(0, 1))

	sec = data.T[i * locs:(i + 1) * locs,:]

	secCon = array(list(reduce(chain, sec)))
	secCon = removeOutliers(secCon)
	secCon = secCon.reshape(-1, 1)

	scaler[i] = scaler[i].fit(secCon)

	pLoc = sec.shape[1]

	sec = [secCon[j * pLoc:(j+1) * pLoc] for j in range(locs)]

	for j in range(locs):
		d[j + (i * locs)] = list(scaler[i].transform(array(sec[j]).reshape(-1,1)))

d = array(d)
e = d.reshape(5 * locs,data.shape[0]).T

i = 1
# plot each column
""" pyplot.figure()
for group in groups:
	pyplot.subplot(len(groups), 1, i)
	pyplot.plot(e[:, group])
	i += 1
pyplot.show() """

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
def createModel(dropoutRate=0.5, numNeurons=80, optimizer='adam'):
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
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

#plot_model(model, to_file='model.png')

epochs = 100
batchSize = 64

history = model.fit(
	x = trainX,
	y = trainY,
	batch_size = batchSize,
	epochs = epochs,
	verbose = 1,
	shuffle = False,
	validation_data=(testX, testY)
)



pyplot.figure()
pyplot.subplot(2,2,1)
pyplot.plot(history.history['val_dense_3_loss'], label='NO2')
pyplot.plot(history.history['val_dense_6_loss'], label='Ozone')
pyplot.plot(history.history['val_dense_9_loss'], label='PM10')
pyplot.plot(history.history['val_dense_12_loss'], label='PM25')
pyplot.plot(history.history['val_dense_15_loss'], label='SO2')
pyplot.title("Loss")
pyplot.ylabel("Test")
pyplot.legend()

pyplot.subplot(2,2,3)
pyplot.plot(history.history['dense_3_loss'], label='NO2')
pyplot.plot(history.history['dense_6_loss'], label='Ozone')
pyplot.plot(history.history['dense_9_loss'], label='PM10')
pyplot.plot(history.history['dense_12_loss'], label='PM25')
pyplot.plot(history.history['dense_15_loss'], label='SO2')
pyplot.ylabel("Train")
pyplot.legend()
pyplot.show()



pyplot.figure()
pyplot.subplot(2,2,2)
pyplot.plot(history.history['val_dense_3_acc'], label='NO2')
pyplot.plot(history.history['val_dense_6_acc'], label='Ozone')
pyplot.plot(history.history['val_dense_9_acc'], label='PM10')
pyplot.plot(history.history['val_dense_12_acc'], label='PM25')
pyplot.plot(history.history['val_dense_15_acc'], label='SO2')
pyplot.ylabel("Accuracy")
pyplot.legend()

pyplot.subplot(2,2,4)
pyplot.plot(history.history['dense_3_acc'], label='NO2')
pyplot.plot(history.history['dense_6_acc'], label='Ozone')
pyplot.plot(history.history['dense_9_acc'], label='PM10')
pyplot.plot(history.history['dense_12_acc'], label='PM25')
pyplot.plot(history.history['dense_15_acc'], label='SO2')
pyplot.legend()
pyplot.show()
