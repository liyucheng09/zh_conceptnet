import requests
import random
import json
from hashlib import md5
import pandas as pd

filepath='/Users/mac/Desktop/ConceptNet/Data/CommonsenseQA/'

appid = '20210426000802170'
appkey = 'o4ewlTPleD8MqNooMG4t'
from_lang = 'en'
to_lang =  'zh'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path


def load_data(type):
    data_path=filepath+type+'_rand_split.jsonl'
    output_path=filepath+type+'_rand_split_zh.jsonl'
    
    dataset = pd.read_json(data_path, orient="records", lines=True)
    question = dataset["question"].values
    for index,i in enumerate(question):
        # res = make_request(i['question_concept'])
        # res = json.loads(res)
        data = []
        data.append(i['question_concept'])
        for j in i['choices']:
            data.append(j["text"])
        data.append(i['stem'])
        query = "\n".join(data)
        res = make_request(query)
        # print(res['trans_result'][0]['dst'])
        res = json.loads(res)
        temp = []
        for dst in res['trans_result']:
            temp.append(dst["dst"])
        question_zh = {}
        question_zh['question_concept'] = temp[0]

        temp_list = []
        choice1 = {"label":"A"}
        choice1["text"] = temp[1]
        temp_list.append(choice1)

        choice2 = {"label":"B"}
        choice2["text"] = temp[2]
        temp_list.append(choice2)

        choice3 = {"label":"C"}
        choice3["text"] = temp[3]
        temp_list.append(choice3)

        choice4 = {"label":"D"}
        choice4["text"] = temp[4]
        temp_list.append(choice4)

        choice5 = {"label":"E"}
        choice5["text"] = temp[5]
        temp_list.append(choice5)


        question_zh['choice'] = temp_list
        question_zh['stem'] = temp[6]
        print(question_zh)

        dataset['question'][index] = question_zh

    dataset.to_json(output_path, orient="records", lines=True, force_ascii=False)
    
    # return data

def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def make_request(query):
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}   

    r = requests.post(url, params=payload, headers=headers)
    result = r.json() 

    return json.dumps(result, indent=4, ensure_ascii=False)


for i in ['train']:
    load_data(i)
    
    # print(dataset)

