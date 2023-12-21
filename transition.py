import sys
import argparse
import json
import requests



def list_transitions(auth):

	transition_url="https://cloudidentity.atlassian.net//rest/api/3/issue/CI-109719/transitions"

	headers={
		"Accept":"application/json",
		"Content-Type":"application/json"
	}

	
	response=requests.get(transition_url,headers=headers,auth=auth)

	data=response.json() 
	print(data)

	transitions=data["transitions"]

	for transition in transitions:
		print(transition,"\n")

	# 111 = Start
	# 421 = Resolve

def make_transition(auth):
	
	make_transition_url="https://cloudidentity.atlassian.net/rest/api/3/issue/CI-109719/transitions"

	headers={
		"Accept":"application/json",
		"Content-Type":"application/json"
	}

	payload=json.dumps(
			{
				"fields":{
					"project":
					{

						"key":"CI"

					}
					
					
					},

					"transition": {
    						"id": "421"
  					}	
			}
			
		)

	response=requests.post(make_transition_url,data=payload,headers=headers,auth=auth)
	print(response.text)





def main(user,token):

	auth=(user,token)
	list_transitions(auth)
	make_transition(auth)
	

if __name__=="__main__":

	parser=argparse.ArgumentParser(description='Jira Credentials')
	parser.add_argument("JIRA_USER")
	parser.add_argument("JIRA_API_TOKEN")

	args=parser.parse_args()
	user=args.JIRA_USER
	token=args.JIRA_API_TOKEN

	main(user,token)
