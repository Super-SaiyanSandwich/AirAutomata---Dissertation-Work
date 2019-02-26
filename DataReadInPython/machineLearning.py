print("::::IMPORTING LIBRARIES::::")
print("::Importing Keras::")
import keras
from keras.models import Model
print("::Importing sys::")
import sys
sys.path.insert(0, '/DataReadInPython')
print("::Importing fileReadIn::")
import fileReadIn as readIn

data = {}
print("::::READING IN DATA FILES::::")
for i in range(2009,2020):
    data.update(readIn.readYearFile(i, DAQI= True))

#model = Sequential()

#from keras.layers import Input, Dense

#model.add(Dense(units = 64, activation='relu', input_dim=))

print("\n::Files Loaded::")

