import pandas as pd

from collect_data import GetData
from data_cleaning import CleanData

data = GetData()
clean = CleanData()

year_list = [2018, 2019, 2020, 2021, 2022, 2023]
full_data = pd.DataFrame()

for year in year_list:
    calendar = data.get_calender(year)
    races = calendar['EventName'].to_list()
    for race in races:
        all_sessions = data.session_list(calendar[calendar['EventName'] == race][['Session1',
                                                                                 'Session2',
                                                                                 'Session3',
                                                                                 'Session4',
                                                                                 'Session5']])
        sessions_practice = [x for x in all_sessions if 'Practice' in x]
        sessions_practice.append('Qualifying')
        sessions = sessions_practice
        if 'Practice' in sessions[len(sessions) - 1]:
            sessions = sessions.pop()
        print(sessions)
        for session in sessions:
            session_data = data.session_data(year=year, location=race, session=session)
            fastest_laps = clean.fastest_laps(session_data=session_data)
            if len(fastest_laps) == 0:
                break
            fastest_laps_ordered = clean.order_laps_delta(laps=fastest_laps)
            needed_laps = fastest_laps_ordered[['DriverNumber',
                                                'LapTime',
                                                'Sector1Time',
                                                'Sector2Time',
                                                'Sector3Time',
                                                'Compound',
                                                'Final_POS']]
            final = clean.time_cols_to_seconds(column_names=['LapTime',
                                                             'Sector1Time',
                                                             'Sector2Time',
                                                             'Sector3Time'],
                                               dataframe=needed_laps)
            final['session'] = session
            final['location'] = race
            final['year'] = year
            full_data = pd.concat([full_data, final])

print(full_data)
full_data.to_csv('data/ML data/data.csv')
