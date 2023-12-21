import sys
import argparse
import json
import requests
import pandas as pd

def createIssues(auth,report):

	create_url = "https://cloudidentity.atlassian.net//rest/api/2/issue"

	scan=pd.read_csv(report).drop_duplicates(subset=['DependencyName'])  #removing duplicate DependencyNames
	scan.fillna('none',inplace=True)  ##replace NaN values with 'none' String
	
	filt=~((scan['DependencyName'].str.contains('com.ibm.security.access.')) | (scan['DependencyPath'].str.contains('cucumber')))  #remove  com.ibm.security deoendencies
	filtered_report=scan.loc[filt]
	

	in_report=[]
	ScanDate=formatDate(filtered_report.iloc[1,1])
	
	
	for row in range(len(filtered_report)): 
	    col=0
	    Project=filtered_report.iloc[row,col]
	    col+=1
	    ScanDate=filtered_report.iloc[row,col]
	    col+=1
	    DependencyName=filtered_report.iloc[row,col]
	    col+=1
	    DependencyPath=filtered_report.iloc[row,col]
	    col+=1
	    Description=filtered_report.iloc[row,col]
	    col+=1
	    License=filtered_report.iloc[row,col]
	    col+=1
	    Md5=filtered_report.iloc[row,col]
	    col+=1
	    Sha1=filtered_report.iloc[row,col]
	    col+=1
	    Identifiers=filtered_report.iloc[row,col]
	    col+=1
	    CPE=filtered_report.iloc[row,col]
	    col+=1
	    CVE=filtered_report.iloc[row,col]
	    col+=1
	    CWE=filtered_report.iloc[row,col]
	    col+=1
	    Vulnerability=filtered_report.iloc[row,col]
	    col+=1
	    Source=filtered_report.iloc[row,col]
	    col+=1
	    CVSSv2_Severity=filtered_report.iloc[row,col]
	    col+=1
	    CVSSv2_Score=filtered_report.iloc[row,col]
	    col+=1
	    CVSSv2=filtered_report.iloc[row,col]
	    col+=1
	    CVSSv3_BaseSeverity=filtered_report.iloc[row,col]
	    col+=1
	    CVSSv3_BaseScore=filtered_report.iloc[row,col]
	    col+=1
	    CVSSv3=filtered_report.iloc[row,col]
	    col+=1
	    CPE_Confidence=filtered_report.iloc[row,col]
	    col+=1
	    Evidence_Count=filtered_report.iloc[row,col]

	    description="Project : {}\n".format(Project) + "Scan Date : {}\n".format(ScanDate) + "DependencyName : {}\n".format(DependencyName) + "DependencyPath: {}\n".format(DependencyPath) +"Description : {}\n".format(Description) + "License: {}\n".format(License) + "Md5 : {}\n".format(Md5) + "Identifiers: {}\n".format(Identifiers) + "CPE: {}\n".format(CPE) + "CVE: {}\n".format(CVE) + "CWE: {}\n".format(CWE) + "Vulnerability: {}\n".format(Vulnerability) + "Source: {}\n".format(Source)+ "CVSSv2_Severity: {}\n".format(CVSSv2_Severity) + "CVSSv2_Score: {}\n".format(CVSSv2_Score) + "CVSSv2: {}\n".format(CVSSv2) + "CVSSv3_BaseSeverity: {}\n".format(CVSSv3_BaseSeverity)+ "CVSSv3_BaseScore: {}\n".format(CVSSv3_BaseScore) + "CVSSv3: {}\n".format(CVSSv3) + "CPE_Confidence : {}\n".format(CPE_Confidence) + "Evidence_Count: {}\n".format(Evidence_Count)

	    summary="[Twistlock DependencyScan '{}'] :Vulnerability found in ".format(report[:-4]) + DependencyName ## what if entire report path is provided, then include just the report name
	    print(summary)
	    in_report.append(summary)
	  
	    if issueExists(auth,DependencyName):
	      print("Issue already exists")
	      continue

	    print("Create issue")
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
									"summary":summary,  
									"description":description,
									"components": [
					      				{
					        				"name": "cig-reqmgr"   # remove hardcoding
					      				}
					    				],
										
								"issuetype":{
								 		"name":"Scan Vulnerability"
								 		},
								"customfield_11377": {
					            "id": "11382",
					            "self": "https://cloudidentity.atlassian.net/rest/api/3/customFieldOption/11382",
					            "value": "Twistlock"
					        			},		 
					        	"duedate": "2023-03-4",
					        	"customfield_11343": ScanDate # Scan Report Date 
					        	}
							}	
						)
					    response=requests.post(create_url,headers=headers,data=payload,auth=auth)
					    print(response)

				   
				    
				
					getAbsentDependencies(auth,in_report,ScanDate)
				

		
def formatDate(in_date):

	x=in_date.split(" ",4)

	print(x)

	dd=x[1]
	month=x[2]
	yy=x[3]

	if month=='Jan':
	 	mm='01'
	elif month=='Feb':
	 	mm='02'
	elif month=='Mar':
	 	mm='03'
	elif month=='Apr':
	 	mm='04'
	elif month=='May':
	 	mm='05'
	elif month=='June':
	 	mm='06'
	elif month=='Jul':
	 	mm='07'
	elif month=='Aug':
	 	mm='08'
	elif month=='Sep':
	 	mm='09'
	elif month=='Oct':
	 	mm='10'
	elif month=='Nov':
	 	mm='11'
	elif month=='Dec':
	 	mm='12'

	out_date=yy+"-"+mm+"-"+dd

	return out_date

def issueExists(auth,DependencyName):

	list_url="https://cloudidentity.atlassian.net//rest/api/3/search"

	q='project="CI" and summary~"Twistlock DependencyScan {}"'.format(DependencyName)
	query={
	      'jql': q
	    }

	headers={
	    "Accept":"application/json",
	    "Content-Type":"application/json"
	  }


	response=requests.get(list_url,headers=headers,params=query,auth=auth)
	data=response.json()
	issues=data["issues"]

	if len(issues)>0:
	    return 1
	else:
	    return 0

def resolve_issues(auth,key,summary,ScanDate):
  
  make_transition_url="https://cloudidentity.atlassian.net/rest/api/3/issue/{}/transitions".format(key)
  comment_url="https://cloudidentity.atlassian.net//rest/api/3/issue/{}/comment".format(key)

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
        "text":"Issue Resolved, Report dated {} doesnt have it anymore".format(ScanDate),
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
	          	"key":"CI"
	          }
	          },

        "transition": {
               "id": "421"
            } 
      }
      
    )

  response=requests.post(make_transition_url,data=transition_data,headers=headers,auth=auth)

def getAbsentDependencies(auth,in_report,ScanDate):

  print("Get absent Dependencies")


  list_url="https://cloudidentity.atlassian.net//rest/api/3/search"

  headers={
	    "Accept":"application/json",
	    "Content-Type":"application/json"
  }

  query='project="CI" and status!=Done and summary~"{}"'.format("Twistlock DependencyScan")  # no need to resolve already resolved issues

  payload = json.dumps( {
    
	    "jql": query,
	    "maxResults": 200,
    
  } )
  
  response=requests.post(list_url,headers=headers,data=payload,auth=auth)

  data=response.json()   # data = a dictionary 
  issues=data["issues"]  # issues= list of all Dependency Scan issues in Jira

  if len(issues)>0:

	    print("Resolving missing dependecies issues")

	    to_resolve={}
	    for issue in issues:
	      fields=issue["fields"]
	      if fields["summary"] not in in_report:
		        resolve_issues(auth,issue["key"],fields["summary"],ScanDate)
		        to_resolve[issue["key"]]=fields["summary"]

	    print(to_resolve)



def main(user,token,report):

  auth=(user,token)
  createIssues(auth,report)
  
if __name__=="__main__":

  parser=argparse.ArgumentParser(description='Jira Credentials')
  parser.add_argument("JIRA_USER")
  parser.add_argument("JIRA_API_TOKEN")
  parser.add_argument("SCAN_REPORT")

  args=parser.parse_args()
  user=args.JIRA_USER
  token=args.JIRA_API_TOKEN
  report=args.SCAN_REPORT

  main(user,token,report)

