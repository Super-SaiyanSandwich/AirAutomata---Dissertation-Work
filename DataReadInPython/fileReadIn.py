import os
import numpy as np
import progressbar
import time

def hourly(data):
    return data


def eightHourly(data):
    return data


averageMethod = {
    'NO2'   : "Hourly",
    'Ozone' : "8 Hourly",
    'PM10'  : "24 Hour",
    'PM25'  : "24 Hour",
    'SO2'   : "Hourly"
}

pollutants = {
    'NO2'   : [67,134,200,267,334,400,467,534,600],
    'Ozone' : [33,66,100,120,140,160,187,213,240],
    'PM10'  : [16,33,50,58,66,75,83,91,100],
    'PM25'  : [11,23,35,41,47,53,58,64,70],
    'SO2'   : [88,177,266,354,443,532,710,887,1064]
}


def getFilename(year): 
    return  "Data/" + str(year) + "Data.txt"

def getDAQI(locationData, dateIndex):
    AQIs = []
    for pollutant in pollutants:
        data = locationData.get(pollutant)        
        if(data):
            dataIN = round(float(data[dateIndex][1]))
            for i in range(9):
                if dataIN < pollutants[pollutant][i]:
                    AQIs.append(i + 1)
                    break
    return max(AQIs)

def getDAQIs(locationData, dateRange):
    DAQIs = np.empty(dateRange, dtype=  dict)
    for dateIndex in range(dateRange):
        AQIs = []
        date = None
        for pollutant in pollutants:
            data = locationData.get(pollutant)      
            if(data):
                try:
                    dataIN = round(float(data[dateIndex][1]))
                    date = data[dateIndex][0]
                    for i in range(9):
                        if dataIN < pollutants[pollutant][i]:
                            AQIs.append(i + 1)
                            break
                except:
                    continue
        if (AQIs):
            DAQIs[dateIndex] = {date : max(AQIs)}
    return DAQIs

def readYearFile(year, DAQI = False):
    print("::Fetching",year,"Data File::")
    filename = getFilename(year)

    
    data = open(filename, 'r')
    datar = data.read()
    datad = eval("lambda: " + datar)()
    print("::Fetched",year,"Data File::")
    print("::Evaluating",year,"Data File::")
    
    #x = []
    #y = []

    z = {}

    for i in progressbar.progressbar(datad):
        tempData = datad[i]

        y = float(tempData.get("Location")[0])    
        #y.append(pointy)

        x = float(tempData.get("Location")[1])
        #x.append(pointx)

        if DAQI:
            dLen = max([len(x) for x in list(tempData.values())])
            z[(x,y)] = getDAQIs(tempData, dLen)
        else:
            z[(x,y)] = tempData
            del z[(x,y)]["Location"]

        
        
    return z



if __name__ == "__main__":
    a = readYearFile(2002)