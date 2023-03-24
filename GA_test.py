# Import modules
import pandas as pd
from collections import defaultdict
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
# Authenticate & Build Service
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'no-org-329603-efeb522bcdb4.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
analytics = build('analyticsreporting', 'v4', credentials=credentials)
import json
import csv
# Set Request Parameters

#VIEW_ID = '180230458'
views = {'Short Automaton': '180230458'}
dimensions = ['ga:country','ga:countryIsoCode','ga:region'] # to add dimensions topic
metrics = ['ga:sessions','ga:users'] # to add metric topic
# https://ga-dev-tools.web.app/dimensions-metrics-explorer

# Build request body
body = {
    "reportRequests": [
        {
            "viewId": views['Short Automaton'],
            "dateRanges": [
                {
                    "startDate": "2008-01-01",
                    "endDate": "2022-01-01"
                }
            ],
            #"dimensions": [{'name': dimension} for dimension in dimensions],
            'dimensions': [{'name': 'ga:country'},{'name': 'ga:countryIsoCode'},{'name': 'ga:region'}], # to add dimensions content
            #"metrics": [{'expression': metric} for metric in metrics],
            'metrics': [{'expression': 'ga:sessions'},{'expression': 'ga:users'}], # to add metrics content
            "pageSize": 100000,
            "samplingLevel": "LARGE"
        }
    ]
}

# Make Request
response = analytics.reports().batchGet(body=body).execute()

# Parse Request
report_data = defaultdict(list)

for report in response.get('reports', []):
    rows = report.get('data', {}).get('rows', [])
    #print(rows)
    for row in rows:
        for i, key in enumerate(dimensions):
            report_data[key].append(row.get('dimensions', [])[i])  # Get dimensions
        for values in row.get('metrics', []):
            all_values = values.get('values', [])  # Get metric values
            for i, key in enumerate(metrics):
                report_data[key].append(all_values[i])

report_df = pd.DataFrame(report_data)
print(report_df)
report_df.to_csv('report.csv')