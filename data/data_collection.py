import pandas as pd

from collect_data import GetData, CleanData

data = GetData()
clean = CleanData()

year_list = [2018, 2019, 2020, 2021, 2022, 2023]
full_data = pd.DataFrame()

for year in year_list:
    calendar = data.get_calender(year)
    races = calendar['EventName'].to_list()
    for race in races:
        event_type = calendar[calendar['EventName'] == race]['EventFormat'].to_list()[0]
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
        event_data = pd.DataFrame()
        for session in sessions:
            session_data = data.session_data(year=year, location=race, session=session)
            fastest_laps = data.fastest_laps(session_data=session_data)
            if len(fastest_laps) == 0:
                break
            fastest_laps_ordered = clean.order_laps_delta(laps=fastest_laps, include_pos=False)
            needed_data = fastest_laps_ordered[['DriverNumber',
                                                'LapTime',
                                                'Sector1Time',
                                                'Sector2Time',
                                                'Sector3Time',
                                                'Compound',
                                                'AirTemp',
                                                'Rainfall',
                                                'TrackTemp',
                                                'WindDirection',
                                                'WindSpeed']]
            session_df = clean.time_cols_to_seconds(column_names=['LapTime',
                                                                  'Sector1Time',
                                                                  'Sector2Time',
                                                                  'Sector3Time'],
                                                    dataframe=needed_data)

            try:
                suffix = "FP" + str(int(session[-1:]))
            except:
                suffix = 'Q'

            if event_data.empty:
                event_data = session_df.add_suffix(suffix)
                event_data = event_data.rename(columns={f'DriverNumber{suffix}': 'DriverNumber'})
            else:
                session_df = session_df.add_suffix(suffix)
                session_df = session_df.rename(columns={f'DriverNumber{suffix}': 'DriverNumber'})
                event_data = pd.merge(event_data, session_df, on='DriverNumber', how="outer")
        event_data['event_name'] = race
        event_data['year'] = year
        event_data['event_type'] = event_type
        full_data = pd.concat([full_data, event_data])

print(full_data.count())
print(full_data)
full_data.to_csv('ML data/data.csv')
