import csv
import io
import json
import os

from bs4 import BeautifulSoup
from flask import Flask, make_response, render_template, request
import requests

try:
    from robobrowser import RoboBrowser
except ImportError:
    RoboBrowser = None


FIXTURE_RETWEETS = {
    "alice": ["bob", "carol"],
    "bob": ["alice"],
    "carol": ["alice", "bob"],
}

app = Flask(__name__)


@app.route('/')
def search():
    return render_template('index.html')


@app.route('/health')
def health():
    return {
        "ok": True,
        "mode": "live-twitter" if os.environ.get("REWTEET_LIVE") == "1" else "offline-fixture",
    }


def get_tweets(handle, max_position=None):
    if RoboBrowser is None:
        raise RuntimeError("RoboBrowser is not installed")

    session = requests.Session()
    browser = RoboBrowser(session=session, parser="lxml")
    url = "https://twitter.com/i/profiles/show/" + handle + "/timeline/tweets?include_available_features=false&include_entities=false&reset_error_state=false"
    if max_position is not None:
        url = url + "&" + "max_position=" + max_position
    browser.open(url)
    result = json.loads(browser.response.content)
    min_position = result['min_position']
    soup = BeautifulSoup(result['items_html'], 'lxml')
    links = [link.get('href') for link in soup.find_all('a')]
    return min_position, links


def duplicates(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


def find_between(s, first="/", last="/status/"):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def get_retweets(handle):
    if os.environ.get("REWTEET_LIVE") != "1":
        return FIXTURE_RETWEETS.get(handle.lower(), [])

    min_position, links = get_tweets(handle)
    while True:
        min_position1, links1 = get_tweets(handle, min_position)
        links = links + links1
        if min_position1 is None:
            break
        min_position = min_position1

    cleaned_retweets = [find_between(x) for x in links if "/status/" in str(x)]
    return duplicates(cleaned_retweets)


def build_matrix(users):
    retweets_graph = {user: get_retweets(user) for user in users}
    rows = []
    for user in users:
        row = {"User": user}
        for other_user in users:
            row[other_user] = 1 if other_user in retweets_graph[user] else 0
        rows.append(row)
    return rows


def matrix_to_csv(users, rows):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["User"] + users)
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


@app.route('/results', methods=['GET', 'POST'])
def results():
    input_values = [value.strip() for value in request.form.getlist('input_text[]') if value.strip()]
    if not input_values:
        input_values = ["alice", "bob", "carol"]
    rows = build_matrix(input_values)
    resp = make_response(matrix_to_csv(input_values, rows))
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp


if __name__ == '__main__':
    try:
        from waitress import serve

        serve(app, host='0.0.0.0', port=8080)
    except ImportError:
        app.run(host='0.0.0.0', port=8080)
