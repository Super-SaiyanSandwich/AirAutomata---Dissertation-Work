# AirAutomata - Dissertation-Work

For the Indivual Literature Review and Project (ECM3401) module.

## Visualisation and Prediction of Air Quality across the UK

This repository is the code that builds the core of the project, for the purpose of both storing a backup as well as using it to share it across my laptop, destop and the University computers.

The project is broken up into several sections:

### Data Readin

This section is design to download a parse the data fed to the DEFRA ATOM feeds, downloading all of the data for the pollutants needed to evaluate Air Quality.

Within the repository, there are two versions of this. Originally I planned to use JavaScript to download and parse the data using all of the libraries for such thing that exist, however in my implementation I came across many issues which I ultimately didn't have the confidence to overcome. The final issue was a lack of a HTTPS object within the nashorn version of JavaScript.

Due to these issues I switched to using Python, something I found unequivocally easier to implement and is the system I will be using for the foreseeable future when downloading the data. The old Java/JavaScript version is still present in the .zip file DataReadInJava.zip.

### Visualisation

This section, further broken down again, focuses on the aspect of the project related to visualising all the data either downloaded or produce by the system designed. This is an important area to experiment with as representing the data can be difficult to get right on the first try, there may always be a more appropriate method to do so.
