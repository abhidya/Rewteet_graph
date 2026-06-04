# Rewteet Graph

Experiment for building a retweet-overlap matrix between Twitter accounts and exporting the result as CSV.

## What is here

- `server.py` - Flask/Waitress web form that accepts handles and returns a CSV matrix.
- `retweets.py` - notebook-oriented helper functions for scraping retweet relationships.
- `stalker.py` - exploratory Twitter profile/location scraping utilities.
- `templates/index.html` - web form template.
- `Untitled*.ipynb` - exploratory notebooks.

## Run locally

The original app expects Python dependencies such as Flask, Waitress, pandas, requests, BeautifulSoup, and RoboBrowser.

```sh
python server.py
```

Then open:

```text
http://localhost:8080
```

## Caveats

- The code targets older Twitter web endpoints that are likely stale.
- Some notebook/script paths were exploratory and may need dependency and API updates before reliable execution.
- Use this repo as a research/archive artifact unless the scraping layer is modernized.
