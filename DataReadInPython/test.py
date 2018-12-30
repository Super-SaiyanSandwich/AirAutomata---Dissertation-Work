import feedparser 

defraATOMUrlABD = "http://uk-air.defra.gov.uk/data/atom-dls/auto/2018/GB_FixedObservations_2018_ABD.atom.en.xml"
defraATOMUrlABD2 = "http://uk-air.defra.gov.uk/data/atom-dls/observations/auto/GB_FixedObservations_2018_ABD.xml"



print("::TEST::\n")

feed, data = feedparser.parse( defraATOMUrlABD2 )


print("::FEED READ::")