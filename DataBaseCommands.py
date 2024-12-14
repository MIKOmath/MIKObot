from utils import *
from utils import ClassMeet
import requests
import json
import datetime
# Base URL for the API
BASE_API_URL = "https://mikomath.org/api/"
# Endpoint for seminars
SEMINARS_ENDPOINT = "seminars/"
# Full URL for the seminars API
SEMINARS_API_URL = f"{BASE_API_URL}{SEMINARS_ENDPOINT}"

def fetch_seminars( date_from=None):
    """
    Fetches seminar data from the API.
    Returns a list of seminar data if successful, raises an exception otherwise.
    """
    try:
        params = {}
        if date_from:
            params['start_date'] = date_from
        # Send a GET request to the seminars API

        response = requests.get(SEMINARS_API_URL,params = params)

        # Raise an HTTPError if the response was unsuccessful
        response.raise_for_status()

        # Parse the JSON response
        seminars = response.json()
        return seminars

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching seminars: {e}")
        raise

def get_class():
    try:


        date_from_filter = datetime.date.today()

        seminar_data = fetch_seminars(date_from=date_from_filter)
        sorted_seminars = sorted(
            seminar_data['results'],
            key=lambda x: x.get("date", "")
        )
        kola=[]
        for kolo_raw in sorted_seminars:
            kolo=ClassMeet()
            kolo.load_from_api(kolo_raw)
            kola.append(kolo)
        return kola
    except Exception as e:
        print(f"Failed to fetch seminars: {e}")

def add_class(kolo):
    pass