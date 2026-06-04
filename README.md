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

## Offline demo path

By default the server uses a fixture retweet graph for `alice`, `bob`, and
`carol`, so `/results` can return a CSV without Twitter scraping, pandas, or
Waitress:

```sh
python smoke_test.py
```

`/health` reports `offline-fixture`. Set `REWTEET_LIVE=1` to attempt the legacy
Twitter scraping path.

## Caveats

- The live code targets older Twitter web endpoints that are likely stale.
- Some notebook/script paths were exploratory and may need dependency and API updates before reliable execution.
- Use this repo as a research/archive artifact unless the scraping layer is modernized.
- Generated notebook checkpoints and IDE metadata are intentionally ignored.
