import requests
import json

url = 'http://gateway.marvel.com/v1/public/characters'
api_key_public = 'df1df21c1c99623b81866bda416893c8' 
hash_value = '15015d7abd4c552016258693f24d6c9e' ###MD5_HASH(TS+PRIVATE_KEY+PUBLIC_KEY)
query = dict(
    apikey = api_key_public,
    ts = '2',
    hash = hash_value,
    nameStartsWith = 'M',
    limit = '50'
)

print(query)

headers = {'Content-Type': 'application/json'}

response = requests.get(url, params=query, headers=headers) 

res = response.json() ###res = dict dt

#print(res['data']['results'], type(res['data']['results']))

for i in range(res['data']['count']):
    res['data']['results'][i]['comics_no'] = res['data']['results'][i]['comics']['available']
    res['data']['results'][i]['series_no'] = res['data']['results'][i]['series']['available']
    res['data']['results'][i]['stories_no'] = res['data']['results'][i]['stories']['available']
    res['data']['results'][i]['events_no'] = res['data']['results'][i]['events']['available']

###Serializing json
json_object = json.dumps(res, indent=4) ###json_object = str dt

###Writing to marvel.json
new_file = 'marvel.json'
with open(new_file, 'w') as outfile:
	outfile.write(json_object)
    
###converting json dataset from dictionary to dataframe
import pandas as pd  
marvel = pd.DataFrame(res['data']['results'])

marvel_new = marvel.loc[:,['name', 'events_no', 'series_no', 'stories_no', 'comics_no', 'id']]
print(marvel_new) 
print('Size of the dataframe = ', marvel_new.shape)