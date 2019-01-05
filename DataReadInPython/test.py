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

defraATOMUrl = "https://uk-air.defra.gov.uk/data/atom-dls/auto/2018/atom.en.xml"

## INFORMATION ON ABERDEEN DATA, USED FOR TESTING
defraATOMUrlABD = "http://uk-air.defra.gov.uk/data/atom-dls/auto/2018/GB_FixedObservations_2018_ABD.atom.en.xml"
defraATOMUrlABD2 = "http://uk-air.defra.gov.uk/data/atom-dls/observations/auto/GB_FixedObservations_2018_ABD.xml"

pollutantCodes = {
    "NO2"   : "8",
    "PM10"  : "5",
    "PM25"  : "6001",
    "Ozone" : "7", 
    "SO2"   : "1"
}

spatailDatasetCode = "{http://inspire.ec.europa.eu/schemas/inspire_dls/1.0}spatial_dataset_identifier_code"
entry =  "{http://www.w3.org/2005/Atom}entry"

#
#
#     MAIN FUNCTIONS
#
#


def getLocations(URL, httpCon, polltantCodes):
    req = httpCon.request("GET",URL)

    reqList = str(req.data).split('\\n')
    reqList[0] = reqList[0][2:]
    reqList[-1] = reqList[-1][:-1]

    parser = EleTree.XMLParser(encoding="utf-8")
    XMLdata = EleTree.fromstringlist(reqList, parser=parser)

    for location in XMLdata.iter("{http://www.w3.org/2005/Atom}entry"):
        for sub in location:
            print(sub.tag)
        print("")

#
#
#     TESTING FUNCTIONS
#
#

print("::TEST::\n")

httpCon = urllib3.PoolManager(cert_reqs="CERT_REQUIRED",ca_certs=certifi.where())
req = httpCon.request("GET",defraATOMUrlABD2)


reqList = str(req.data).split('\\n')
reqList[0] = reqList[0][2:]
reqList[-1] = reqList[-1][:-1]

parser = EleTree.XMLParser(encoding="utf-8")
ABDXMLdata = EleTree.fromstringlist(reqList, parser=parser)

##with open(fileName,'w') as ABDfile:
##    ABDfile.write(ABDXMLdata)


""" 
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
 """

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
    values[indx] = data
    

getLocations(defraATOMUrl, httpCon, pollutantCodes)

print("::TESTS END::")

