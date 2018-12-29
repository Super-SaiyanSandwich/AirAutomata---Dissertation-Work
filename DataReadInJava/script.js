var fun1 = function(name) {
    print('Hi there from Javascript, ' + name);
    print(a)
    return "greetings from javascript";
};

var fun2 = function (object) {
    print("JS Class Definition: " + Object.prototype.toString.call(object));
};


var ATOMread = function (feedUrl) {
    print("::ENTER ATOM::");
    require([
        'dojo/request/xhr'
    ]
        , function (xhr) {

    print("::ENTER ATOM:: REQUIREMENTS");
    var htmlDivID = "contentDiv";
    
      // Parse ATOM feed
      xhr.get({
         url: feedUrl,
         preventCache: true,
         handleAs: "xml",
         load: function(xmlDoc, ioArgs){         
             var i = 0;
             var htmlOutputContent = "";
          
             var node = xmlDoc.getElementsByTagName("feed").item(0);
         
             if (node == null) {
                 console.debug("ERROR: Error in parsing ATOM Feeds XML format.");                     
                 return;
             }
         
             var NumOfFeedsEntry = node.getElementsByTagName("entry").length;
         
             for (i = 0; i < NumOfFeedsEntry; ++i) {
                var entry = node.getElementsByTagName('entry').item(i);
                 
                var title = entry.getElementsByTagName('title').item(0).firstChild.data;
                 var published = entry.getElementsByTagName('published').item(0).firstChild.data;            
                 var summary = entry.getElementsByTagName('summary').item(0).firstChild.data;
                 var link = entry.getElementsByTagName('link').item(0).getAttribute("href");
                 
                htmlOutputContent += '<hr><p><a target="_blank" href="' + link +'">' + title + '</a><br/>' + 
                          '<span class="smaller">' + published + '</span><br/>' + 
                          summary +
                          '</p>';
             }
             
             document.getElementById(htmlDivID).innerHTML = htmlOutputContent;             
         },
         error: function(error, ioArgs){                 
             dojo.byId(htmlDivID).innerHTML = "Error In Loading and Parsing The Atom Feeds";
             console.debug("ATOM URL CONTENT PASRING ERROR (DEBUG): ", error, ioArgs);             
         }
    });
    });
};  


dojoConfig = {
    baseUrl: "dojoSrc",
    async: 1,
    packages: [
        'dijit',
        'dijit-themes',
        'dojo',
        'dojox',
        'util'
    ]
};


load("jvm-npm.js");
load("nashorn:mozilla_compat.js");

importPackage(org.jdesktop.xpath);

print("::SUBTEST:: REQUIREMENTS LOADED");


var dojo = require("dojoSrc/dojo/dojo.js");

require([
    'dojo'
], function (dojo) {
    print("FUCK YOU");
    if (dojo == null){
        print("FUCK YOU ALL");
    }
    print(dojo.version);
});

print("::SUBTEST:: DOJO REQUIRED");


print("::SUBTEST:: DOJO VERSION");

