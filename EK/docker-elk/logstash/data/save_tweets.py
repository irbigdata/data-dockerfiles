import time
import re
import csv
import os
import json
import requests
import json

url = 'https://www.sahamyab.com/guest/twiter/list?v=0.1'
count_needed, sleep_time = 1000, 60
count_sofar = 0
regex = r"#([^\s#]+)"
tweet_ids = set()

dest_path = "tweets"

while count_sofar < count_needed:
    response = requests.request(
        'GET', url, headers={'User-Agent': 'Chrome/61'})
    result = response.status_code
    if result == requests.codes.ok:
        tweets = response.json()['items']
        for tweet in tweets:
            try:
                if tweet["id"] not in tweet_ids:
                    # extracting the hashtags
                    hashtag_list = re.findall(regex, tweet["content"])
                    tweet['hashtags'] = hashtag_list
                    filename = os.path.join(dest_path, f"{tweet['id']}.json")
                    with open(filename, 'w', encoding="utf-8") as output_file:
                        output_file.write(json.dumps(tweet))
                        output_file.write('\n')
                    print(f"tweet ID : {tweet['id']}")
                    count_sofar += 1
                    tweet_ids.add(tweet["id"])

            except Exception as e:
                print("print exception: " + str(e))

    else:
        print("Response code error: " + str(result))
    print(f'Count of fetched tweets is {count_sofar}')
    time.sleep(sleep_time)
