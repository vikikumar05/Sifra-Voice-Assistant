import requests

api_address = "https://newsapi.org/v2/top-headlines?country=in&apiKey=3e2c5f3f9f6f4d2e8b6b1b4c7d7e0c5d"
json_data = requests.get(api_address).json()

ar=[]

def news():
    for i in range(0, 10):
        ar.append("Number" + str(i+1)+ json_data["articles"][i]["title"] + ".")

    return ar
