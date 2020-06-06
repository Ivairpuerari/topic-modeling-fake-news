import json
import os
import re
from progress.bar import IncrementalBar

paths_to_read = []

words = ["fake news", "fake", "news", "misinformation", "falsehoods", "Social Media",
         "bad information", "pandemic of misinformation", "internet", "web", "Infodemiological",
         "infodemic", "rumors", "tweeters", "twitter", "social network", "facebook", "whatsapp", "instagram"]

articles = []


def match(text):
    if text == '':
        return False
    for word in words:
        if re.search(r'\s' + word + '\s', text, re.M | re.I) is not None:
            return True
    return False


def add_article(file):
    articles.append(file)


def get_title(data):
    return data['metadata']['title']


def get_abstract(data):
    try:
        return [abstract['text'] for abstract in data['abstract']][0]
    except IndexError:
        return ""
    except KeyError:
        return ""


def get_body(data):
    return " ".join([item['text'] for item in data['body_text']])


def save_article(article):
    articles.append(article)


def build_collection(data):
    article = get_title(data).replace('\n', '')
    article += get_abstract(data).replace('\n', '')
    article += get_body(data).replace('\n', '')
    save_article(article)


def read_file(file):
    with open(file, 'r') as json_data:
        data = json.load(json_data)
        if match(get_title(data)):
            build_collection(data)
            return
        if match(get_abstract(data)):
            build_collection(data)


def read_path(path):
    files = os.listdir(path)
    bar = IncrementalBar('Processing folder '+path, max=len(files))
    for file in files:
        read_file(path + '/' + file)
        bar.next()

    bar.finish()


[read_path(path) for path in paths_to_read]

path_to_write = ''

with open(path_to_write, 'w', encoding="utf-8") as fw:
    bar_write = IncrementalBar('Saving collection', max=len(articles))
    for line in articles:
        fw.write(line)
        bar_write.next()
    bar_write.finish()