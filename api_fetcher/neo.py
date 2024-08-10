import requests

def fetch_neo_data(api_key):
    url = f"https://api.nasa.gov/neo/rest/v1/feed?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['near_earth_objects']
    else:
        raise Exception(f"Failed to fetch NEO data: {response.status_code}")
