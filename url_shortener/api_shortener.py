from flask import Flask
from flask import request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.assignment
col = db.shortened_urls


def encode(url_id):
    # base 62 characters
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(characters)
    ret = []
    # convert base10 url_id into base62 url_id for having alphanumeric shorten url
    while url_id > 0:
        val = url_id % base
        # to db
        ret.append(characters[val])
        url_id = url_id // base
    # since ret has reversed order of base62 url_id, reverse ret before return it
    return "".join(ret[::-1])


@app.route('/', methods=['GET', 'POST'])
def short_d_url():
    given_url = request.args.get('url')
    given_url = str(given_url)

    # check for match for the url in db
    matches = col.find({"given_url": {"$eq": given_url}})
    matched = {}
    for match in matches:
        print(match)
        matched = match
    if matched:
        url_id = matched["id"]
        hits = matched["hits"] + 1
        seen_url = col.update({"id": url_id}, {'$set': {"hits": hits}})
        print(seen_url)
    # no match found
    else:
        urls = {}
        # checking whether collection is empty
        if col.count() == 0:
            # 10 billion urls can be stored
            url_id = 10000000000
            urls["given_url"] = given_url
            urls["id"] = url_id
            urls['hits'] = 1
            first_url = col.insert(urls)
            print(first_url)
        else:
            # adding url,id (id is +1 of id of the last entry in the collection)
            last = col.find().sort("_id", -1).limit(1)
            for akhri in last:
                bottom = akhri
            url_id = bottom['id'] + 1
            urls["given_url"] = given_url
            urls["id"] = url_id
            urls['hits'] = 1
            new_url = col.update({"id": url_id}, {'$setOnInsert': urls}, upsert=True)
            print(new_url)

    short_url = encode(url_id)
    # return redirect("upwards.in/" + short_url)
    return "upwards.in/" + short_url
