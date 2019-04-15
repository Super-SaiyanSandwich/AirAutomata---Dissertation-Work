import os
import numpy as np
import progressbar
import time
import datetime

"""
A set of functions that was included at the beginning of development, however is not need
after a little research as the purpose that the functions would fulfill has already been
implemented by DEFRA in the ATOM service.

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
} """

##  A dictionary of the DAQI bands for each pollutant
pollutants = {
    'NO2'   : [67,134,200,267,334,400,467,534,600],
    'Ozone' : [33,66,100,120,140,160,187,213,240],
    'PM10'  : [16,33,50,58,66,75,83,91,100],
    'PM25'  : [11,23,35,41,47,53,58,64,70],
    'SO2'   : [88,177,266,354,443,532,710,887,1064]
}


def getFilename(year): 
    """
        Function used to construct a file path when selecting the source of data

        Parameters
        ----------
        year: int
            The year currently selected for the data source
            
        Returns
        -------
        str
            File path for the year data text document
    """
    return  root + str(year) + "Data.txt"

def getDAQI(locationData, dateIndex):
    """
        Gets the DAQI value

        Parameters
        ----------
        httpCon : urllib3.PoolManager
            Used to access the URL and download the related file
        locationCode : str
            Location and year saught for data file
        mode : str
            Defines whether it is automatic or non-automatic data stream from DEFRA
        pollutantCodes : dict
            Urls and related names of saught pollutants
            
        Returns
        -------
    """
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
                    #date = datetime.datetime.strptime(date[0:11], "%Y-%B-%dT%H")

                    for i in range(9):
                        if dataIN < pollutants[pollutant][i]:
                            AQIs.append(i + 1)
                            break
                except:
                    continue
        if (AQIs):
            DAQIs[dateIndex] = {date : max(AQIs)}
    return DAQIs

def readYearFile(year, DAQI = False, dateConv = False):
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

        if dateConv:
            for p in tempData:
                if p != "Location":
                    for indxi, ite in enumerate(tempData[p]):
                        tempData[p][indxi][0] = datetime.datetime.strptime(ite[0], "%Y-%m-%dT%H:%M:%SZ")

        if DAQI:
            dLen = max([len(x) for x in list(tempData.values())])
            z[(x,y)] = getDAQIs(tempData, dLen)
            
        else:
            z[(x,y)] = tempData
            del z[(x,y)]["Location"]

        
        
    return z

root = "./Data/"

## Finds the correct root to retrieve the data from
try:
    os.listdir(".").index("Data")
except:
    root = "../Data/"

if __name__ == "__main__":
    root = "Data/"
    a = readYearFile(2002)