whatsapp_history
================
A bunch of useful tools to process whatsapp history.
Initially I planned to do conversation analysis and so on, but the history provided by whatsapp is mostly lacking (does not include reply metadata for example), and it has been useful enough to just look at the messages themselves.
You are welcome to play with it an improve it.


Installation:
=============

* Clone the repository
* `python -m venv .venv --prompt whatsapp_history`
* `source .venv/bin/activate`
* `pip install -r requirements.txt`

Usage:
======

* From your whatsapp group, export chat history (no need for media files)
* Download the file, and extract the text file inside
* `python analyze.py INPUT_FILENAME output.json` will get you a json file with all the messages
* `python top_posters.py output.json` will get you the list of top posters with the number of messages per person
* `python upload.py output.json INDEX USERNAME` will upload the messages to elasticsearch
