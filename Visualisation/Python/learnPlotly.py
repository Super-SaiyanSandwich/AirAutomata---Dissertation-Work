username  =  "SuperSaiyanSandwich"
plotlyAPI = "gOAmpsOinHlGJatVILJl"

filename = "Data/2019Data.txt"

date = 0

import plotly
import plotly.graph_objs as go
import plotly.tools as tls

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

trace0 = go.Scatter(
    x=xr,  y=yr, mode="markers"
)

trace1 = go.Contour(
    x=xrs,  y=yrs, z=zCont, connectgaps=True, line=dict(width = 0),
    autocontour=False, contours=dict( start = 1, end = 10, size = 1),
    colorscale=[
        [0,"rgb(0,0,255)"],
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



fig = tls.make_subplots(rows=1, cols=2, subplot_titles=('Scaler',
                                                        'Data'))

fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 2)
 


plotly.offline.plot(fig, show_link=False,auto_open=True)

print("Test Complete")