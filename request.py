import requests
import json

store_hash = 'hchlmxrf0p'
url = f'https://api.bigcommerce.com/stores/{store_hash}/v3/customers'

headers = {
    'Content-Type': "application/json",
    "X-Auth-Token": "dtfqm7e076muz8q7qrvcspn9h8parkb"
}

resp = requests.get(url, headers=headers)
print(resp)

new_user = requests.post(url, headers=headers, data=json.dumps(
    [{
        "email": "qqqqq@qq.com",
        "first_name": "opp",
        "last_name": "wee"
    }]))
print(new_user)