import requests

token = 'EAAXrgbJ16VkBO94M7rSJ2PyZBmr7Y0CWrwgxbOOuojqj21JX51AKnGr7FeEWYGSLffe1eLbWivP7DxIGBXX9r41XqrQFrjvVgDyt0znXx10QIlfY6MLcjINbM2BbPEUEmZBSZCzedktPHIk0iuGtkuKNL3gWqi8ctMeUmcDdJV0Ok21VPscvXbYUhyzmHoOZAxwqtytqVZBhzFUlbIdZCpWcgU07DZC'
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
    text = messages['text']['body']
    id = messages['id']
    timestamp = messages['timestamp']
    context = messages.get('context')
    if context:
        forwarded = context['forwarded']
    return forwarded,text,id,timestamp

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

