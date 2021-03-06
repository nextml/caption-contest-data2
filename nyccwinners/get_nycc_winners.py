# -*- coding: utf-8 -*-
"""nycc_winners.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BmAxnZWdk5_7CXn1_i1i8kqXxB4zkl6w
"""

import json
import requests

def make_contest_id_list():
    ids = {}
    with open('productionCaptionContestIds.json','r') as f:
        idslt748 = json.load(f)
    for k in idslt748.keys():
        no = int(k[-3:])
        ids[no] = idslt748[k]
    print(ids)
    # We dropped contest 748 annoyingly
    # Now let us get the ones from s3
    contest_log = requests.get('https://s3-us-west-2.amazonaws.com/mlnow-newyorker/contest_log.json').json()['contests']
    expids = {}
    for d in contest_log:
        no = d['contest_number']
        if no > 749:
            expids[no] = d['exp_uid']
    for k in expids:
        print(expids[k])
        d = requests.get('https://s3-us-west-2.amazonaws.com/mlnow-newyorker/%s/nyr_json.json'%expids[k]).json()['data']['primary']['cartoon']['cartoonId']
        ids[k] = d
    with open('NYCCcartoonIds.json', 'w') as f:
        json.dump(ids, f)
    print(ids)
    return ids


def get_winners(id):
    def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
        request = requests.post('https://graphql.newyorker.com/graphql', json={'query': query})
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

            
    # The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       
    query = """
    {
        cartoon(copilotId: "%s") {
            title
            contestFinalists {
                id
                text
                rating
            }
        }
    }
    """ % id
    result = run_query(query) # Execute the query
    print(result)
    return result

ids_dict = make_contest_id_list()
winners = []
for cartoonId in ids_dict.values():
    winners.append(get_winners(cartoonId))

with open('nyc_winners.json','w') as f:
    json.dump(winners, f)