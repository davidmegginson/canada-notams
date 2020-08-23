Canada NOTAMs
=============

Read NOTAMs for an airport or route from the Nav Canada API and
display them in reverse date.


## Installation

Set up and activate a virtual environment if desired:

    python3 -m venv venv
    . venv/bin/activate
    
Load the dependencies:

    pip3 install -r requirements.txt


## Usage

Add a Canadian airport GPS code as a parameter. For CYYZ (Toronto Pearson):

    python3 canada-notams.py CYYZ
    
For a flight from Toronto to CYVR (Vancouver):

    python3 canada-notams.py CYYZ CYVR
    
To page through the NOTAMs for CYUL (Montreal):

    python3 canada-notams.py CYVR | less

Note that only Canadian airport codes recognized by ourairports.com will work.

The default search radius is 25 nautical miles around your airport or
route. To change that, use the --radius option:

    python3 canada-notams.py --radius 50 CYRO
    
The script will deduplicate NOTAMs and display them sorted most-recent
first (using the start validity date).

You can also sort by radius distance fromt he airport/route rather
than date, but because of the way Nav Canada encodes its NOTAMs, the
result will usually not be what you expect:

    python3 canada-notams.py --sort distance --radius 50 CYRO
    

## License

This code is in the Public Domain and comes with NO WARRANTY. See
UNLICENSE.md for details.
