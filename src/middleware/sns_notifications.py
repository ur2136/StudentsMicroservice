import boto3
import json

class Notifications():
    def __init__(self):
        self.s_topic = "arn:aws:sns:us-east-1:614741084428:Students"
        self.sns_client = boto3.client('sns', region_name='us-east-1')


    def list_topics(self):
        response = self.sns_client.list_topics()
        return response

    def publish_notification(self, sns_topic, json_message):
        res = self.sns_client.publish(
            TopicArn = sns_topic,
            Message = json.dumps(json_message, indent=2, default=str),
            Subject = 'Event'
        )

        print("publish_notification response = ",json.dumps(res, indent=2, default=str))

    def add_filter(self, event_filter):
        pass

    def check_publish(self, request, response):
        if self.s_topic:
            if request.method in ['PUT','POST']:
                event = {
                    "URL": request.url,
                    "Method": request.method
                }
                if request.json:
                    event["new_data"] = request.json
                self.publish_notification(self.s_topic, event)
