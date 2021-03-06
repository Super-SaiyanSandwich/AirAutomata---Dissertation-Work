print("::::IMPORTING LIBRARIES::::")
print("::Importing fileReadIn::")
import fileReadIn as readIn
import csv
import pandas as pd
import numpy as np
import datetime, dateutil
import gc

import progressbar

from tkinter import Tk, Frame, IntVar, StringVar, OptionMenu, Label, OptionMenu, Button, N, E, W, S


POLLUTANTS = [
    "PM10",
    "Ozone",
    "SO2",
    "PM25",
    "NO2"
    ]

OPTIONS = POLLUTANTS + ["ALL"]

def generateDates(yStart, yEnd):
    if yEnd != datetime.date.today().year:
        return [time.strftime("%Y-%m-%dT%H:%M:%SZ") for time in list(dateutil.rrule.rrule(dateutil.rrule.HOURLY,
            dtstart= datetime.datetime(yStart,1,1,0,0,0,0),
            until= datetime.datetime(yEnd,12,31,23,0,0,0)))]
    else:
        today = datetime.date.today() - datetime.timedelta(days = 1)
        return [time.strftime("%Y-%m-%dT%H:%M:%SZ") for time in list(dateutil.rrule.rrule(dateutil.rrule.HOURLY,
            dtstart= datetime.datetime(yStart,1,1,0,0,0,0),
            until= datetime.datetime(yEnd,today.month,today.day,23,0,0,0)))]



def getData(yStart, yEnd, polu):
    data = {}
    print("::::READING IN DATA FILES::::")


    yData = readIn.readYearFile(yStart)
    for location in yData:
        for polutant in yData[location]:
            if polutant == polu:
                data.update({location: yData[location][polu]})
    gc.collect()

    for i in range(yStart + 1,yEnd + 1):
        yData = readIn.readYearFile(i)
        for location in yData:
            gc.collect()
            try:
                data[location] += yData[location][polu]
            except:
                continue

    return data


def saveCSV(yearStart, yearEnd, polu):
    data = getData(yearStart, yearEnd, polu)

    print("::Files Loaded::\n")

    print("::Converting to DataFrame::")

    headers = list(data.keys())
    dates = generateDates(yearStart,yearEnd)
    pdata = list(data.values())

    pdates = np.zeros((len(headers), len(dates)), dtype= np.int16)

    for locI in progressbar.progressbar(range(len(headers))):
        for data in pdata[locI]:
            try:
                pdates[locI, dates.index(data[0])] = round(float(data[1]))
            except:
                try:
                    pdates[locI, dates.index(data[0].lstrip())] = round(float(data[1]))
                except:
                    continue

    """ alpha = [[date] + list(pdates[:,i]) for i, date in enumerate(dates)]
    pdData = np.array([[""] + headers] +  alpha ) """  #Spent an hour getting this down before realising I can include it all in
                                                       #dataframe decleration :(

    
    bIndexs = [i for i,a in enumerate(pdates) if len(set(a)) == 1]
    pdates = np.delete(pdates, bIndexs, 0).T
    headers = [a for i,a in enumerate(headers) if i not in bIndexs]

    dataFrame = pd.DataFrame(pdates, index = dates, columns = headers)



    print("::WRITING FILES::")
    dataFrame.to_csv("DataSET-"+polu+str(yearStart)+"-"+str(yearEnd)+".csv")
    print("::::FINISHED::::")



if __name__ == "__main__":
    print("::::OPENING::::")
    
    root = Tk()
    root.title("Select Dataset to Create.")
    
    # Add a grid
    mainframe = Frame(root)
    mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
    mainframe.columnconfigure(0, weight = 1)
    mainframe.rowconfigure(0, weight = 1)
    mainframe.pack(pady = 50, padx = 50)
    
    # Create a Tkinter variables
    tkYStart = IntVar(root)
    tkYEnd = IntVar(root)
    tkPolu = StringVar(root)


    years = list(range(2001,2020))
    tkYStart.set(2001)
    tkYEnd.set(2002)
    tkPolu.set("PM10")
    
    popupYStart = OptionMenu(mainframe, tkYStart, *years)
    Label(mainframe, text="Select Starting Year:").grid(row = 1, column = 1)
    popupYStart.grid(row = 1, column =3)

    popupYEnd = OptionMenu(mainframe, tkYEnd, *years)
    Label(mainframe, text="Select Ending Year:").grid(row = 2, column = 1)
    popupYEnd.grid(row = 2, column =3)

    popupPolu = OptionMenu(mainframe, tkPolu, *OPTIONS)
    Label(mainframe, text="Select Polutant:").grid(row = 3, column = 1)
    popupPolu.grid(row = 3, column =3)
    
    def changeYStart(*args):
        if tkYStart.get() > tkYEnd.get():
            tkYEnd.set(tkYStart.get())

    def changeYEnd(*args):
        if tkYStart.get() > tkYEnd.get():
            tkYStart.set(tkYEnd.get())
        
    tkYStart.trace('w', changeYStart)
    tkYEnd.trace('w', changeYEnd)

    def run():
        if tkPolu.get() == "ALL":
            for polu in POLLUTANTS:
                saveCSV(tkYStart.get(), tkYEnd.get(), polu)
        else:
            saveCSV(tkYStart.get(), tkYEnd.get(), tkPolu.get())

    btn = Button(root, text="RUN", command = run)
    btn.pack()
    root.mainloop()