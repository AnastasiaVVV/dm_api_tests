"""
curl -X 'PUT' \
  'http://5.63.153.31:5051/v1/account/74b47c08-c184-4ff9-8c8f-c92d20ee55bf' \
  -H 'accept: text/plain'
"""
import pprint
import requests


# url = 'http://5.63.153.31:5051/v1/account'
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json'
# }
# json = {
#     "login": "morugova_test",
#     "email": "morugova_test@mail.ru",
#     "password": "123456789"
# }
#
# response = requests.post(
#     url=url,
#     headers=headers,
#     json=json
# )


url = 'http://5.63.153.31:5051/v1/account/74b47c08-c184-4ff9-8c8f-c92d20ee55bf'
headers = {
    'accept': 'text/plain'
}

response = requests.put(
    url=url,
    headers=headers
)

print(response.status_code)
pprint.pprint(response.json())
response_json = response.json()
print(response_json['resource']['rating']['quantity'])