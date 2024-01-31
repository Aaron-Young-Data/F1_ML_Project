from data.collect_data import GetData
from data.data_cleaning import CleanData

data = GetData()
clean = CleanData()

print(data.get_calender(year=2023))
session = data.session_data(year=2023, location='Bahrain', session='Q')
lap_data = clean.order_laps_delta(laps=clean.fastest_laps(session_data=data.session_data(year=2023, location='Austin', session='Q')))
print(lap_data)
data = clean.time_cols_to_seconds(column_names=['LapTime', 'LapTimeDelta'], dataframe=lap_data)
data.to_csv('data.csv')