import requests
import json
from secretvalues import api_key

TOXIC_THRESHOLD = .83
header = {'Content-type': 'application/json'}
url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={}'.format(api_key)
def format_json(message):
	data = {'comment': {'text': message}, 'languages': ["en"],'requestedAttributes': {'TOXICITY':{}, 'SEVERE_TOXICITY': {}} }
	return json.dumps(data)
def toxicity(message):
	toxic_json = requests.post(url, headers=header, data=format_json(message))
	toxic_json = toxic_json.json()
	try:
		score = toxic_json['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value']
		return score
	except Exception as e:
		print(toxic_json)
