from ast import main
import requests
import json
import pandas as pd  
import string

url = 'http://gateway.marvel.com/v1/public/characters'
# api_key_public = 'df1df21c1c99623b81866bda416893c8' 
# hash_value = '15015d7abd4c552016258693f24d6c9e' ###MD5_HASH(TS+PRIVATE_KEY+PUBLIC_KEY)

def get_marvel_chars(letter, limit_val, apikey_user, hash_user):
    query = dict(
    apikey = apikey_user,
    ts = '2',
    hash = hash_user,
    nameStartsWith = letter,
    limit = limit_val
    )

    # print(query)

    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, params=query, headers=headers) 

    res = response.json() ###res = dict dt

    #print(res['data']['results'], type(res['data']['results']))

    for i in range(len(res['data']['results'])):
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
    marvel = pd.DataFrame(res['data']['results'])

    marvel_new = marvel.loc[:,['name', 'events_no', 'series_no', 'stories_no', 'comics_no', 'id']]
    # print(marvel_new) 
    # print('Size of the dataframe = ', marvel_new.shape)

    return marvel_new

def filter_marvel_chars(df, col_name, filter):
    temp = df.query(filter)
    print(temp)
    print("The filtered dataframe's has ", temp.shape[0], " characters")

if __name__ == "__main__":
    df_list = []

    for i in (string.ascii_lowercase):
        try:
            df_list.append( get_marvel_chars(i, 50, 'df1df21c1c99623b81866bda416893c8', '15015d7abd4c552016258693f24d6c9e'))
            print("fetching characters with ", i )        
        except:
            print("Couldn't fetch characters: ", i)
    df = pd.concat(df_list, axis=0)
    print(df)

    filter_marvel_chars(df, "name", "name == 'Zeus'")
    filter_marvel_chars(df, "comics_no, stories_no", "`comics_no` >= 200 and `stories_no` >= 250")
