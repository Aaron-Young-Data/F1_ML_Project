from collect_data import GetData
from data_cleaning import CleanData

data = GetData()
clean = CleanData()

print(data.get_calender(year=2023))
session = data.session_data(year=2023, location='Bahrain', session='Q')
clean.fastest_laps(session_data=session)
ordered_laps = clean.order_laps_delta(laps=clean.fastest_laps(session_data=session))
print(ordered_laps)