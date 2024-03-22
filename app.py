from flask import Flask, jsonify, render_template, request
from twilio.twiml.voice_response import VoiceResponse
from hubspot_contacts import get_props_from_number
from lookup import lookup
import time
app = Flask(__name__)





@app.route('/')
def root_page():
	# Sample data to pass to the template
	title = "My Server"
	message = "Mazel Tov, you made it to the server!!!"
	subheading = "There's not really much to see here, so feel free to carry on. Thanks for stopping by and have a nice day!"
	link = giannis_link()
	return render_template("index.html", title=title, message=message, subheading=subheading, link=link)

@app.route("/data")
def get_data():
  # Sample data dictionary
	data = {
		"message": "this is sample data",
		"number": 34,
		"name": "Giannis Antetokounmpo",
		"status": "GOAT"
		
	}
	# Return the data as JSON using jsonify
	return jsonify(data)

def giannis_link(): 
    return "https://en.wikipedia.org/wiki/Giannis_Antetokounmpo"

def call_routing_logic(from_number):
    try:
        lookup_results = lookup(from_number).get_right_contact()
        print(lookup_results)
    except Exception as e:
        print(f'error searching for {from_number}, returning default value')
        return "414-336-7659"
    if type(lookup_results) != dict:
        print(f'contact not found or multiple contacts found for number {from_number}, returning default value')
        return "414-336-7659"
    if lookup_results["hs_lead_status"] == None:
        print("no lead status found, returning default value")
        return "414-336-7659"
    lead_status = lookup_results["hs_lead_status"].lower()
    case_type = lookup_results["case_type"]
    if 'future pay' in lead_status or 'at consult' in lead_status or 'after consult' in lead_status:
        print(f'contact found with lead status: {lead_status}')
        return "414-316-3555"
    elif 'active' in lead_status:
        print("contact found with active case")
        if case_type == "Chapter 13 Bankruptcy":
            print("active case found with chapter 13 Bankruptcy")
            return "414-395-4525"
        elif case_type == "Chapter 7 Bankruptcy":
            print("active case found with chapter 7 Bankruptcy")
            return "414-395-4513"
        elif case_type == "Chapter 128":
            print("active case found with chapter 128 Bankruptcy")
            return "414-395-4511"
    elif 'bad timing' in lead_status or 'no hire' in lead_status:
        print('contact found with no hire or rehired - no hire')
        return "414-567-3205"
    elif 'immigration' in lead_status:
        print('immigration contact found')
        return "414-567-3209"

    return "414-336-7569"


@app.route("/callRouter", methods=["POST"])
def handle_call():
    #print(request.form)
    print(f"call recieved from {request.form.get('From')}")
    from_number = request.form.get("From")
    
    #to_number = call_routing_logic(from_number)
    response = VoiceResponse()
    response.say("Hello, you made it this far, well done!")
    #response.hangup()
    response.dial("513-218-2332", caller_id=from_number)
    return str(response)

@app.route("/test-hubspot-lookup")
def hubspot_lookup_test():
    ret = get_props_from_number("+14146072404")
    return jsonify(ret)

@app.route("/testWebhook", methods=["POST"])
def test_hook():
    start = time.time()
    data = request.get_json()
    name = data['customer_name']
    number = data['customer_phone_number']
    print(f"call recieved from {name} at number {number} with the following routing logic results:")
    print(f"Number would be forwarded to {call_routing_logic(number)}")
    end = time.time()
    print(f"operations completed in {end - start} seconds")
    return "", 200