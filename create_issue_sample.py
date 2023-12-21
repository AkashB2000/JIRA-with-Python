import sys
import argparse
import json
import requests
import pandas as pd
from auth import auth


def createTask():

	create_url="https://cloudidentity.atlassian.net//rest/api/2/issue"

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
					},
					"summary":"Scan Automation Testing 102",  # issue heading
					"description":"Scan Automation Testing 102",
					"issuetype":{
					"name":"Task"
					},
					"duedate": "2023-5-9",
					
    				

					}
			}
		)
		
	response=requests.post(create_url,headers=headers,data=payload,auth=auth)
	print(response.text)

def main():
	
	createTask()
	#listTasks(auth)
	
	

if __name__=="__main__":

	

	main()