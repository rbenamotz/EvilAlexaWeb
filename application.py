from flask import Flask
from flask import render_template
from flask import request
from flask import Response
import boto3
#import configparser



application = Flask(__name__)
application.debug = False
#parser = configparser.ConfigParser()
#parser.read("./config.ini")
#aws_access_key_id = parser["aws"]["aws_access_key_id"]
#aws_secret_access_key = parser["aws"]["aws_secret_access_key"]
#aws_region = parser["aws"]["defaultRegion"]
#aws_queue_url = parser["aws"]["alexa_queue_url"]
aws_access_key_id = os.environ["aws_access_key_id"]
aws_secret_access_key = os.environ["aws_secret_access_key"]
aws_region = os.environ["defaultRegion"]
aws_queue_url = os.environ["alexa_queue_url"]




def sendToQueue(txt):
	sqs = boto3.resource('sqs', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
	queue = sqs.Queue(aws_queue_url)
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



