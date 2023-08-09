# curl -X GET "https://api.thinkific.com/api/public/v1/enrollments?page=1&limit=1000" -H  "accept: application/json"
import requests
import json
import pandas as pd



dictt =  {
      "id": [],
      "user_id": []
    #   "user_email": [],
    #   "user_name": [],
    #   "user_id": [],
    #   "course_name": [],
    #   "course_id": [],
    #   "percentage_completed": [],
    #   "expired": [],
    #   "is_free_trial": [],
    #   "completed": [],
    #   "started_at": [],
    #   "activated_at": [],
    #   "completed_at": [],
    #   "updated_at": [],
    #   "expiry_date":[]
    }
lst = []
dict2 = {
    'bundle_id':[]
}
lst2 = []
# /?page={page}&limit=1000
def get_courses_data(id):
    try:
        response_temp = requests.get(
                    f"https://api.thinkific.com/api/public/v1/courses/{id}",
                    headers={
                        "X-Auth-API-Key": '0af37f50be358db530e91f3033ca7b1d',
                        "X-Auth-Subdomain": "alnafi",
                        "Content-Type": "application/json"
                    })
        json_data = json.loads(response_temp.text)
        # print(json_data)
        return json_data
    except Exception as e:
        print("id not found", id)


def formatdate(datestr):
    date_string=datestr
    substring = date_string[:19]
    new_substring = substring.replace('T', " ")
    return new_substring


ids = [
    2292447, 2293684, 2277479, 2278274, 1385501, 1943275, 1718948, 1686288, 1686288, 2277382,
    2277262, 2275987, 2275972, 2275596, 1943641, 2275565, 2140528, 2277161, 1838744, 1771221,
    2275657, 2275805, 1828809, 1828809, 1828809, 1828809, 1697234, 1828809, 1828809, 1828809,
    2302028, 1828809, 1828809, 1828809, 1828809, 1697234, 1828809, 2302377, 1828809, 2252625,
    2321192, 2302377	
]




for id in ids:
    # for i in range(1,5):
    # print("bundle id: ",id)
    json_data = get_courses_data(id)
    try:
        if json_data:
            # print("in json")
            # for j in range(len(json_data)):
            # print("in json  for loop")
            dictt['id'].append(json_data['id'])
            dictt['user_id'].append(json_data['user_id'])

            lst.append(dictt)
            dictt =  {
            "id": [],
            "user_id": [],
            }
                
        else:
            print("there is no enrollment for this bundle id: ",id)
            dict2['bundle_id'] = id
            lst2.append(dict2)
            dict2 = {
            'bundle_id':[]
        }
    except Exception as e:
        print(e)
        print("json data empty",id)
        dict2['bundle_id'] = id
        lst2.append(dict2)

        dict2 = {
        'bundle_id':[]
        }


all_enrollments = pd.DataFrame(lst)
all_enrollments.to_csv("all_enrollments.csv",index=False)

empty_bundles = pd.DataFrame(lst2)
empty_bundles.to_csv("empty_all_enrollments.csv",index=False)