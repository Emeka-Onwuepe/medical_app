import json
import requests
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from platforms.helpers import get_message, send_whatsapp_message_func
from platforms.models import Whatsapp_Record
from variables import token, phone_id



# Create your views here.
@csrf_exempt 
def Whatsapp_Hooks(request, *args, **kwargs):
    if request.method == 'GET':
        VERIFY_TOKEN = '01948ea0-dc55-7b76-ae95-6bc44cc9f7e9'
        mode = request.GET['hub.mode']
        challenge = request.GET['hub.challenge']
        verify_token = request.GET['hub.verify_token']
       
        if mode == 'subscribe' and verify_token == VERIFY_TOKEN:
            return HttpResponse(challenge,status=200)
        

    if request.method == 'POST':
        # print(request.headers['Content-Type'])
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        try:
            if 'messages' in data['entry'][0]['changes'][0]['value'].keys():
                print('hello')
                message_type,forwarded,content,id,timestamp,record_format = get_message(data)
                print(message_type)
                if forwarded:
                    # customer messages
                    pass
                else:
                    pass
                    # practitioner message
                # send_whatsapp_message_func('message recieved')
        except KeyError:
            pass
        return HttpResponse("EVENT_RECEIVED", status=200)
    return HttpResponse("Invalid request", status=400)


def send_whatsapp_message(request,message):
    # print(request.__dict__)
    
    # response = send_whatsapp_message_func(message)
    # print('hello')
    # url = f"https://graph.facebook.com/v21.0/{phone_id}/messages"
    # headers = {
    #     "Authorization": f"Bearer {token}",
    #     "Content-Type": "application/json"
    # }
    # payload = {
    #     "messaging_product": "whatsapp",
    #     "to": '+2348132180216',
    #     "type": "text",
    #     "text": {
    #         "body": message
    #     }
    # }
    # response = requests.post(url, headers=headers, json=payload)
    return HttpResponse("hello my guy", status=200)


def get_media_file(request,image_id):
    image_endpoint = url = f"https://graph.facebook.com/v22.0/{image_id}"
    headers = {
        'Authorization': f'Bearer {token}'
        }
    get_image_url = requests.request("GET", image_endpoint, headers=headers, data={})
    if get_image_url.status_code != 200:
        return HttpResponse("Failed to retrieve media url", status=get_image_url.status_code)
    url = get_image_url.json()['url']
    print(url)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return HttpResponse(response.content, content_type=response.headers['Content-Type'])
    else:
        return HttpResponse("Failed to retrieve media file", status=response.status_code)
    
def get_abs(request):
    
    # print(allowed_hosts)
    record = Whatsapp_Record.objects.first()
    return HttpResponse(record.get_absolute_url(), status=200)