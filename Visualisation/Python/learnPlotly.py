username  =  "SuperSaiyanSandwich"
plotlyAPI = "gOAmpsOinHlGJatVILJl"

filename = "Data/2019Data.txt"

import plotly
import plotly.graph_objs as go
import plotly.tools as tls

data = open(filename,"r")
datar = data.read()
datad = eval(datar)

x = []
y = []
xr = []
yr = []

text = []

for i in datad:
    ##text.append(i)
    pointy = float(datad[i].get("Location")[0])
    y.append(pointy)
    yr.append(round(pointy,2))

    pointx = float(datad[i].get("Location")[1])
    x.append(pointx)
    xr.append(round(pointx,2))


trace0 = go.Scatter(
    x=x,  y=y, mode="markers"
)

trace1 = go.Scatter(
    x=xr,  y=yr, mode="markers"
)

fig = tls.make_subplots(rows=1, cols=2, subplot_titles=('rounded = False',
                                                        'rounded = True'))

fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 2)



plotly.offline.plot(fig, show_link=False,auto_open=True)