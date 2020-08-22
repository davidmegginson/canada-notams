""" Read and display NOTAMs from the Nav Canada API

Started 2020-08-20 by David Megginson
"""

import argparse, csv, json, requests, sys

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


p = argparse.ArgumentParser(description="Display Canadian NOTAMs");
p.add_argument("-r", "--radius", type=int, help="Radius (nautical miles) to search around the airport", default=25)
p.add_argument("airports", metavar="ID", nargs="+", help="Airport identifiers")
args = p.parse_args()

# Load the airport data
airports = load_airports("ca-airports.csv")

notams = {}

# Iterate through the requested airports
for airport in args.airports:
    # Do we recognise the airport?
    ident = airport.strip().upper()
    if not ident in airports:
        print("Airport {} not found".format(ident), file=sys.stderr)
        continue
    else:
        latlon = airports[ident]

        # Make the API call
        response = requests.get(API_CALL.format(lat=latlon[0], lon=latlon[1], ident=ident, radius=args.radius))
        response.raise_for_status()

        # Add all the NOTAMs to the pool
        for notam in response.json()["data"]:
            notams[notam["pk"]] = notam

# Display the NOTAMs, sorted by reverse start validity
for notam in sorted(notams.values(), reverse=True, key=lambda notam: notam.get("startValidity")):
    print(notam["text"], "\n\n")
                        
exit(0)
