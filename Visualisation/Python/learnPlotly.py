username  =  "SuperSaiyanSandwich"
plotlyAPI = "gOAmpsOinHlGJatVILJl"

filename = "Data/2019Data.txt"

date = 0

import plotly
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.io as pio

import os

import numpy as np

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

trace0 = go.Contour(
    x=xrs,  y=yrs, z=zCont, connectgaps=True, line=dict(width = 0),
    autocontour=False, contours=dict( start = 1, end = 10, size = 1),
    colorscale=[
        [0,"rgb(255,255,255)"],
        [0.1,"rgb(156,255,156)"],
        [0.2,"rgb(49,255,0)"],
        [0.3,"rgb(49,207,0)"],
        [0.4,"rgb(255,255,0)"],
        [0.5,"rgb(255,207,0)"],
        [0.6,"rgb(255,154,0)"],
        [0.7,"rgb(255,146,146)"],
        [0.8,"rgb(255,0,0)"],
        [0.9,"rgb(153,0,0)"],
        [1.0,"rgb(209,48,255)"]
    ]
)

trace1 = go.Scatter(x=x,y=y,mode="markers",marker=dict(color='rgb(0,0,240)',opacity=0.4,size=5))

layout = go.Layout(
    autosize=False,
    width=1037,
    height=996,
    margin=go.layout.Margin(
        l=30,
        r=30,
        b=30,
        t=30,
        pad=4
    )
)
 
fig = go.Figure(data=[trace0, trace1],layout=layout)

plotly.offline.plot(fig, show_link=False,auto_open=True)

print("Test Complete")