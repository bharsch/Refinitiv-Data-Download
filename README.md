# Downloading Time Series Data from Refinitiv

> [!NOTE]
> There are four Python code files. You can find instructions on how to use them in the sections below.

This Python Code allows you to:

1. retrieve the tickers of all constituents in an index
2. load time series data for specific or multiple stocks
3. export time series data in wide format as an XLSX file.

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

One Index:
If you want the constituents tickers of only one index, you can execute the function below. It takes the index and the date for which you want the constituents as arguments. 

```
date = "20241031"
index = "0#.SP400"

constituents = getSingleIndexConstituents(date, index)
```

Multiple Indices:
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

For both functions, the returned data will be a pandas data frame that contains as columns the names of the indices and as row values the tickers of the constituents of the indices. 

### Step 3: Load Time Series Data of a list of stocks

You can load any data field from Refinitiv which is accessible by the package ```refinitiv.data```. Currently, you are limited to the frequency intervals below:

- daily
- 1d
- 1D
- 7D
- 7d
- weekly
- 1W
- monthly
- 1M
- quarterly
- 3M
- 6M
- yearly
- 12M
- 1Y

Intraday data (hourly, minutes, etc.) is not supported at this time! 
To load this data, you can execute the function ```getIndexTimeSeries()```. 

It takes the following arguments:

- index_data -> Pandas Dataframe containing the list of stocks for each index. The format has to match the format used by the function ```getMultipleIndicesConstituents()```.
- index -> List of indices (i.e. column names in the Dataframe) for which you want to read the data.
- fields -> List of Refinitiv data fields that you want to load.
- start_date -> First date for which you want to load data for.
- end_date -> Last date for which you want to load data for.
- frequency -> Frequency of the data.
- dataset_prefix -> Name prefix of the CSV file that contains the downloaded data. 
- sleep_time -> Specific how many seconds you want to wait after downloading data for each constituent. 
- message_interval -> Define how many constituents (In Percent) have to be processed until you print a status message in the console. 
- saving_interval -> Define how many constituents (In Percent) have to be processed until you save the downloaded data as a CSV file.

The option to allow simultaneous data download & CSV export of the data allows you to save the data in defined frequencies to prevent data loss if the connection to Refinitiv interrupts during the downloading process. 

_Here is an example_:
```
daily_data_fields = [
    "TR.TotalReturn",
    "TR.PriceClose", 
    "TR.PriceToBVPerShare",
    "TR.CompanyMarketCap"
]

daily_time_series_data = getIndexTimeSeries(index_data = constituents, 
                                            index = ["0#.GDAXI", "0#.SP400"], 
                                            fields = daily_data_fields, 
                                            start_date = "2024-10-01", 
                                            end_date = "2024-10-31", 
                                            frequency = "daily", 
                                            dataset_prefix = "daily_time_series_data",
                                            sleep_time = 2, 
                                            message_interval = 0.2,
                                            saving_interval = 0.2)
```

### Step 4: Export data as XLSX file.

You can export the data in wide format (Data fields are sheets and constituents are column names) using the function ```exportTimeSeriesDataAsXLSX()```. It takes as arguments the pandas data frame returned by the ```getIndexTimeSeries()``` function, a dictionary containing the names of the value columns you want to export as well as the names of their respective Excel sheets. Finally, you need to specify the output file name. 

```
value_column_dictionary = {
        "Total Return": "ReturnTotal",
        "Price Close": "PriceClose",
        "Price To Book Value Per Share (Daily Time Series Ratio)": "MTBV",
        "Company Market Cap": "MCAP"
}

exportTimeSeriesDataAsXLSX(time_series_data = daily_time_series_data, 
                           value_column_dictionary = value_column_dictionary, 
                           output_file_name = "Output_Data/Refinitiv_Data")
```
