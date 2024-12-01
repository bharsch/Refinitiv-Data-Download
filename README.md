# Downloading Time Series Data from Refinitiv

> [!NOTE]
> There are four Python code files. You can find instructions on how to use them in the sections below.

1. Retrieving the tickers of all constituents in an index
2. Loading time series data for specific or multiple stocks
3. Exporting time series data in wide format as XLSX file.

## Code Structure

There are three .py scripts that contain functions:

1. Functions_Index_Consituents.py
2. Functions_Loading_Data.py
3. Functions_Creating_XLSX.py

The fourth .py script is the Main_Script.py which executes the functions defined in the other scripts. 
You don't need to explicitly execute any functions in any script other than Main_Script.py since it inherits all functions from the other scripts. 

## How to Execute Script

### Step 1: Open Refinitiv Workspace & Establish Connection

Open Refinitiv Workspace to allow the Python script to load data. The workspace needs to run for the entire time you execute the script. 
Next, connect to Refinitiv by executing section (I) of the Main_Script.py!

```
rd.open_session() 
```

### Step 2: Read Ticker Data of Constituents of Index

**One Index**
If you want the constituents tickers of only one index, you can execute the function below. It takes the index and the date for which you want the constituents as arguments. 

```

date = "20241031"
index = "0#.SP400"

constituents = getSingleIndexConstituents(date, index)
```

__Multiple Indices__
To get the tickers of more than one index, execute the code below. It takes a dictionary as argument. The key is the index. The value is a list where 

- the first position of the list is the required date and
- the second index is the sample size.

You can specify a sample size for the index. If you only want 25% of constituents of that index, set the value to 0.25 to randomly sample 25% of the data loaded. 

```
data_request = {
    
        "0#.GDAXI": ["20241031", 0.25],
        "0#.SP400": ["20241031", 0.05]
}

constituents = getMultipleIndicesConstituents(data_request)
```

