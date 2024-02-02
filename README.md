# Scouting App 2023-2024

## Prerequisites

### Pypi Packages

- [`Flask`](https://pypi.org/project/Flask)
- [`google-api-python-client`](https://pypi.org/project/google-api-python-client)
- [`google-auth-httplib2`](https://pypi.org/project/google-auth-httplib2)
- [`google-auth-oauthlib`](https://pypi.org/project/google-auth-oauthlib)
- [`waitress`](https://pypi.org/project/waitress)

Install With
- Windows:  &emsp;`py -m pip install --upgrade Flask google-api-python-client google-auth-httplib2 google-auth-oauthlib waitress`
- Linux/Apple: &emsp;`python3 -m pip install --upgrade Flask google-api-python-client google-auth-httplib2 google-auth-oauthlib waitress`

### Google Sheets API

To set up the Google Sheets API, follow this [tutorial](https://developers.google.com/sheets/api/quickstart/python) up through the **Authorize credentials for a desktop application** header. Convert the OAuth json into one line, and save it for later.

In the repository root, run the command:

(Windows) &emsp; `py -m scoutingutil.configsetup`

(Linux) &emsp; `python3 -m scoutingutil.configsetup`

Input the values it asks for (one of them is the one line OAuth JSON). Once you finish, a config file will be generated for the Scouting App.

### Scouting UI

Make a copy of [this google sheet](https://docs.google.com/spreadsheets/d/1uGZ_Y-TE_1au2BciUUOWUa7XV6pJXrmi6vW5y2W4v1Y/edit?usp=sharing). This Scouting UI will work for any data sheet linked to it as long as the "versions" are right.

In the copy, go to the settings sheet in the spreadsheet and set the required values.
- `ID`: The ID of the data spreadsheet being used (read comment for detailed instructions)
- `GRAB`: The name of the sheet to get data from in the data spreadsheet.
- `CONSTANTS`: The name of the sheet to read constants from in the data spreadsheet.
- `ID COLUMN`: The column to use when identifying an "individual" between rows. An example would be a Team ID
- `LIMIT COLUMN`: The column to use when trying to limit how much data is viewed. An example would be the date the match happened.

#### Issues

Sometimes the appscripts functions won't load right for the graphs and all of them will have a name error. If this happens, delete the row/column then undo the delete (Ctrl + Z or **Edit** > **Undo**). This should make google sheets (hopefully) reload the appscripts.


## Run

To run the Scouting App, run the appropriate command in the repository root:

(Windows) &emsp; `py server.py`

(Linux) &emsp; `python3 server.py`

If the API token has not been generated, is missing, or is invalid, the app will try to generate a new one. Make sure you are doing the OAuth verification using the google account that has write access to the [Scouting UI Sheet](#scouting-ui).

## Contact

If you have any problems or questions:

1. Make an issue
2. Email me
