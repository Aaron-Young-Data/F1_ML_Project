import fastf1
import pandas as pd


class GetData:
    def __init__(self):
        fastf1.Cache.enable_cache('Cache')

    def get_calender(self, year: int, testing=False):
        # returns the information for the schedule (Location, Date, Format, Session(s))
        schedule = fastf1.get_event_schedule(year=year, include_testing=testing)
        if schedule.empty:
            raise Exception('No Data Collected!')
        else:
            return schedule[['EventName',
                             'EventDate',
                             'EventFormat',
                             'Session1',
                             'Session2',
                             'Session3',
                             'Session4',
                             'Session5']]

    def session_data(self, year: int, location: str, session=None):
        session_data = fastf1.get_session(year=year, gp=location, identifier=session)
        return session_data

    def session_list(self, session_df: pd.DataFrame):
        sessions = [x for c in session_df.columns for x in session_df[c].value_counts()[:1].index]
        return sessions
