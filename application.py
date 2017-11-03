from flask import Flask
from flask import render_template
from flask import request
from flask import Response
import boto3


def sendToQueue(txt):
	sqs = boto3.resource('sqs', region_name='us-east-1')
	queue = sqs.Queue('https://sqs.us-east-1.amazonaws.com/192158051712/EvilAlexaQueue')
	response = queue.send_message(
		MessageBody=txt,
		)
	return response.get('MessageId')

def sendMessage(txt):
	txt = txt.strip()
	txt = txt[:500]
	if (not txt):
		return "No text entered!"
	messageId = sendToQueue(txt)
	return "Thank you."

application = Flask(__name__)
application.debug = True

@application.route('/', methods=['GET'])
def hello():
	return render_template('home.html')

@application.route('/speak', methods=['POST'])
def speak():
	user_message = sendMessage(request.form['txt'])
	return render_template('thankyou.html', user_message = user_message)

@application.route("/sms", methods=['POST'])
def sms():
	user_message = sendMessage(request.form['Body'])
	return ""
	#resp = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>" + user_message + "</Message></Response>"
	#return Response(resp, mimetype='text/xml')

if __name__ == "__main__":
	application.run(host='0.0.0.0')



