from flask import Flask
from flask import render_template
from flask import request
import boto3


def sendToQueue(txt):
	sqs = boto3.resource('sqs', region_name='us-east-1')
	queue = sqs.Queue('https://sqs.us-east-1.amazonaws.com/192158051712/EvilAlexaQueue')
	response = queue.send_message(
		MessageBody=txt,
		)
	return response.get('MessageId')

application = Flask(__name__)
application.debug = True

@application.route('/', methods=['GET'])
def hello():
	return render_template('home.html')

@application.route('/speak', methods=['POST', 'GET'])
def login():
	txt = request.form['txt'].strip()
	txt = txt[:500]
	if (not txt):
		return "No text entered!"
	messageId = sendToQueue(txt)
	return "Thank you. Will say \"" + txt + "\" soon."

if __name__ == "__main__":
	application.run()



