import json
import requests

url = "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=1"

payload = {}
headers= {
  "apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"
}

response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = json.loads(response.text)
print(status_code)
print(result['result'])

#one line
print(json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=1", headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result'])