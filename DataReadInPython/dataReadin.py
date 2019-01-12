#
#
#     IMPORTS
#
#
import xml.etree.ElementTree as EleTree

import numpy 

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

##
##  ATOM feed codes
##
"""  The following are the string codes used to identify elements with the DEFRA ATOM feed. 
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


def getLocations(URL, httpCon, pollutantCodes):
    data = {}

    req = httpCon.request("GET",URL)

    reqList = str(req.data).split('\\n')
    reqList[0] = reqList[0][2:]
    reqList[-1] = reqList[-1][:-1]

    parser = EleTree.XMLParser(encoding="utf-8")
    XMLdata = EleTree.fromstringlist(reqList, parser=parser)

    for location in XMLdata.iter(entry):
        for polltant in location.iter(link):
            ##print(polltant.attrib["href"])
            if polltant.attrib["href"] in pollutantCodes:
                locationCode = list(location)[0].text
                print("LOADING: ",locationCode)
                data[locationCode] = getLocationData(httpCon, locationCode, pollutantCodes)
                break
    
    return data


def getLocationData(httpCon, locationCode, pollutantCodes):
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
    pollutantCodes : dict
        Urls and related names of saught pollutants
        
    Returns
    -------
    dict
        Dictionary of values for each pollutant

    """
    
    locationData = {}

    req = httpCon.request("GET", getLocationDataURL(locationCode))

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
                
                for indxi, ite in enumerate(data):
                    data[indxi] = ite.split(",")   
                
                try:
                    locationData[pollutantCodes[pollutant]].append(data)   
                except:
                    locationData[pollutantCodes[pollutant]] = data
                    
        except KeyError:
            continue

    return locationData
        
            
## Generates the main Url for the year of data being downloaded
def getDataUrl(year):
    return "https://uk-air.defra.gov.uk/data/atom-dls/auto/"+ str(year) +"/atom.en.xml"

## Generates the location Url for the year of data being downloaded
def getLocationDataURL(locationID):
    return "https://uk-air.defra.gov.uk/data/atom-dls/observations/auto/" + locationID + ".xml"

## Creates a Http connection object
def getHttpCon():
    return httpCon = urllib3.PoolManager(cert_reqs="CERT_REQUIRED",ca_certs=certifi.where())

#
#
#     TESTING FUNCTIONS
#
#

if __name__ == '__main__':
    print("::TEST::\n")    
    data = getLocations(getDataUrl(2019), getHttpCon(), pollutantCodes)
    print("::TESTS END::")

