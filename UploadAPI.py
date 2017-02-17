import requests
base_url = 'http://localhost:8080/api'
def UploadAPI(User, score, date):
    payload = {'name': str(User),'score': score, 'date': date}
    sendUserResults = requests.post(base_url + '/memoryGame', data=payload)
    print(sendUserResults)