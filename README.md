# Audio Analysis Dashboard
Provides some analytical capability given an audio transcript with timestamps

## Dependencies
Requires the following python packages:
* `pandas`
* `dash`, `dash-html-components`, `dash-core-components`; refer to https://dash.plot.ly/installation
* `colorlover`; refer https://plot.ly/ipython-notebooks/color-scales/

## Running the app
The main application is `app.py` located in the analytics folder.
If you're in the main repo folder you can start the web page by running the following at the command line:
```bash
python analytics/app.py
```
Once started a link to the page will be printed to the console, which by default is http://127.0.0.1:8050

## TODO
The following improvements are on the cards:
### Formatting
* Find a more visually appealing audio player
* Fix the formatting (margins)
### Features
* Audio playback visualisation
* Fix formatting of speaker timeline
* Add sentiment analysis graphing
* Re-sort word histogram when filtered on speaker
* Link audio playback time to other features such as speaker ID card
