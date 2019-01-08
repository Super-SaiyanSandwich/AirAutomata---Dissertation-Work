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

pollutantCodes = {
    "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/8":    "NO2",
    "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/5":    "PM10",
    "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/6001": "PM25",
    "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/7":    "Ozone",
    "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/1":    "SO2"
}

missingFOI = "http://environment.data.gov.uk/air-quality/so/GB_SamplingFeature_missingFOI"

##
##  ATOM feed codes
##

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
        
            

def getDataUrl(year):
    return "https://uk-air.defra.gov.uk/data/atom-dls/auto/"+ str(year) +"/atom.en.xml"

def getLocationDataURL(locationID):
    return "https://uk-air.defra.gov.uk/data/atom-dls/observations/auto/" + locationID + ".xml"

#
#
#     TESTING FUNCTIONS
#
#

print("::TEST::\n")

httpCon = urllib3.PoolManager(cert_reqs="CERT_REQUIRED",ca_certs=certifi.where())


"""
req = httpCon.request("GET",defraATOMUrlABD2)
reqList = str(req.data).split('\\n')
reqList[0] = reqList[0][2:]
reqList[-1] = reqList[-1][:-1]

parser = EleTree.XMLParser(encoding="utf-8")
ABDXMLdata = EleTree.fromstringlist(reqList, parser=parser)

##with open(fileName,'w') as ABDfile:
##    ABDfile.write(ABDXMLdata)



for child in ABDXMLdata:
    print(child.tag, child.text)
    for subChild in child:
        print("\t",subChild.tag, subChild.text)
        for subsubChild in subChild:
            print("\t\t",subsubChild.tag, subsubChild.attrib)
            if (subsubChild.tag == "{http://www.opengis.net/om/2.0}result"):
                for sssChild in subsubChild:
                    print("\t\t\t",sssChild.tag,sssChild.text)

print("\n\n::TEST 2::\n")


featureOI = []
t = []

for ite in ABDXMLdata.iter('{http://www.opengis.net/om/2.0}featureOfInterest'):
    feature = list(ite.attrib.values())[0]
    featureOI.append(feature)
    if (feature == 'http://environment.data.gov.uk/air-quality/so/GB_SamplingFeature_missingFOI'):
        t.append(False)
        continue
    
    
t = numpy.array(featureOI)!='http://environment.data.gov.uk/air-quality/so/GB_SamplingFeature_missingFOI'

c = 0
values = []

for indx, ite in enumerate(ABDXMLdata.iter('{http://www.opengis.net/swe/2.0}values')):
    if t[indx]:
        values.append(ite.text)


for indx, data in enumerate(values):
    data = data[20:].split("@@")
    for indxi, ite in enumerate(data):
        data[indxi] = ite.split(",")
    values[indx] = data """
    

data = getLocations(getDataUrl(2019), httpCon, pollutantCodes)

print("::TESTS END::")

