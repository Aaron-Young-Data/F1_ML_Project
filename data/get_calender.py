import pandas as pd

from collect_data import GetData
from data_cleaning import CleanData

data = GetData()
clean = CleanData()

year_list = [2018, 2019, 2020, 2021, 2022, 2023]
full_calender = pd.DataFrame()

for year in year_list:
    calendar = data.get_calender(year)
    full_calender = pd.concat([full_calender, calendar])

full_calender.to_csv('ML data\\calender.csv')


