""" Read and display NOTAMs from the Nav Canada API

Started 2020-08-20 by David Megginson
"""

import csv, json, requests, sys

API_CALL = "https://plan.navcanada.ca/weather/api/alpha/?point={lon},{lat},{ident},site&alpha=notam&radius={radius}"
""" Template for a NOTAM query """

def load_airports (filename):
    """ Load airport locations from a CSV file
    (Refresh from https://ourairports.com/countries/CA/airports.csv)
    """
    airports = dict()
    with open(filename, "r") as input:
        reader = csv.DictReader(input)
        for airport in reader:
            lat = airport["latitude_deg"]
            lon = airport["longitude_deg"]
            ident = airport["gps_code"]
            airports[ident] = (lat, lon,)
    return airports


# Check usage
if len(sys.argv) != 2:
    print("Usage: python {} <airport-ident>".format(sys.argv[0]), file=sys.stderr)
    exit(2)

# Load the airport data
airports = load_airports("ca-airports.csv")

# Do we recognise the airport?
ident = sys.argv[1].strip().upper()
if not ident in airports:
    print("Airport {} not found".format(ident), file=sys.stderr)
    exit(1)
else:
    latlon = airports[ident]

# Always use a 50 nm radius for now
radius = 50


# Make the API call
response = requests.get(API_CALL.format(lat=latlon[0], lon=latlon[1], ident=ident, radius=radius))
response.raise_for_status()

# Display the NOTAMs, sorted by reverse start validity
info = response.json()
for notam in sorted(info["data"], reverse=True, key=lambda notam: notam.get("startValidity")):
    print(notam["text"], "\n\n")
                        
exit(0)
