import datorama
import requests
import pandas as pd
import json

headers = {
    'X-API-KEY': 'ADD API KEY HERE',
}

#  Get a list of Template IDs
templates_response = requests.get('https://public-api.process.st/templates', headers=headers, params={'limit':500})
templates_response_json = templates_response.json()
templates_df = pd.DataFrame(templates_response_json['data'])
id_list = templates_df["id"].tolist()


#  Loop through Tag endpoint with Template ID list as input
tags = []
for x in id_list:
    API_URL = "https://app.process.st/api/1/tag-memberships?templateId={}&v=4".format(x)
    tag_response = requests.get(API_URL, auth=('ADD API KEY HERE', ''))
    tag_response_json = tag_response.json()
    tags.append(tag_response_json)

res = [ele for ele in tags if ele != []]

#  Each line will have a column per Tag + Template combination
#  Loop through each line, and each column, and append Tag Name and Template ID to respective lists

a_list = []
b_list = []
for x in res:
    for line in x:
        a_list.append(line['tag']['name'])
        b_list.append(line['template']['id'])

 
#  Use Pandas to join our 2 lists
df = pd.DataFrame()
df['Template_ID']  = b_list
df['Tag_Name'] = a_list

#  Turn Dataframe into csv for Datorama ingestion
csv_string = df.to_csv()
datorama.save_csv(csv_string)
