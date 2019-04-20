import pandas as pd
from flask import Flask, render_template, request, make_response

import json as json
import requests
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
# from tqdm import tqdm_notebook as tqdm



app = Flask(__name__)


@app.route('/')
def search():
    return render_template('index.html')



def get_tweets(handle, max_position=None):
    session = requests.Session()
    browser = RoboBrowser(session=session, parser="lxml")
    url = "https://twitter.com/i/profiles/show/" + handle + "/timeline/tweets?include_available_features=false&include_entities=false&reset_error_state=false"
    if max_position != None:
        url = url + "&" + "max_position=" + max_position
    browser.open(url)
    result = json.loads(browser.response.content)
    min_position = result['min_position']
    soup = BeautifulSoup(result['items_html'], 'lxml')
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
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
    # handle = "AllCapsKristi"
    min_position, links = get_tweets(handle)
    while (True):
        min_position1, links1 = get_tweets(handle, min_position)
        links = links + links1
        if (min_position1 == None):
            break
        min_position = min_position1

    cleaned_retweets = [find_between(x) for x in links if "/status/" in str(x)]
    #   cleaned_retweets = [x for x in cleaned_retweets if x != handle]
    cleaned_retweets = duplicates(cleaned_retweets)
    return cleaned_retweets


def get_df(users):
    dataframe = []
    retweets_graph = {}

    for i in (users):
        retweets_graph[i] = get_retweets(i)

    for i in users:
        temp = []
        temp.append(i)
        for j in users:
            answer = ""
            if j in retweets_graph[i]:
                answer = 1
            else:
                answer = 0
            #     print(i, j, answer)
            temp.append(answer)
        # print(temp)
        dataframe.append(temp)

    df = pd.DataFrame(dataframe, columns=(["User"] + users), dtype=float)
    return df


@app.route('/results', methods=['GET', 'POST'])
def results():
    input_values = request.form.getlist('input_text[]')
    print(input_values)
    df = get_df(input_values)
    resp = make_response(df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp


if __name__ == '__main__':
    app.run(debug=True)
