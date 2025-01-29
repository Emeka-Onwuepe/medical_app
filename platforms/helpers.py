import requests

token = 'EAAXrgbJ16VkBO98cHwL1PU5BhHZAh95yHRbkb0ZBD69OEK7bWku3DS5iCllzbUK4yMax8zRrEd8AFy6BvnkZCi6DkdKFgOdDgnezAImS81TB5buEL2c74UTst532z1ZCBLFsm34ssjIv5LZCIcrj3j90GhaZArOzCLmCZA7R4ZC4HhkiHWeTF9xJfqlVvZCILtLiQqg100J2GG9vZAnJvSdekJkZCwUAJIZD'
phone_id = '534666619730859' 


def send_whatsapp_message_func(message):
    print('ran')
    url = f"https://graph.facebook.com/v21.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": '+2348132180216',
        "type": "text",
        "text": {
            "body": message
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response


def get_message(data):
    forwarded = False
    messages = data['entry'][0]['changes'][0]['value']['messages'][0]
    message_type = messages['type']
    if message_type == 'text':
        content = messages['text']['body']
    else:
        content = f"{messages[message_type]['id']}\{messages[message_type]['mime_type']}" 
    id = messages['id']
    timestamp = messages['timestamp']
    context = messages.get('context')
    if context:
        forwarded = context['forwarded']
    return message_type,forwarded,content,id,timestamp

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

{'object': 'whatsapp_business_account', 'entry': [{'id': '519993747869426',
                                                'changes': [{'value': {'messaging_product': 'whatsapp', 
                                                                       'metadata': {'display_phone_number': '15551818928', 'phone_number_id': '534666619730859'},
                                                                       'contacts': [{'profile': {'name': 'EMEKA ONWUEPE'}, 'wa_id': '2348132180216'}],
                                                                       'messages': [{'from': '2348132180216', 'id': 'wamid.HBgNMjM0ODEzMjE4MDIxNhUCABIYIEFDOEIyQTU4MTVGQjVEMTU5MTg4RjU5RkFGN0UyOTk0AA==',
                                                                                    'timestamp': '1738105784', 'type': 'image', 
                                                                                    'image': {'mime_type': 'image/jpeg', 'sha256': 'fofx8QXQ1FXG412pH959yCMbR2qYpXbuw0OMm1t0aWw=', 
                                                                                    'id': '503401162364441'}}]}, 'field': 'messages'}]}]}


{'object': 'whatsapp_business_account', 
 'entry': [{'id': '519993747869426', 
            'changes': [{'value': {'messaging_product': 'whatsapp', 
                                   'metadata': {'display_phone_number': '15551818928', 'phone_number_id': '534666619730859'},
                                   'contacts': [{'profile': {'name': 'EMEKA ONWUEPE'}, 'wa_id': '2348132180216'}], 
                                   'messages': [{'from': '2348132180216', 'id': 'wamid.HBgNMjM0ODEzMjE4MDIxNhUCABIYIEJBODZFQzVERDMwQjhEOEY0NUMyNzFGQUE1OTYyQzFCAA==', 'timestamp': '1738108711',
                                                 'type': 'audio', 'audio': {'mime_type': 'audio/ogg; codecs=opus', 'sha256': '9eToXT58+oi7Jz8U3DWIJ90wXc8oYVHTRd3ITqiSq8o=', 'id': '1962350167582284', 'voice': True}}]}, 'field': 'messages'}]}]}