from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from flask import send_from_directory
import boto3
import os


app = Flask(__name__)
app.debug = True
aws_access_key_id = os.environ["aws_access_key_id"]
aws_secret_access_key = os.environ["aws_secret_access_key"]
aws_region = os.environ["defaultRegion"]
aws_queue_url = os.environ["alexa_queue_url"]




def sendToQueue(txt):
	sqs = boto3.resource('sqs', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
	queue = sqs.Queue(aws_queue_url)
	response = queue.send_message(MessageBody=txt)
	return response.get('MessageId')

def sendMessage(txt):
	txt = txt.strip()
	txt = txt[:500]
	if (not txt):
		return "No text entered!"
	messageId = sendToQueue(txt)
	return "Thank you."



@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET'])
def hello():
	return render_template('home.html')

@app.route('/speak', methods=['POST'])
def speak():
	user_message = sendMessage(request.form['txt'])
	return render_template('thankyou.html', user_message = user_message)

@app.route("/sms", methods=['POST'])
def sms():
	user_message = sendMessage(request.form['Body'])
	return ""

if __name__ == "__main__":
	app.run(debug=True, use_reloader=True)