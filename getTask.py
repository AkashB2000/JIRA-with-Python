import sys
import argparse
import json
import requests
import pandas as pd
from auth import auth

def getTask():

	get_url="https://cloudidentity.atlassian.net//rest/api/3/issue/CI-109970"

	headers={
		"Accept":"application/json",
		"Content-Type":"application/json"
	}

		

	response=requests.get(get_url,headers=headers,auth=auth)
	
	print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))








def main():


	
	getTask()
	#listTasks(auth)
	

if __name__=="__main__":

	# parser=argparse.ArgumentParser(description='Jira Credentials')
	# parser.add_argument("JIRA_USER")
	# parser.add_argument("JIRA_API_TOKEN")

	# args=parser.parse_args()
	# user=args.JIRA_USER
	# token=args.JIRA_API_TOKEN

	main()

