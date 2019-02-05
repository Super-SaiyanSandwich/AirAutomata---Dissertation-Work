
import os

import numpy as np

plotlyUsername  =  "SuperSaiyanSandwich"
plotlyAPI = "gOAmpsOinHlGJatVILJl"

filename = "Data/2019Data.txt"

date = 0


pollutants = {
    'NO2'   : [67,134,200,267,334,400,467,534,600],
    'Ozone' : [33,66,100,120,140,160,187,213,240],
    'PM10'  : [16,33,50,58,66,75,83,91,100],
    'PM25'  : [11,23,35,41,47,53,58,64,70],
    'SO2'   : [88,177,266,354,443,532,710,887,1064]}

data = open(filename,"r")
datar = data.read()
datad = eval(datar)

x = []
y = []
xr = []
yr = []

z = []

def getDAQI(locationData, dateIndex):
    AQIs = []
    for pollutant in pollutants:
        data = locationData.get(pollutant)        
        if(data):
            dataIN = round(float(data[dateIndex][4]))
            for i in range(9):
                if dataIN < pollutants[pollutant][i]:
                    AQIs.append(i + 1)
                    break
    return max(AQIs)



for i in datad:
    pointy = float(datad[i].get("Location")[0])    
    y.append(pointy)
    yr.append(round(pointy, 2))

    pointx = float(datad[i].get("Location")[1])
    x.append(pointx)
    xr.append(round(pointx, 2))

    z.append(getDAQI(datad[i], date))




xrs = list(set(xr))
yrs = list(set(yr))

xrs.sort()
yrs.sort()

zCont = np.full((len(yrs),len(xrs)), None)


for i in range(len(z)):
    xin = xrs.index(xr[i])
    yin = yrs.index(yr[i])
    zin = z[i]
    zCont[yin, xin] = zin