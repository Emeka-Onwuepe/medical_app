import requests
from datetime import datetime

from variables import phone_id, token


def send_whatsapp_message_func(message,sender):
    url = f"https://graph.facebook.com/v22.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": sender,
        "type": "text",
        "text": {
            "body": message
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.text)
    return response

def convert_whatsapp_timestamp(timestamp):
    return datetime.fromtimestamp(int(timestamp)).astimezone()

def get_message(data):
    context = 'medical_practitioner'
    messages = data['entry'][0]['changes'][0]['value']['messages'][0]
    sender = messages['from']
    message_type = messages['type']
    record_format = 'text'
    if message_type == 'text':
        content = messages['text']['body']
    else:
        content = messages[message_type]['id']
        record_format = messages[message_type]['mime_type'].split('/')[1]
    id = messages['id']
    timestamp = messages['timestamp']
    verify_context = messages.get('context')
    if verify_context:
        context = 'patient'
    return {'record_type':message_type, 'context':context,
            'content':content,'record_id':id,
            "timestamp": convert_whatsapp_timestamp(timestamp),
            'record_format':record_format, 'sender':sender}
    



# {
#   "field": "messages",
#   "value": {
#     "messaging_product": "whatsapp",
#     "metadata": {
#       "display_phone_number": "16505551111",
#       "phone_number_id": "123456123"
#     },
#     "contacts": [
#       {
#         "profile": {
#           "name": "test user name"
#         },
#         "wa_id": "16315551181"
#       }
#     ],
#     "messages": [
#       {
#         "from": "16315551181",
#         "id": "ABGGFlA5Fpa",
#         "timestamp": "1504902988",
#         "type": "text",
#         "text": {
#           "body": "this is a text message"
#         }
#       }
#     ]
#   }
# }


# data3 = {'object': 'whatsapp_business_account', 
#  'entry': [{'id': '519993747869426', 
#             'changes': [{'value': {'messaging_product': 'whatsapp', 
#                                    'metadata': {'display_phone_number': '15551818928', 'phone_number_id': '534666619730859'}, 
#                                    'contacts': [{'profile': {'name': 'EMEKA ONWUEPE'}, 'wa_id': '2348132180216'}],
#                                    'messages': [{'from': '2348132180216', 'id': 'wamid.HBgNMjM0ODEzMjE4MDIxNhUCABIYIDcwMkE3NjYzRkUxMDUxRDQ5NDA3MzY0RUMzQzIxMjU3AA==', 
#                                                  'timestamp': '1737752784', 'text': {'body': 'Yes'}, 'type': 'text'}]}, 'field': 'messages'}]}]}


# data4 = {'object': 'whatsapp_business_account', 
#  'entry': [{'id': '519993747869426', 
#             'changes': [{'value': {'messaging_product': 'whatsapp', 
#                                    'metadata': {'display_phone_number': '15551818928', 'phone_number_id': '534666619730859'}, 
#                                    'contacts': [{'profile': {'name': 'EMEKA ONWUEPE'}, 'wa_id': '2348132180216'}],
#                                    'messages': [{'context': {'forwarded': True}, 
#                                                  'from': '2348132180216', 
#                                                  'id': 'wamid.HBgNMjM0ODEzMjE4MDIxNhUCABIYIDM0RUMyMkQ3RURBQ0U1MEE3NEEwOTg3RDdCQUU4NjAwAA==', 
#                                                  'timestamp': '1737753025', 
#                                                 'text': {'body': 'The sight of you vexing and stammering, e dey Sabi sweet me eeeh'}, 'type': 'text'}]}, 'field': 'messages'}]}]}


    
# print(get_message(data4))

# data1 = {'object': 'whatsapp_business_account', 
#  'entry': [{'id': '519993747869426', 
#             'changes': [{'value': {'messaging_product': 'whatsapp', 
#                                    'metadata': {'display_phone_number': '15551818928', 'phone_number_id': '534666619730859'}, 
#                                    'statuses': [{'id': 'wamid.HBgNMjM0ODEzMjE4MDIxNhUCABEYEjE4ODE5M0U5NDhGRUNDNzYzNAA=', 
#                                                  'status': 'read', 'timestamp': '1737755158', 'recipient_id': '2348132180216',
#                                                  'conversation': {'id': '078694ec27569781ab940f1392775786', 
#                                                                   'origin': {'type': 'service'}}, 
#                                                  'pricing': {'billable': True, 'pricing_model': 'CBP', 'category': 'service'}}]},
#                          'field': 'messages'}]}]}


# print(data1['entry'][0]['changes'][0]['value'].keys())
# print(data1['entry'][0]['changes'][0]['field'])

# # for d in data1['entry']:
# #     print(d)
# #     print('-------------------------------')

# {'object': 'whatsapp_business_account', 'entry': [{'id': '519993747869426',
#                                                 'changes': [{'value': {'messaging_product': 'whatsapp', 
#                                                                        'metadata': {'display_phone_number': '15551818928', 'phone_number_id': '534666619730859'},
#                                                                        'contacts': [{'profile': {'name': 'EMEKA ONWUEPE'}, 'wa_id': '2348132180216'}],
#                                                                        'messages': [{'from': '2348132180216', 'id': 'wamid.HBgNMjM0ODEzMjE4MDIxNhUCABIYIEFDOEIyQTU4MTVGQjVEMTU5MTg4RjU5RkFGN0UyOTk0AA==',
#                                                                                     'timestamp': '1738105784', 'type': 'image', 
#                                                                                     'image': {'mime_type': 'image/jpeg', 'sha256': 'fofx8QXQ1FXG412pH959yCMbR2qYpXbuw0OMm1t0aWw=', 
#                                                                                     'id': '503401162364441'}}]}, 'field': 'messages'}]}]}


# {'object': 'whatsapp_business_account', 
#  'entry': [{'id': '519993747869426', 
#             'changes': [{'value': {'messaging_product': 'whatsapp', 
#                                    'metadata': {'display_phone_number': '15551818928', 'phone_number_id': '534666619730859'},
#                                    'contacts': [{'profile': {'name': 'EMEKA ONWUEPE'}, 'wa_id': '2348132180216'}], 
#                                    'messages': [{'from': '2348132180216', 'id': 'wamid.HBgNMjM0ODEzMjE4MDIxNhUCABIYIEJBODZFQzVERDMwQjhEOEY0NUMyNzFGQUE1OTYyQzFCAA==', 'timestamp': '1738108711',
#                                                  'type': 'audio', 'audio': {'mime_type': 'audio/ogg; codecs=opus', 'sha256': '9eToXT58+oi7Jz8U3DWIJ90wXc8oYVHTRd3ITqiSq8o=', 'id': '1962350167582284', 'voice': True}}]}, 'field': 'messages'}]}]}


# {'object': 'whatsapp_business_account', 'entry': [{'id': '519993747869426', 'changes': [{'value': {'messaging_product': 'whats 'whatsapp', 'metadata': {'display_phone_number': '15551818928', 'phone_number_id': '534666619730859'}, 'contacts': [{'': {'naprofile': {'name': 'EMEKA ONWUEPE'}, 'wa_id': '2348132180216'}], 'messages': [{'context': {'from': '2348132180216', 'idMjM0ODE': 'wamid.HBgNMjM0ODEzMjE4MDIxNhUCABIYIERDNDRERkQyREJGRkNDN0U0Qzc0MzQ1NzRFMzQ5MEMxAA=='}, 'from': '2348132180216', 'id'MjE4MDI: 'wamid.HBgNMjM0ODEzMjE4MDIxNhUCABIYIDM4OTZBNjFCRDE5NTcxMkI1QkYyMzc3OTM3REIzQzkyAA==', 'timestamp': '1738365659', 'tex'text'}t': {'body': 'Ok'}, 'type': 'text'}]}, 'field': 'messages'}]}]}