import requests
from utils import flatten_json, data_to_excel, data_to_gsheets


# SEARCH QUERIES
type = 'place' # type of search to perform
query = 'restaurants' # desired search query (e.g., restaurants, convenience store, etc.)
center = '16.817337, 96.171700' # center of search area (lat long)
radius = 5000 # distance from center in meters
fields = 'name, location, phone, description, website'
limit = 300 # number of listings to fetch at once


# GOOGLE SHEET SETUP
sheet_id = ''
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


# FACEBOOK SETUP
CLIENT_ID =
CLIENT_SECRET = ''
fb_token_params = {'client_id': CLIENT_ID,
                   'client_secret': CLIENT_SECRET,
                   'grant_type': 'client_credentials'}

fb_token_response = requests.get('https://graph.facebook.com/oauth/access_token', fb_token_params)
FB_ACCESS_TOKEN = fb_token_response.json()['access_token']


# QUERYING FACEBOOK
fb_search_params = {'type': type,
                    'q': query,
                    'center': center,
                    'distance': radius,
                    'fields': fields,
                    'access_token': FB_ACCESS_TOKEN,
                    'limit': limit}

locations = []

fb_search_response = requests.get('https://graph.facebook.com/search', fb_search_params)

while len(locations) < limit:
    print('locations:' , len(locations))
    print(fb_search_response.json())

    locations_json = fb_search_response.json()['data']

    for i in locations_json:
        flattened = flatten_json(i, '_')
        locations.append(flattened)

    if 'paging' in fb_search_response.json():
        next_url = fb_search_response.json()['paging']['next']
        fb_search_response = requests.get(next_url)



# data_to_excel(locations, 'Facebook Locale Search.xlsx', query)
data_to_gsheets('test.csv', locations, scope, sheet_id)










