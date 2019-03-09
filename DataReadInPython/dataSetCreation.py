print("::::IMPORTING LIBRARIES::::")
print("::Importing fileReadIn::")
import fileReadIn as readIn
import csv
import pandas as pd
import numpy as np
import datetime, dateutil
import gc

import progressbar

from tkinter import *


POLLUTANTS = [
    "PM10",
    "Ozone",
    "SO2",
    "PM25",
    "NO2"
    ]

def generateDates(yStart, yEnd):
    return [time.strftime("%Y-%m-%dT%H:%M:%SZ") for time in list(dateutil.rrule.rrule(dateutil.rrule.HOURLY,
        dtstart= datetime.datetime(yStart,1,1,0,0,0,0),
        until= datetime.datetime(yEnd,12,31,23,0,0,0)))]


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
            pdates[locI, dates.index(data[0])] = round(float(data[1]))

    """ alpha = [[date] + list(pdates[:,i]) for i, date in enumerate(dates)]
    pdData = np.array([[""] + headers] +  alpha ) """  #Spent an hour getting this down before realising I can include it all in
                                                       #dataframe decleration :(

    dataFrame = pd.DataFrame(pdates.T, index = dates, columns = headers)

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

    popupPolu = OptionMenu(mainframe, tkPolu, *POLLUTANTS)
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
        saveCSV(tkYStart.get(), tkYEnd.get(), tkPolu.get())

    btn = Button(root, text="RUN", command = run)
    btn.pack()
    root.mainloop()