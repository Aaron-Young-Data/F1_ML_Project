import fastf1
from fastf1.core import Laps
import pandas as pd

class CleanData:
    def __init__(self):
        fastf1.Cache.enable_cache('Cache')

    def fastest_laps(self, session_data):
        # returns the fastest laps from given session object
        # checks if the session_data is a session object
        try:
            session_data.load()
        except AttributeError:
            raise Exception('session_data is not a session object')

        list_fastest_laps = list()
        drivers = pd.unique(session_data.laps['Driver'])
        for drv in drivers:
            drvs_fastest_lap = session_data.laps.pick_driver(drv).pick_fastest()
            list_fastest_laps.append(drvs_fastest_lap)

        fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
        return fastest_laps

    def order_laps_delta(self, laps:pd.DataFrame):
        pole_lap = laps.pick_fastest()
        laps['LapTimeDelta'] = laps['LapTime'] - pole_lap['LapTime']

        return laps[['Driver', 'LapTime', 'LapTimeDelta']]

