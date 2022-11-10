import requests
import json

store_hash = 'hchlmxrf0p'
url = f'https://api.bigcommerce.com/stores/{store_hash}/v2/orders'

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    "X-Auth-Token": "dtfqm7e076muz8q7qrvcspn9h8parkb"
}

resp = requests.get(url, headers=headers)
print(resp)

new_user = requests.post(url, headers=headers, data=json.dumps(
    {
        "billing_address": {
            "first_name": "Jane",
            "last_name": "Doe",
            "street_1": "123 Main Street",
            "city": "Austin",
            "state": "Texas",
            "zip": "78751",
            "country": "United States",
            "country_iso2": "US",
            "email": "janedoe@email.com"
        },
        "products": [
            {
                "name": "BigCommerce Coffee Mug",
                "quantity": 1,
                "price_inc_tax": 50,
                "price_ex_tax": 45
            }
        ]
    }
))
print(new_user)
