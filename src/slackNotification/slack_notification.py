import os
from botocore.vendored import requests

"""
Lambda to send a failure alert to a configured webhook on slack
"""
def lambda_handler(event, context):
    """Handles slack alerts for a configured webhook"""
    slack_webhooks = os.environ['SLACK_WEBHOOK'].split(',')
    message = {}
    if 'status' in event:
        message['Error'] = event['taskname'] + 'Error'
        message['Cause'] = event['status']
    elif 'Error' in event:
        message['Error'] = event['Error']
        message['Cause'] = event['Cause']
    send_to_slack(slack_webhooks, message)


def send_to_slack(slack_webhooks, message):
    """Sends message to the configure slack webhook"""
    if not slack_webhooks:
        print('No webhooks provided. Not sending a message...')
        return
    for webhhook in slack_webhooks:
        data = {"text": message}
        response = requests.post(webhhook, json=data)
        response.raise_for_status()
