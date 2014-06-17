###EpaNet input

####EpaNetInp.py

Script which creates <u>partial</u> epanet input (*.inp) file - only sections [JUNCTIONS], [PIPES] and [Coords] are written and minor losses are calculated, based on user's input through "csv"" file - refer to input template.

In order to calculate minor losses, user should have **DWheadlosses.py** script <u>and</u> **k_factors.csv** in path. Files are in my github repo. 

**Note:** User should create two csv-files out of template excel file - one for nodes and other for pipes.

Dependancy: **numpy**


####MinorLoss.py

Calculates only minor losses in pipe line and print them in specified file. Useful for graphic input.

Requires DWheadloss.py script and k_factors.csv data file to be installed in pythonn path.

Dependancy: **numpy**


####InputTemplate.xls

Template file, consisting of two worksheets which should be exported to two separate csv-files - one for nodes and other for pipes.

#### Example

Example files, together with EpaNet network (InputTest.inp) file, which can be opened in EpaNet.

File **loss.csv** is example output of *MinorLoss.py* script.

**Disclaimer: ** Use scripts on your own risk - no any kind of warranty.

(c) D. Djokic, 2014

