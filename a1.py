import requests
import json
url = 'http://gateway.marvel.com/v1/public/characters'
api_key_public = 'df1df21c1c99623b81866bda416893c8' 
hash_value = '15015d7abd4c552016258693f24d6c9e' #MD5_HASH(TS+PRIVATE_KEY+PUBLIC_KEY)
query = dict(
    apikey = api_key_public,
    ts = '2',
    hash = hash_value,
    nameStartsWith = 'S',
    limit = '10'
)
print (query)

headers = {'Content-Type': 'application/json'}

newSession = requests.Session()

response = newSession.get(url, params=query, headers=headers, verify=False) 

res = response.json()

print(res)

# Serializing json
json_object = json.dumps(res, indent=4)

# Writing to sample.json
with open("marvel.json", "w") as outfile:
	outfile.write(json_object)
