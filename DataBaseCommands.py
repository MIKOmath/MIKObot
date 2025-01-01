from utils import *
from utils import ClassMeet
import requests
import json
import datetime
# Base URL for the API
BASE_API_URL = "http://127.0.0.1:8000/api/"
# Endpoints for fetching
SEMINARS_ENDPOINT = "seminars/"
SEMINARS_GROUPS_ENDPOINT="seminar-groups/"
# Full URL for the API
SEMINARS_API_URL = f"{BASE_API_URL}{SEMINARS_ENDPOINT}"
GROUPS_API_URL = f"{BASE_API_URL}{SEMINARS_GROUPS_ENDPOINT}"
def fetch_seminars( date_from=None,date=None):
    """
    Fetches seminar data from the API.
    Returns a list of seminar data if successful, raises an exception otherwise.
    """
    try:
        params = {}
        if date_from:
            params['start_date'] = date_from
        if date:
            params['date'] = date
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

def get_class(exact_date=None):
    """
    Returns list of ClassMeet objects, fetched from API
    """
    try:
        date_for_filter = datetime.date.today()
        if exact_date:
            seminar_data = fetch_seminars(date = date_for_filter)
        else:
            seminar_data = fetch_seminars(date_from=date_for_filter)
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
        return []

def get_groups():
    """
        Fetches seminar data from the API.
        Returns a list of seminar data if successful, raises an exception otherwise.
        """
    try:
        # Send a GET request to the seminars-groups API

        response = requests.get(GROUPS_API_URL)

        # Raise an HTTPError if the response was unsuccessful
        response.raise_for_status()

        # Parse the JSON response
        seminars_groups_json = response.json()
        groups=[]
        for raw_group in seminars_groups_json['results']:
            group = Group()
            group.load_from_json(raw_group)
            groups.append(group)
        return groups

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching seminars: {e}")
        return []
def get_group_by_id(ID):
    """
            Fetches seminar data from the API, by id.
    """
    try:
        # Send a GET request to the seminars-groups API

        response = requests.get(GROUPS_API_URL+f"{ID}/")

        # Raise an HTTPError if the response was unsuccessful
        response.raise_for_status()

        # Parse the JSON response
        seminars_groups_json = response.json()
        group = Group()
        group.load_from_json(seminars_groups_json)
        return group

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching seminars: {e}")
        return None
def add_class(kolo):
    pass


def start_class(seminar_id, token):
    """
    Updates the 'started' field of a specific seminar to True using the API.

    Args:
        seminar_id (int): ID of the seminar to update.
        token (str): The API token for authentication.

    Returns:
        dict: Response data or error message from the API.
    """
    endpoint = f"{BASE_API_URL}seminars/{seminar_id}/"
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    # The data to send in the PATCH request
    data = {
        "started": True
    }

    try:
        # Send a PATCH request to update the seminar
        response = requests.patch(endpoint, json=data, headers=headers)

        # Check for errors in the response
        if response.status_code == 200:
            print(f"Seminar {seminar_id} marked as started successfully.")
            return response.json()
        else:
            print(f"Failed to update seminar: {response.status_code}")
            return response.json()  # Return error details if available
    except requests.RequestException as e:
        print(f"Error connecting to the API: {e}")
        return {"error": str(e)}
def finish_class(seminar_id, token):
    """
    Updates the 'started' field of a specific seminar to True using the API.

    Args:
        seminar_id (int): ID of the seminar to update.
        token (str): The API token for authentication.

    Returns:
        dict: Response data or error message from the API.
    """
    endpoint = f"{BASE_API_URL}seminars/{seminar_id}/"
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    # The data to send in the PATCH request
    data = {
        "finished": True
    }

    try:
        # Send a PATCH request to update the seminar
        response = requests.patch(endpoint, json=data, headers=headers)

        # Check for errors in the response
        if response.status_code == 200:
            print(f"Seminar {seminar_id} marked as finished successfully.")
            return response.json()
        else:
            print(f"Failed to update seminar: {response.status_code}")
            return response.json()  # Return error details if available
    except requests.RequestException as e:
        print(f"Error connecting to the API: {e}")
        return {"error": str(e)}


