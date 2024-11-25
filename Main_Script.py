##################################### (0) Import Packages #####################################

# General Packages
import pandas as pd
import os

os.chdir(r'C:\Users\mauri\Desktop\Work\1) Current Employers\University of Tübingen (HIWI)\Department of Finance\10) Daten für Bachelorarbeiten aktualisieren\V3')

# Data API
import refinitiv.data as rd

from Functions_Index_Constituents import * 
from Functions_Loading_Data import * 
from Functions_Creating_XLSX import * 
##################################### (I) Open Refinitiv Connection #####################################

rd.open_session() 

##################################### (II) Load Constituents #####################################

data_request = {
    
        "0#.GDAXI": ["20241031", 0.25],
        "0#.SP400": ["20241031", 0.05]
}

constituents = getMultipleIndicesConstituents(data_request)
constituents.to_csv("Output_Data/constituents.csv", index = False, sep = ",")

##################################### (III) Load Time Series Data #####################################



daily_data_fields = [
    "TR.TotalReturn",
    "TR.PriceClose", 
    "TR.PriceToBVPerShare",
    "TR.CompanyMarketCap",
    "TR.F.TotAssets",
]

yearly_data_fields = [
    "TR.TRESGScore",
    "TR.EnvironmentPillarScore",
    "TR.SocialPillarScore",
    "TR.GovernancePillarScore"
]

#   Interval can be any of these:
#   
#   "daily", "1d", "1D", 
#   "7D", "7d", "weekly", "1W", 
#   "monthly", "1M", 
#   "quarterly", "3M", "6M", 
#   "yearly", "12M", "1Y"
#
#   IMPORTANT: Retrieving intraday data (hourly, minutes, etc.) is not supported in this script! 
#

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

yearly_time_series_data = getIndexTimeSeries(index_data = constituents, 
                                            index = "0#.GDAXI", 
                                            fields = yearly_data_fields, 
                                            start_date = "2010-01-01", 
                                            end_date = "2023-12-31", 
                                            frequency = "yearly", 
                                            dataset_prefix = "yearly_time_series_data",
                                            sleep_time = 2, 
                                            message_interval = 0.2,
                                            saving_interval = 0.2)

##################################### (IV) Exporting XLSX Files #####################################

##################################### (I) Close Refinitiv Connection #####################################

rd.close_session() 
