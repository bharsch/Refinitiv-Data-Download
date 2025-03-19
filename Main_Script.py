##################################### (0) Import Packages #####################################

# General Packages

import pandas as pd
import os
import sys

local_path = r'C:\Users\Admin.Harsch\OneDrive - UT Cloud\Teaching\BA_Data_Download'
# local_path = r"C:\Users\mauri\Desktop\Projects\Work\Refinitiv-Data-Download"

os.chdir(local_path)
sys.path.append(local_path)

# Data API
import refinitiv.data as rd

from Functions_Index_Constituents import * 
from Functions_Loading_Data import * 
from Functions_Creating_XLSX import * 
##################################### (I) Open Refinitiv Connection #####################################

rd.open_session() 

##################################### (II) Load Constituents #####################################

data_request = {
    
        "0#.GDAXI": ["20250301", 1],
        "0#.SPX": ["20250301", 1]
}

constituents = getMultipleIndicesConstituents(data_request)

output_dir = "Output_Data"

# Check if the folder exists, create if not
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save CSV file
constituents.to_csv(os.path.join(output_dir, "constituents.csv"), index=False, sep=",")

##################################### (III) Load Time Series Data #####################################

#
#   Only add columns that are time series data. Data like TR.CommonName are not time series data and cannot be loaded
#

daily_data_fields = [
    "TR.TotalReturn",
    "TR.PriceClose",
    "TR.PriceToBVPerShare",
    "TR.CompanyMarketCap"
]

yearly_data_fields = [
    "TR.TRESGScore",
    "TR.EnvironmentPillarScore",
    "TR.SocialPillarScore",
    "TR.GovernancePillarScore",
    "TR.F.TotAssets"
]

#   Interval can be any of these:
#   
#   "daily", "1d", "1D", 
#   "7D", "7d", "weekly", "1W", 
#   "monthly", "1M", 
#   "quarterly", "3M", "6M", 
#   "yearly", "12M", "1Y"

daily_time_series_data = getIndexTimeSeries(index_data = constituents, 
                                            index = ["0#.SPX", "0#.GDAXI"], 
                                            fields = daily_data_fields, 
                                            start_date = "2012-03-01", # yyyymmdd
                                            end_date = "2025-03-01", 
                                            frequency = "daily", 
                                            dataset_prefix = "daily_time_series_data",
                                            sleep_time = 2, 
                                            message_interval = 0.2,
                                            saving_interval = 0.2)

yearly_time_series_data = getIndexTimeSeries(index_data = constituents, 
                                            index = ["0#.SPX", "0#.GDAXI"], 
                                            fields = yearly_data_fields, 
                                            start_date = "2012-03-01", 
                                            end_date = "2025-03-01", 
                                            frequency = "yearly", 
                                            dataset_prefix = "yearly_time_series_data",
                                            sleep_time = 2, 
                                            message_interval = 0.2,
                                            saving_interval = 0.2)

yearly_time_series_data.head()
daily_time_series_data.head()

##################################### (IV) Exporting XLSX Files #####################################

value_column_dictionary = {
        "Total Return": "ReturnTotal",
        "Price Close": "PriceClose",
        "Price To Book Value Per Share (Daily Time Series Ratio)": "MTBV",
        "Company Market Cap": "MCAP",
        "ESG Score": "ESGScore",
        "Environmental Pillar Score": "EnvironmentalScore",
        "Social Pillar Score": "SocialScore",
        "Governance Pillar Score": "GovernanceScore",
        "Total Assets": "TotalAssets"
}

data_frames_for_export = [daily_time_series_data, yearly_time_series_data]
merge_columns = ["Date", "Stock"]

#Merges dataframes together so that they are exported as one excel file
merged_time_series_data = mergeTimeSeriesData(data_frames_for_export, merge_columns)

exportTimeSeriesDataAsXLSX(time_series_data = merged_time_series_data, 
                           value_column_dictionary = value_column_dictionary, 
                           output_file_name = "Output_Data/BA_WiSe24_Data_US",
                           add_company_names = True) #Set to true if you want sheet with company common names

##################################### (I) Close Refinitiv Connection #####################################

rd.close_session() 
