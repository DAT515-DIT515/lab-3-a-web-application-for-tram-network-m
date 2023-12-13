import requests
import json
import html
from urllib.parse import urlencode, urlparse, parse_qs

STOP_FILE = 'https://www.vasttrafik.se/reseplanering/hallplatslista/'
TRAM_FILE = '/Users/andyvungoc/PycharmProjects/DAT515/lab3/static/tramnetwork.json'

# Load tram network data
with open(TRAM_FILE, 'r') as tramfile:
    tram_data = json.load(tramfile)

# Extract unique stops from tram network data
stops = set()
for line in tram_data['lines']:
    stops.update(tram_data['lines'][line])

# Fetch stop information from the given URL
response = requests.get(STOP_FILE)
response.raise_for_status()

decoded_content = html.unescape(response.text.encode('ascii', 'ignore').decode('ascii'))
lines = decoded_content.split('\n')

stops_code = {}

for row in range(len(lines)):
    s = str(''.join(lines[row].strip(' ').split(',')))
    if s in stops:
        url_params = parse_qs(urlparse(lines[row-1]).query)
        stop_gid = url_params.get('stopAreaGid', [''])[0]
        stops_code[s] = f'https://avgangstavla.vasttrafik.se/?source=vasttrafikse-stopareadetailspage&stopAreaGid={lines[row-1][-19:-3]}'
    else:
        pass

# Save the URLs to JSON file
output_file = 'static/tram-url.json'
with open(output_file, 'w') as file:
    json.dump(stops_code, file, indent=2, ensure_ascii=False)

print(f"Stop URLs saved to {output_file}")