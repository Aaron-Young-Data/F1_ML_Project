import pandas as pd

data = pd.read_csv('ML data/data.csv')
track_data = pd.read_csv('ML data/track_data.csv')

print(data)
print(track_data)

sprint_data = data[data['event_type'] != 'conventional'].fillna(value=0)
conventional_data = data[data['event_type'] == 'conventional']

sprint_data['is_sprint'] = 1
conventional_data['is_sprint'] = 0

final_data = pd.concat([sprint_data, conventional_data])

final_data.dropna(how='any', inplace=True)

final_data = pd.merge(final_data, track_data, on='event_name', how="outer")

final_data.replace(to_replace={'SOFT': 1,
                               'MEDIUM': 2,
                               'HARD': 3,
                               'INTERMEDIATE': 4,
                               'WET': 5,
                               'HYPERSOFT': 1,
                               'ULTRASOFT': 2,
                               'SUPERSOFT': 3,
                               'UNKNOWN': 0,
                               'TEST_UNKNOWN': 0
                               }, inplace=True)

testing_data = final_data[(final_data['year'] == 2023) & (final_data['event_name'] == 'Bahrain Grand Prix')]

testing_data.drop(columns=['event_name',
                           'year',
                           'event_type',
                           'Unnamed: 0',
                           'Sector1TimeQ',
                           'Sector2TimeQ',
                           'Sector3TimeQ',
                           'CompoundQ',
                           'AirTempQ',
                           'RainfallQ',
                           'TrackTempQ',
                           'WindDirectionQ',
                           'WindSpeedQ'], inplace=True)

final_data.drop(columns=['DriverNumber',
                         'event_name',
                         'year',
                         'event_type',
                         'Unnamed: 0',
                         'Sector1TimeQ',
                         'Sector2TimeQ',
                         'Sector3TimeQ',
                         'CompoundQ',
                         'AirTempQ',
                         'RainfallQ',
                         'TrackTempQ',
                         'WindDirectionQ',
                         'WindSpeedQ'], inplace=True)

testing_data = testing_data.astype(float)
final_data = final_data.astype(float)

testing_data.to_csv('ML data/testing_data_cleaned.csv', index=False)

final_data.to_csv('ML data/data_cleaned.csv', index=False)
