"""Read and display NOTAMs from the Nav Canada API

Download NOTAMS from the Nav Canada API and display them for the route
specified (airports only).

Installation:
    pip3 install -r requirements.txt

Usage:
    python3 canada-notams.py --radius 20 CYOW CYYZ

The --radius option specifies the search radius for NOTAMs around your
route in nautical miles (defaults to 25). The script will display the
NOTAMs in reverse order of date.


Started 2020-08-20 by David Megginson

Last updated 2020-08-22

"""

import argparse, csv, json, logging, requests, sys, urllib


#
# Check for Python3
#
if sys.version_info < (3,):
    raise RuntimeError("libhxl requires Python 3 or higher")


#
# Variables
#

logger = logging.getLogger("canada-notams")
""" Logger object for this module """

API_CALL = "https://plan.navcanada.ca/weather/api/alpha/?{points}&alpha=notam&radius={radius}"
""" Template for a NOTAM query """


#
# Functions
#

def load_airports (filename):
    """ Load airport locations from a CSV file
    (Refresh from https://ourairports.com/countries/CA/airports.csv)
    @param filename Path to the CSV file containing the OurAirports data export
    @returns a dict of lat/lon tuples keyed by airport identifiers
    """

    airport_locations = dict()
    with open(filename, "r") as input:
        reader = csv.DictReader(input)
        for airport in reader:
            lat = airport["latitude_deg"]
            lon = airport["longitude_deg"]
            airport = airport["gps_code"]
            airport_locations[airport] = (lat, lon,)
    return airport_locations


def load_notams (airports, radius=25, airport_data="ca-airports.csv"):
    """ Load the NOTAMs from the Nav Canada website
    @param airports A list of airport identifiers
    @param radius The search radius in nautical miles (defaults to 25)
    @param airport_data The file containing Canadian airport data
    @returns A list of NOTAM objects
    """
    
    # Load the airport data
    airport_locations = load_airports(airport_data)
    points = []
    for airport in airports:
        airport = airport.strip().upper()
        if not airport in airport_locations:
            logger.warning("Airport %s not found", airport)
            continue
        else:
            logger.debug("Adding %s to route", airport)
            latlon = airport_locations[airport]
            points.append("point={},{},{},site".format(float(latlon[1]), float(latlon[0]), urllib.parse.quote(airport)))

    # Make the API call to Nav Canada
    api_call = API_CALL.format(points="&".join(points), radius=radius)
    logger.debug("API call: %s", api_call)
    response = requests.get(api_call)
    response.raise_for_status()

    # Deduplicate NOTAMs (the "pk" field means "primary key")
    notams = {}
    for notam in response.json()["data"]:
        notams[notam["pk"]] = notam

    logger.debug("Found %d NOTAMs", len(notams))
    return notams.values()


def display_notams(notams):
    """ Dump NOTAMs to the standard output, sorted by reverse date
    @param notams A list of NOTAM objects
    """
    
    for notam in sorted(notams, reverse=True, key=lambda notam: notam.get("startValidity")):
        print("** Effective {}".format(notam["startValidity"]))
        print(notam["text"], "\n\n")


#
# Command-line invocation
#
if __name__ == "__main__":

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Parse command-line arguments
    p = argparse.ArgumentParser(description="Display Canadian NOTAMs");
    p.add_argument("-r", "--radius", type=int, help="Radius (nautical miles) to search around the airport", default=25)
    p.add_argument("airports", metavar="ID", nargs="+", help="Airport identifiers")
    args = p.parse_args()

    # Get and display the NOTAMs
    notams = load_notams(args.airports, args.radius)
    display_notams(notams)

    # Exit with a success code
    exit(0)

