from flask import Flask
app = Flask(__name__)

@app.route('/')
def root_page():
	# Sample data to pass to the template
	title = "My Server"
	message = "Mazel Tov, you made it to the server!!!"
	subheading = "There's not really much to see here, so feel free to carry on. Thanks for stopping by and have a nice day!"
	link = giannis_link()
	return render_template("index.html", title=title, message=message, subheading=subheading, link=link)
