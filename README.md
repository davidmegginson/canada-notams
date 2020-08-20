Canada NOTAMs
=============

Read NOTAMs from the Nav Canada API and display them in reverse start-validity datetime.


## Installation

Set up and activate a virtual environment if desired:

    python3 -m venv venv
    . venv/bin/activate
    
Load the dependencies:

    pip3 install -r requirements.txt


## Usage

Add a Canadian airport GPS code as a parameter. For CYYZ (Toronto Pearson):

    python3 canada-notams.py CYYZ
    
To page through the NOTAMs for CYVA (Vancouver):

    python3 canada-notams.py CYVR | less

Note that only Canadian airport codes recognized by ourairports.com will work.

NOTAMs will always be sorted most-recent first (using the start validity date).


## License

This code is in the Public Domain and comes with NO WARRANTY. See
UNLICENSE.md for details.
