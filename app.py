from flask import Flask, jsonify, render_template, request
from twilio.twiml.voice_response import VoiceResponse
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