VENV=./venv/bin/activate

run: $(VENV)
	. $(VENV) && python canada-notams.py CYRO CYGK

venv: $(VENV)

$(VENV): requirements.txt
	python3 -m venv venv && . $(VENV) && pip install -r requirements.txt

