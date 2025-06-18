import json
from django.db import IntegrityError
import requests
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from platforms.helpers import get_message, send_whatsapp_message_func
from platforms.models import Whatsapp_Record, Whatsapp_Temp_Record
from users.models import Medical_practitional_Meta_Data, Patient, User
from variables import token, phone_id,VERIFY_TOKEN
from django.utils import timezone



# Create your views here.
@csrf_exempt 
def Whatsapp_Hooks(request, *args, **kwargs):

    if request.method == 'GET':
        mode = request.GET['hub.mode']
        challenge = request.GET['hub.challenge']
        verify_token = request.GET['hub.verify_token']
       
        if mode == 'subscribe' and verify_token == VERIFY_TOKEN:
            return HttpResponse(challenge,status=200)
        

    if request.method == 'POST':
        session_minutes = 10
        
        print('message recieved')
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        try:
            if 'messages' in data['entry'][0]['changes'][0]['value'].keys():
                whatsapp_message = get_message(data)
                patient = None
                print(whatsapp_message)
                if (timezone.now() - whatsapp_message['timestamp']) > timezone.timedelta(minutes=session_minutes):
                    # remember to decide what to do with the message
                    return HttpResponse("EVENT_RECEIVED", status=200)
                
                sender =  whatsapp_message.pop('sender')
                # medical_practitioner = f"0{sender[3:]}"
                medical_practitioner = f"+{sender}"
                medical_practitioner = User.objects.get(phone_number=medical_practitioner) 
                md_meta,created = Medical_practitional_Meta_Data.objects.get_or_create(medical_practitioner=medical_practitioner)
                whatsapp_message['medical_practitioner'] = medical_practitioner
                previous_messages = Whatsapp_Temp_Record.objects.filter(medical_practitioner=medical_practitioner)
                print(md_meta) 
                if (timezone.now() - md_meta.last_opened) > timezone.timedelta(minutes=session_minutes):
                    md_meta.status = 'closed'
                    md_meta.current_patient = 'none'
                    md_meta.notified = False
                    md_meta.last_opened = timezone.now()
                    md_meta.save()
                    send_whatsapp_message_func("Session has been closed, please resend",sender)
                    return HttpResponse("EVENT_RECEIVED", status=200)
                
                if whatsapp_message['record_type'] == 'text' and whatsapp_message['context'] == 'medical_practitioner':
                    if whatsapp_message['content'].strip()[:4].lower() == 'copy':
                        _,identifier = whatsapp_message['content'].split(' ')
                        identifier = identifier.strip()
                        try:
                            patient  = Patient.objects.get(whatsapp_number=identifier)
                            md_meta.current_patient = patient.pk
                            md_meta.save()
                            send_whatsapp_message_func(f"{patient.full_name} has been identified",sender)
                            
                            for message in previous_messages:
                                Whatsapp_Record.objects.create(medical_practitioner=message.medical_practitioner,
                                                            patient = patient,context = message.content,
                                                            record_id = message.record_id,
                                                            record_type = message.record_type,
                                                            record_format = message.record_format,
                                                            content = message.content,
                                                            timestamp = message.timestamp
                                                            )
                                message.delete()
                            return HttpResponse("Patient Identified", status=200)
                        except Patient.DoesNotExist:
                            md_meta.current_patient = 'none'
                            md_meta.status = 'closed'
                            md_meta.notified = False
                            md_meta.save()
                            send_whatsapp_message_func(f"Patient with identifier {identifier} not found",sender)
                            return HttpResponse("Invalid request", status=400)
                        except IntegrityError:
                            pass
                    elif whatsapp_message['content'].lower().strip() == 'end':
                        md_meta.status = 'closed'
                        md_meta.current_patient = 'none'
                        md_meta.notified = False
                        md_meta.save()
                        send_whatsapp_message_func("Session has been closed",sender)
                        return HttpResponse("EVENT_RECEIVED", status=200)
                     
                if md_meta.status == 'closed' and md_meta.notified == False and md_meta.current_patient == 'none':
                    md_meta.notified = True
                    md_meta.status = 'open'
                    md_meta.last_opened = timezone.now()
                    md_meta.save()
                    msg = "Please Identify the patient with this record by writing COPY followed by the patient's phone number. \n Eg copy 080377****  \n Remember to send END to close the session"
                    response = send_whatsapp_message_func(msg,sender)
                    if response.status_code != 200:
                        md_meta.notified = False
                        md_meta.status = 'closed'
                        md_meta.save()
                    Whatsapp_Temp_Record.objects.create(**whatsapp_message)
                elif md_meta.current_patient !='none':
                    patient = Patient.objects.get(pk=int(md_meta.current_patient))
                    whatsapp_message['patient'] = patient
                    Whatsapp_Record.objects.create(**whatsapp_message)
                    
                    for message in previous_messages:
                        try:
                            Whatsapp_Record.objects.create(medical_practitioner=message.medical_practitioner,
                                                            patient = patient,context = message.context,
                                                            record_id = message.record_id,
                                                            record_type = message.record_type,
                                                            record_format = message.record_format,
                                                            content = message.content,
                                                            timestamp = message.timestamp
                                                            )
                            message.delete()
                        except IntegrityError:
                            pass

        except User.DoesNotExist:
            msg = 'You are not authorized to send messages to this number'
            send_whatsapp_message_func(msg,sender)
            return HttpResponse("Invalid request", status=400)
        return HttpResponse("EVENT_RECEIVED", status=200)
    return HttpResponse("Invalid request", status=400)


def send_whatsapp_message(request,message):
    send_whatsapp_message_func(message,'+2348132180216')
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


def get_media_file(request,media_id):
    image_endpoint = url = f"https://graph.facebook.com/v22.0/{media_id}"
    print('image_endpoint',image_endpoint)
    print('token',token)
    headers = {
        'Authorization': f'Bearer {token}'
        }
    get_image_url = requests.request("GET", image_endpoint, headers=headers, data={})
    if get_image_url.status_code != 200:
        print(get_image_url.json()) 
        return HttpResponse("Failed to retrieve media url", status=get_image_url.status_code)
    url = get_image_url.json()['url']

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # print(response.content)
        return HttpResponse(response.content, content_type=response.headers['Content-Type'])
    else:
        return HttpResponse("Failed to retrieve media file", status=response.status_code)
    
def get_abs(request):
    
    # print(allowed_hosts)
    record = Whatsapp_Record.objects.first()
    return HttpResponse(record.get_absolute_url(), status=200)

def facebook_privacy_policy_callback(request):
    """
    This is a placeholder view for the Facebook privacy policy callback.
    It can be used to handle any specific logic related to the callback.
    """

    # You can add any logic you need here, such as logging or redirecting.
    return HttpResponse("Facebook Privacy Policy Callback Received", status=200)


import base64
import hashlib
import hmac
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def facebook_data_deletion_callback(request):
    if request.method == 'POST':
        signed_request = request.POST.get('signed_request')
        data = parse_signed_request(signed_request)
        if not data:
            return JsonResponse({'error': 'Invalid signature'}, status=400)
        user_id = data.get('user_id')

        # Start data deletion
        status_url = 'https://www.<your_website>.com/deletion?id=abc123'
        confirmation_code = 'abc123'

        response_data = {
            'url': status_url,
            'confirmation_code': confirmation_code
        }
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def parse_signed_request(signed_request):
    try:
        encoded_sig, payload = signed_request.split('.', 1)
        secret = b'appsecret'  # Use your app secret here

        sig = base64_url_decode(encoded_sig)
        data = json.loads(base64_url_decode(payload))

        expected_sig = hmac.new(secret, payload.encode(), hashlib.sha256).digest()
        if sig != expected_sig:
            # Bad signature
            return None
        return data
    except Exception:
        return None

def base64_url_decode(input_str):
    input_str += '=' * (-len(input_str) % 4)  # Pad with '='
    return base64.urlsafe_b64decode(input_str)