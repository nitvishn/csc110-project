import json
import datetime
from typing import Any

def load_covid_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)['OWID_WRL']
        return data['data']

def new_cases_in_interval(case_data: dict[str, Any], start: datetime.datetime, end: datetime.datetime) -> int:
    return sum([case['new_cases'] for case in case_data if start <= datetime.datetime.strptime(case['date'], "%Y-%m-%d") <= end])

def new_cases_at_times(case_data, times, resolution):
    return [new_cases_in_interval(case_data, time, time + resolution) for time in times]

load_covid_data('data/owid-covid-data.json')