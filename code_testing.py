import requests
# from django.shortcuts import render
# def get_media(request):
#     url = "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=1124584105820060&ext=1738205530&hash=ATvZ8BeUB3cyPT6uyd5Fx8IcuqSYY2Q1_HYFUd-u1aCh2A"
#     headers = {
#         'Authorization': 'Bearer EAAXrgbJ16VkBO9p8skbDcL4XAIBZCtNwLVpxImq0WThjSvenAZAiU6oZCpMlpB4Imr9LGA4ZCR6ybW8N7ZBXw2SF8XXB8K3q8sjZAiGty5m8kkCQ2N7jJUmZCxVcVsFlWisqzutPtSgkkxskTyH7oqftgeAMcPgQ9s8jxFozz4VCM1E7OmXCTsgFrdnI1wQgJORv1Vn7kbrRqGs4tCu6knQXQAMiZAoZD'
#     }

#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         media_url = response.url
#     else:
#         media_url = None

#     return render(request, 'media_display.html', {'media_url': media_url})


# import requests
# from django.http import HttpResponse

# url = "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=1124584105820060&ext=1738206635&hash=ATv4BrynWvFYnmQL02L3W7G9ru-ptlyAy5wvyZr56KvWPA"

# payload = {}
# headers = {
#   'Authorization': 'Bearer EAAXrgbJ16VkBO9p8skbDcL4XAIBZCtNwLVpxImq0WThjSvenAZAiU6oZCpMlpB4Imr9LGA4ZCR6ybW8N7ZBXw2SF8XXB8K3q8sjZAiGty5m8kkCQ2N7jJUmZCxVcVsFlWisqzutPtSgkkxskTyH7oqftgeAMcPgQ9s8jxFozz4VCM1E7OmXCTsgFrdnI1wQgJORv1Vn7kbrRqGs4tCu6knQXQAMiZAoZD'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.url)


import requests
import json
from variables import token, phone_id

url = "https://graph.facebook.com/v22.0/1124584105820060"

payload = json.dumps({
  "name": "Add your name in the body"
})
headers = {
  'Authorization': f'Bearer {token}',
  
}


# response = requests.request("GET", url, headers=headers, data=payload)
# data = response.json()['url']
# print(data)
# # print(json.dumps(response.text)['url'])
# print('done')

# api_key = 'a2799c4221aaa16735e5935d944722f3'
api_key = '86523673f36adc5023ad8a84e87bd931'
lat = 6.5456
lon = 3.3479
url = f'https://pro.openweathermap.org/data/2.5/forecast/climate?lat={lat}&lon={lon}&appid={api_key}'

url = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={api_key}'
url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}'
response = requests.request("GET", url)
data = response.json()
print(data)
# print(json.dumps(response.text)['url'])
print('done')



