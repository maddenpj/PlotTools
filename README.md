## Plot Output .py

A simple command line driven plotting (csv for now) tool 

Uses matplotlib.

Features

* grep - filter the file to only the lines that contain data. 
	
      $ plotOutput.py Data.csv -g PlotMe
	  // will skip all lines that do not contain 'PlotMe'
* column select - Select which column of data to plot
* Data Aggregation - selects whether to aggregate the data or not
* STDIN - read from STDIN. Great for piping
	
      $ cat Data.csv | plotOutput.py -c 1
      // plots column 1 
* Data stream aggregation and scaling
	
      $ plotOutput <File1>:Scale1,<File2>:Scale2
      // This will plot the data in file1*Scale1 then aggregate it with File2*Scale2


