from flask import Flask
from flask import render_template
from flask import request
import boto3


def sendToQueue(txt):
	sqs = boto3.resource('sqs', region_name='us-east-1')
	queue = sqs.Queue('https://sqs.us-east-1.amazonaws.com/192158051712/evailAlexa.fifo')
	response = queue.send_message(
		MessageBody=txt,
		MessageGroupId='messageGroup1'
		)
	return response.get('MessageId')

application = Flask(__name__)
application.debug = True

@application.route('/', methods=['GET'])
def hello():
	return render_template('home.html')

@application.route('/speak', methods=['POST', 'GET'])
def login():
	txt = request.form['txt']
	return sendToQueue(txt)

if __name__ == "__main__":
	application.run()



