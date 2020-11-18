import requests

resp = requests.post('http://localhost:5000/api/directions', json = {'start_address':'5619 Belarbor St Houston TX','end_address':'5514 Griggs Rd Houston TX'})
print(resp.json())