import sys
import argparse
import json
import requests
import pandas as pd
from auth import auth



keys=["CI-109720","CI-109719","CI-109716","CI-109713"]
for key in keys:

	url="https://cloudidentity.atlassian.net/rest/api/3/issue/{}".format(key)

	response=requests.delete(url=url,auth=auth)

		
	print("Tasks Deleted")



