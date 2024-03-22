import requests
import os


#client = hubspot.Client.create(access_token=api_key)

def get_props_from_number(phone_number):
    api_key = os.environ.get("HUBSPOT_PRIVATE_APP_TOKEN")
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    url = f'https://api.hubspot.com/crm/v3/objects/contacts/search'
    query = {
        'query': f'"{phone_number}"',
        'filterGroups': [
            {
                'filters': [
                    {
                        'propertyName': 'mobilephone',
                        'operator': 'EQ',
                        'value': phone_number
                    }
                ]
            },
            {
                'filters': [
                    {
                        'propertyName': 'phone',
                        'operator': 'EQ',
                        'value': phone_number
                    }
                ]
            }
        ],
        'properties': [ "lastname", 
                        "firstname", 
                        "leadsource", 
                        "case_type", 
                        "hs_lead_status", 
                        "mobilephone", 
                        "phone"]
    }
    try:
        response = requests.post(url, headers=headers, json=query)
        data = response.json()
        returned_properties = data['results'][0]['properties']
        return returned_properties
    except Exception:
        return None
        

""" def get_properties(id):
    try:
        api_response = client.crm.contacts.basic_api.get_by_id(
            contact_id=id, 
            archived=False, 
            properties=["lifecyclestage", 
                        "lastname", 
                        "firstname", 
                        "leadsource", 
                        "case_type", 
                        "hs_lead_status", 
                        "mobilephone", 
                        "phone"]
        )
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling basic_api->get_by_id: %s\n" % e)
        """
#get_properties()
#print(get_id_from_number(" 262-291-0025"))