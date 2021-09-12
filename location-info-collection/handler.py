import json
import os

import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))


def post(event, context):
    body: dict = json.loads(event['body'])
    location = body['location']
    table.put_item(
        Item={
            'user_id': body['user_id'],
            'timestamp': body['timestamp'],
            'lat_north_south': location['lat_north_south'],
            'latitude': location['latitude'],
            'lon_west_east': location['lon_west_east'],
            'longitude': location['longitude']
        }
    )
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('success!')
    }
