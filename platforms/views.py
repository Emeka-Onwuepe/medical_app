import json
import requests
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from platforms.helpers import get_message, send_whatsapp_message_func,token,phone_id




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
        data = json.loads(request.body.decode('utf-8'))
        try:
            if 'messages' in data['entry'][0]['changes'][0]['value'].keys():
                forwarded,text,id,timestamp = get_message(data)
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
    response = send_whatsapp_message_func(message)
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