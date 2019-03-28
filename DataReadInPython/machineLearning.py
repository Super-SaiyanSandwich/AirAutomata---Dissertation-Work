import pandas
from matplotlib import pyplot
from copy import deepcopy

# load dataset
datasetPM25 = pandas.read_csv('DataSET-PM252018-2019.csv', header=0, index_col=0)
datasetPM10 = pandas.read_csv('DataSET-PM102018-2019.csv', header=0, index_col=0)
datasetOzone = pandas.read_csv('DataSET-Ozone2018-2019.csv', header=0, index_col=0)
datasetNO2 = pandas.read_csv('DataSET-NO22018-2019.csv', header=0, index_col=0)
datasetSO2 = pandas.read_csv('DataSET-SO22018-2019.csv', header=0, index_col=0)

""" #reduce dataset
datasetPM10 = datasetPM10.loc[:,datasetPM25.keys()]
datasetOzone = datasetPM10.loc[:,datasetPM25.keys()]
datasetNO2 = datasetPM10.loc[:,datasetPM25.keys()]
datasetSO2 = datasetPM10.loc[:,datasetPM25.keys()] """


sets = [datasetNO2, datasetOzone, datasetPM10, datasetPM25, datasetSO2]

keys = set.intersection(*[set(l) for l in sets])

sets = [a.loc[:,keys] for a in sets]

groups = [0, 1, 2, 3, 4 , 5, 6]
groups = [i + 7 for i in groups]


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
	pyplot.show()