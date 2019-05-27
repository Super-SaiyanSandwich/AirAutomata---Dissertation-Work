0#
#
#     IMPORTS
#
#
import xml.etree.ElementTree as EleTree

import numpy 

import progressbar

import certifi
import urllib3

#
#
#     IMPORTANT VARIABLES
#
#

## INFORMATION ON ABERDEEN DATA, USED FOR TESTING
defraATOMUrlABD = "http://uk-air.defra.gov.uk/data/atom-dls/auto/2018/GB_FixedObservations_2018_ABD.atom.en.xml"
defraATOMUrlABD2 = "http://uk-air.defra.gov.uk/data/atom-dls/observations/auto/GB_FixedObservations_2018_ABD.xml"

## LIST OF NEEDED POLLUTANT URLS AND THE RELATED NAME
pollutantCodes = {
    "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/8":    "NO2",
    "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/5":    "PM10",
    "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/6001": "PM25",
    "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/7":    "Ozone",
    "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/1":    "SO2"
}

## WITHIN THE DATASETS, IF A DATA SAMPLE HAS THIS CODE FOR ONE OF IT'S ATTRIBUTES THEN IT IS USELESS
missingFOI = "http://environment.data.gov.uk/air-quality/so/GB_SamplingFeature_missingFOI"

## DIFFERENT TYPES OF DATA
auto = "auto"
nonAuto = "non-auto"
aggregated = "aggregated" ## NOT USED

##
##  ATOM feed codes
##
"""  
    The following are the string codes used to identify elements with the DEFRA ATOM feed. 
"""

spatialDatasetCode = "{http://inspire.ec.europa.eu/schemas/inspire_dls/1.0}spatial_dataset_identifier_code"
entry =  "{http://www.w3.org/2005/Atom}entry"
link =  "{http://www.w3.org/2005/Atom}link"
href =  "{http://www.w3.org/1999/xlink}href"
featureMember = "{http://www.opengis.net/gml/3.2}featureMember"
observation = "{http://www.opengis.net/om/2.0}OM_Observation"
featureOfInterest = "{http://www.opengis.net/om/2.0}featureOfInterest"
resultValues = "{http://www.opengis.net/swe/2.0}values"

#
#
#     MAIN FUNCTIONS
#
#

def getData(year):
    """
        Gets all of the data, for a specific year across all locations that existed in that year.
        Filters out unneccesary information

        Parameters
        ----------
        year : int
            The year of data being downloaded

        Returns
        -------
        data
            dictionary of all the data
    """

    data = {}
    HttpCon = getHttpCon()
    
    data.update(getLocations(getDataUrl(year, auto), auto, HttpCon, pollutantCodes))
    data.update(getLocations(getDataUrl(year, nonAuto), nonAuto,  HttpCon, pollutantCodes))
    
    return data


def getLocations(URL, mode, httpCon, pollutantCodes):
    """
        Finds all of the different location codes for sensors reading in information.
        Once found, all of the data for that location is download and filtered for only
        the pollutants needed in this project.

        Parameters
        ----------
        URL : string
            Either the automatic or non-automatic string URL for a year
        mode : string
            Either automatic or non-automatic
        httpCon : urllib3.PoolManager
            Used to access the URL and download the related file
        pollutantCodes : dict
            Urls and related names of saught pollutants
        
        Returns
        -------
        data
            dictionary of all the data
    """

    data = {}

    req = httpCon.request("GET",URL)

    reqList = str(req.data).split('\\n')
    reqList[0] = reqList[0][2:]
    reqList[-1] = reqList[-1][:-1]

    parser = EleTree.XMLParser(encoding="utf-8")
    XMLdata = EleTree.fromstringlist(reqList, parser=parser)
    print("LOADING ALL " + mode.upper() + "MATIC DATA STREAMS")
    for location in progressbar.progressbar(XMLdata.iter(entry)):
        for polltant in location.iter(link):
            ##print(polltant.attrib["href"])
            if polltant.attrib["href"] in pollutantCodes:
                locationCode = list(location)[0].text
                if "Agg" in locationCode: break
                #print("LOADING " + mode.upper() + "MATIC DATA STREAM::" ,locationCode)
                locationData = getLocationData(httpCon, locationCode, mode, pollutantCodes)
                if locationData != {}:
                    data[locationCode] = locationData
                    data[locationCode].update({"Location" : location[-1].text.split(" ")[0:2]})
                break
    
    httpCon.clear()

    return data


def getLocationData(httpCon, locationCode, mode, pollutantCodes):
    """
        Downloads all of the data for a certain location.

        By using the standardised Url naming system for the different locations, this function
        downloads and parses the .XML file related to the year and location being saught.
        The year is part of the location code in the form of "GB_FixedObservations_[year]_[location]"

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
        dict
            Dictionary of values for each pollutant
    """
    
    locationData = {}

    req = httpCon.request("GET", getLocationDataURL(locationCode, mode))

    reqList = str(req.data).split('\\n')
    reqList[0] = reqList[0][2:]
    reqList[-1] = reqList[-1][:-1]

    parser = EleTree.XMLParser(encoding="utf-8")
    XMLdata = EleTree.fromstringlist(reqList, parser=parser)

    for obs in XMLdata.iter(observation):
        try:
            pollutant = obs[6].attrib[href]
            
            if (pollutant in pollutantCodes) and (obs[7].attrib[href] != missingFOI):
                
                a = list(obs.iter(resultValues))[0]
                data = a.text
                data = data[20:].split("@@")
                
                if data != ['']:
                    badData = []
                    for indxi, ite in enumerate(data):
                        t = ite.split(",")                        
                        try:
                            if t[4] != "-99":
                                data[indxi] = list(numpy.array(t)[[0,4]])
                            else: 
                                badData.append(indxi)     
                        except:
                            badData.append(indxi)
                            continue
                    c = 0
                    for indxi in badData:
                        del data[indxi - c]
                        c += 1
                
                    locationData.update({pollutantCodes[pollutant] : data})
                    
        except KeyError:
            continue

    httpCon.clear()

    return locationData
        
            
## Generates the main Url for the year and mode of data being downloaded
def getDataUrl(year, mode):
    return "https://uk-air.defra.gov.uk/data/atom-dls/" + mode + "/" + str(year) +"/atom.en.xml"

## Generates the location Url for the year and mode of data being downloaded
def getLocationDataURL(locationID, mode):
    return "https://uk-air.defra.gov.uk/data/atom-dls/observations/" + mode + "/" + locationID + ".xml"

## Creates a Http connection object
def getHttpCon():
    return urllib3.PoolManager(cert_reqs="CERT_REQUIRED",ca_certs=certifi.where())

#
#
#     TESTING FUNCTIONS
#
#

if __name__ == '__main__':
    print("::TEST::\n")

    for i in range(2017,2020):
        data = getData(i)         
        f= open("Data/"+str(i)+"Data.txt","w+")
        f.write(str(data))
        f.close()
    print("::TESTS END::")

