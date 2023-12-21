import sys
import argparse
import json
import requests
import pandas as pd

def getComponentLead(auth,component):

	list_components="https://cloudidentity.atlassian.net/rest/api/3/project/CI/components"

	headers={
		"Accept":"application/json",
		"Content-Type":"application/json"
	}

	response=requests.get(list_components,headers=headers,auth=auth)
	components=response.json() #   list of components
	component_id=[]
	component_name=[]
	lead_id=[]
	lead_name=[]

	for component in components:
		#print(component,"\n\n")
		component_id.append(component["id"])
		component_name.append(component["name"])
		if "lead" in component.keys():
			lead_id.append(component["lead"]["accountId"])
			lead_name.append(component["lead"]["displayName"])
		else:
			lead_id.append("N.A")
			lead_name.append("N.A")

		

	comp_df=pd.DataFrame(zip(component_id,component_name,lead_id,lead_name),columns=["COMPONENT ID","COMPONENT NAME","LEAD ID","LEAD NAME"])
	print(comp_df)

	

def createTask(auth,summary):

	create_url="https://cloudidentity.atlassian.net//rest/api/2/issue"

	headers={
		"Accept":"application/json",
		"Content-Type":"application/json"
	}

	if TaskExists(auth,summary):

		print("Task already exists")
	else:

		assignee=getComponentLead(auth,"cig-certmgr")

		payload=json.dumps(
			{
				"fields":{
					"project":
					{

						"key":"CI"
					},
					"summary":summary,  # issue heading
					"description":"Issue  Created from Python",
					"issuetype":{
					"name":"Task"
					},
					"components": [
      					{
        					"name": "cig-certmgr"
      					}
    					],
					"assignee": {
      					"id": "63bba8ca0913ada386aa27d2"
    					}
    				

					}
			}
		)

		response=requests.post(create_url,headers=headers,data=payload,auth=auth)
		print(response.text)

def TaskExists(auth,summary):

	list_url="https://cloudidentity.atlassian.net//rest/api/3/search"

	q='project =CI AND summary~"{}"'.format(summary)
	query={
			'jql': q
		}

	headers={
		"Accept":"application/json",
		"Content-Type":"application/json"
	}


	response=requests.get(list_url,headers=headers,params=query,auth=auth)
	
	data=response.json()   # dictionary
	
	issues=data["issues"]  # list
	
	if len(issues)>0:
		return 1
	else:
		return 0


def listTasks(auth):


	list_url="https://cloudidentity.atlassian.net//rest/api/3/search"

	q='project=CI and assignee=63bba8ca0913ada386aa27d2'
	query={
			'jql': q
		}

	headers={
		"Accept":"application/json",
		"Content-Type":"application/json"
	}


	response=requests.get(list_url,headers=headers,params=query,auth=auth)
	data=response.json()   # dictionary
	issues=data["issues"]

	summary_list=[]
	key_list=[]

	for issue in issues:
		key_list.append(issue["key"])
		fields=issue["fields"]
		summary_list.append(fields["summary"])

	tasks=pd.DataFrame(zip(key_list,summary_list),columns=["ISSUE KEY","ISSUE SUMMARY"])
	print(tasks)

def resolve(auth,key):
	
	make_transition_url="https://demo999.atlassian.net/rest/api/3/issue/{}/transitions".format(key)
	comment_url="https://demo999.atlassian.net//rest/api/3/issue/{}/comment".format(key)

	headers={
		"Accept":"application/json",
		"Content-Type":"application/json"
	}

	comment_data=json.dumps({
		"body":{
		"type":"doc",
		"version":1,
		"content":[
			{
				"type":"paragraph",
				"content":[
				{
				"text":"Issue Resolved, Q4 report doesnt have it anymore",
				"type":"text"
				}
				]
				
			}
		]
		}
		})

	response=requests.post(comment_url,headers=headers,data=comment_data,auth=auth)

	transition_data=json.dumps(
			{
				"fields":{
					"project":
					{

						"key":"FLIP"

					}
					},

					"transition": {
    						"id": "31"
  					}	
			}
			
		)

	response=requests.post(make_transition_url,data=transition_data,headers=headers,auth=auth)

def main(user,token):

	auth=(user,token)
	
	#createTask(auth,"Sample Task from Python 2")
	#listTasks(auth)
	getComponentLead(auth,"cig-certmgr")
	

if __name__=="__main__":

	parser=argparse.ArgumentParser(description='Jira Credentials')
	parser.add_argument("JIRA_USER")
	parser.add_argument("JIRA_API_TOKEN")

	args=parser.parse_args()
	user=args.JIRA_USER
	token=args.JIRA_API_TOKEN

	main(user,token)

