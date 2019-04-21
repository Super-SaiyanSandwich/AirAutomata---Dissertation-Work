
import plotly
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.io as pio

from mpl_toolkits.basemap import Basemap

import os

import numpy as np

from itertools import chain
from functools import reduce

import pandas

plotlyUsername  =  "SuperSaiyanSandwich"
plotlyAPI = "gOAmpsOinHlGJatVILJl"

filename = "Data/2019Data.txt"

date = 10


pollutants = {
    'NO2'   : [67,134,200,267,334,400,467,534,600],
    'Ozone' : [33,66,100,120,140,160,187,213,240],
    'PM10'  : [16,33,50,58,66,75,83,91,100],
    'PM25'  : [11,23,35,41,47,53,58,64,70],
    'SO2'   : [88,177,266,354,443,532,710,887,1064]
}

polluVal = [
    [67,134,200,267,334,400,467,534,600],
    [33,66,100,120,140,160,187,213,240],
    [16,33,50,58,66,75,83,91,100],
    [11,23,35,41,47,53,58,64,70],
    [88,177,266,354,443,532,710,887,1064]
]

## Before move to CSVs
""" data = open(filename,"r")
datar = data.read()
datad = eval(datar) """

root = ""

datasetPM25 = pandas.read_csv(root + 'DataSET-PM252017-2019.csv', header=0, index_col=0)
datasetPM10 = pandas.read_csv(root + 'DataSET-PM102017-2019.csv', header=0, index_col=0)
datasetOzone = pandas.read_csv(root + 'DataSET-Ozone2017-2019.csv', header=0, index_col=0)
datasetNO2 = pandas.read_csv(root + 'DataSET-NO22017-2019.csv', header=0, index_col=0)
datasetSO2 = pandas.read_csv(root + 'DataSET-SO22017-2019.csv', header=0, index_col=0)

sets = [datasetNO2, datasetOzone, datasetPM10, datasetPM25, datasetSO2]


##DATASET REDUCTION##
keys = set.union(*[set(l) for l in sets])

#sets = [a.loc[:,keys] for a in sets]

#keys = [list(map(eval,a)) for a in sets]

x = []
y = []
xr = []
yr = []

z = []

def roundTo(x, to):    
    return round(x / to) * to


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

def getAQI(data, polluIndex):
    pset = [a for a in polluVal[polluIndex] if a < data]
    return 1 + len(pset)


""" for i in range(5):
    for ind, loc in enumerate(keys[i]):
        pointy = float(loc[1])    
        y.append(pointy)
        yr.append(roundTo(pointy, 0.25))

        pointx = float(loc[0])
        x.append(pointx)
        xr.append(roundTo(pointx, 0.25))

        z.append(getAQI(sets[i][str(loc)][date], i )) """

for loc in keys:
    elem = [0] * 5
    for i in range(5):
        try:
            elem[i] = getAQI(sets[i][loc][date], i)
        except:
            continue
    
    pointy = float(eval(loc)[1])
    y.append(pointy)
    yr.append(roundTo(pointy, 0.25))

    pointx = float(eval(loc)[0])
    x.append(pointx)
    xr.append(roundTo(pointx, 0.25))

    z.append(max(elem))
    



xNum = round(14 / 0.25) + 1
yNum = round(14.5 / 0.25) + 1

xrA = ["%.1f" % i for i in np.linspace(-12,4, xNum)]
yrA = ["%.1f" % i for i in np.linspace(48,62.5, yNum)]

edgeW = [-12] * xNum
edgeE = [4] * xNum
edgeN = [62.5] * yNum
edgeS = [48] * yNum

smootherX = edgeW + edgeE + xrA + xrA
smootherY = yrA + yrA + edgeN + edgeS
smootherZ = [1] * (2 * (xNum + yNum))

""" xrs = list(set(xr))
yrs = list(set(yr))

xrs.sort()
yrs.sort()

zCont = np.full((105,120), None)

zCont[:,0] = 2
zCont[:,119] = 2


for i in range(len(z)):
    xin = xrs.index(xr[i])
    yin = yrs.index(yr[i])
    zin = z[i]
    zCont[yin, xin] = zin """

trace0 = go.Contour(
    x=(xr + smootherX),  y=(yr + smootherY), z=(z + smootherZ), connectgaps=True,
    line=dict(width = 0, smoothing=1.0),
    autocontour=False,
    contours=dict( start = 1, end = 10, size = 1),
    colorscale=[
        [0.0,"rgb(156,255,156)"],
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

trace2 = go.Contour(
    x=(xr + smootherX),  y=(yr + smootherY), z=(z + smootherZ), connectgaps=True,
    line=dict(width = 0, smoothing=1.0),
    autocontour=False,
    contours=dict( start = 1, end = 10, size = 1),
    colorscale=[
        [0.0,"rgb(255,255,255)"],
        [1.0,"rgb(255,255,255)"]
    ]
)

c=[ "rgb(156,255,156)",
    "rgb(156,255,156)",
    "rgb(49,255,0)",
    "rgb(49,207,0)",
    "rgb(255,255,0)",
    "rgb(255,207,0)",
    "rgb(255,154,0)",
    "rgb(255,146,146)",
    "rgb(255,0,0)",
    "rgb(153,0,0)",
    "rgb(209,48,255)" ]

cz = [c[i] for i in z]

trace1 = go.Scatter(x=x,y=y,mode="markers",marker=dict(
        color=cz,
        opacity=1.0,
        size=9,
        line = dict(
            width = 2,
        )))

""" trace2 = go.Contour(
    z=z,
    x=x,
    y=y,
    colorscale="RdBu",
    zauto=False,  # custom contour levels
    zmin=0,      # first contour level
    zmax=10        # last contour level  => colorscale is centered about 0
) """

m = Basemap(llcrnrlon=-11.1,llcrnrlat=48.7,urcrnrlon=4.0,urcrnrlat=60.7,
             resolution='f', projection='merc')#, lat_0 = 39.5, lon_0 = -3.25)

#m.fillcontinents(color='none', lake_color='aqua')

# Make trace-generating function (return a Scatter object)
def make_scatter(x,y):
    return go.Scatter(
        x=x,
        y=y,
        mode='lines',
        line=go.scatter.Line(color="black"),
        name=' '#,  # no name on hover
        #fill='toself',
        #fillcolor="white"
    )

# Functions converting coastline/country polygons to lon/lat traces
def polygons_to_traces(poly_paths, N_poly):
    ''' 
    pos arg 1. (poly_paths): paths to polygons
    pos arg 2. (N_poly): number of polygon to convert
    '''
    traces = []  # init. plotting list 

    for i_poly in range(N_poly):
        poly_path = poly_paths[i_poly]
        
        # get the Basemap coordinates of each segment
        coords_cc = np.array(
            [(vertex[0],vertex[1]) 
             for (vertex,code) in poly_path.iter_segments(simplify=False)]
        )
        
        # convert coordinates to lon/lat by 'inverting' the Basemap projection
        lon_cc, lat_cc = m(coords_cc[:,0],coords_cc[:,1], inverse=True)
        
        # add plot.ly plotting options
        traces.append(make_scatter(lon_cc,lat_cc))
     
    return traces

# Function generating coastline lon/lat traces
def get_coastline_traces():
    poly_paths = m.drawcoastlines().get_paths() # coastline polygon paths
    N_poly = 34 # use only the 91st biggest coastlines (i.e. no rivers)
    return polygons_to_traces(poly_paths, N_poly)

# Function generating country lon/lat traces
def get_country_traces():
    poly_paths = m.drawcountries().get_paths() # country polygon paths
    N_poly = len(poly_paths)  # use all countries
    return polygons_to_traces(poly_paths, N_poly)

traces_cc = get_coastline_traces()#+get_country_traces()

layout = go.Layout(
    autosize=False,
    width=1000,
    height=996,
    margin=go.layout.Margin(
        l=30,
        r=30,
        b=30,
        t=30,
        pad=4
    ),
    xaxis=go.layout.XAxis(
        range = [-10,2]
    ),
    yaxis=go.layout.YAxis(
        range = [50,60.5]
    ),
    showlegend=False,
    hovermode="closest"
    #,
    #images= [dict(
    #              source= "back.png",
    #              xref= "x",Figure
    #              yref= "y",
    #              x= 0,
    #              y= 0,
    #              sizex= 12,
    #              sizey= 10.5,
    #              sizing= "stretch",
    #              opacity= 0.0,
    #              layer= "above")] 
)



data = traces_cc + [trace1, trace0]

 
#fig = go.Figure(data=[trace0, trace1],layout=layout)

fig = go.Figure(data=data, layout=layout)


plotly.offline.plot(fig, show_link=False,auto_open=True)

print("Test Complete")