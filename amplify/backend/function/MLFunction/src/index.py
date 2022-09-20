import json
import requests

def handler(event, context):
    print('received event:')
    print(event)
    feed = "https://abcnews.go.com/abcnews/moneyheadlines"
    response = requests.get(feed)
    print(response)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('Hello from lambda!!')
    }