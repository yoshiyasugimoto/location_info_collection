import base64
import csv
from datetime import datetime, timezone, timedelta
import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))

s3 = boto3.resource('s3')
S3_BUCKET = os.getenv("S3_BUCKET")


def post(event, context):
    body: dict = json.loads(event['body'])
    location = body['location']

    convert_datetime_utc = datetime.fromtimestamp(body['timestamp'])
    convert_datetime_jst = convert_datetime_utc - timedelta(hours=9)
    date: str = convert_datetime_jst.strftime('%Y-%m-%d')
    table.put_item(
        Item={
            'user_id': body['user_id'],
            'date': date,
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


def output_csv(event, context):
    now_jst = datetime.now(timezone(timedelta(hours=9)))
    start_datetime = datetime(now_jst.year, now_jst.month, now_jst.day - 1, 0, 0, 0, 0, tzinfo=timezone(timedelta(hours=9)))
    end_datetime = datetime(now_jst.year, now_jst.month, now_jst.day - 1, 23, 59, 0, 0, tzinfo=timezone(timedelta(hours=9)))
    start_timestamp = int(start_datetime.timestamp())
    end_timestamp = int(end_datetime.timestamp())
    date_str: str = start_datetime.strftime('%Y-%m-%d')

    daily_location_data = []
    last_key = None
    while True:
        option = {
            'KeyConditionExpression':
                Key('date').eq(date_str) & Key('timestamp').between(start_timestamp, end_timestamp)
        }
        if last_key:
            option['ExclusiveStartKey'] = last_key
        result = table.query(**option)
        daily_location_data.extend(result['Items'])
        if 'LastEvaluatedKey' not in result:
            break
        last_key = result['LastEvaluatedKey']

    column_names = ['user_id', 'timestamp', 'lat_north_south', 'latitude', 'lon_west_east', 'longitude']
    daily_location_info_file = f'{date_str}-location-info-collection.csv'
    with open(f'/tmp/{daily_location_info_file}', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=column_names)
        writer.writeheader()
        for d in daily_location_data:
            del d['date']
            writer.writerow(d)

    bucket = s3.Bucket(S3_BUCKET)
    bucket.upload_file(f'/tmp/{daily_location_info_file}', daily_location_info_file)
    return {
        'statusCode': 200,
        'body': json.dumps('success!')
    }


def bucket_list(event, context):
    bucket = s3.Bucket(S3_BUCKET)
    files = [f.key for f in bucket.objects.all()]

    response = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(files)
    }
    return response


def download_csv(event, context):
    path = event.get('pathParameters')
    csv_file = path['file']

    bucket = s3.Bucket(S3_BUCKET)
    bucket.download_file(csv_file, f'/tmp/{csv_file}')

    with open(f"/tmp/{csv_file}", "rb") as f:
        bytes = f.read()
        encode_string = base64.b64encode(bytes)

    return {'statusCode': 200,
            'headers': {
                "Content-Type": "application/zip"
            },
            'body': encode_string.decode()
            }
