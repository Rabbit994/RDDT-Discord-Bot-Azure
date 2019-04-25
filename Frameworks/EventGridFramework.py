from datetime import datetime
from azure.eventgrid import EventGridClient
from msrest.authentication import TopicCredentials
import Frameworks.CommonFramework as CommonFramework


def publish_event(event):
        config = CommonFramework.RetrieveConfigOptions("eventgrid")
        credentials = TopicCredentials(config['key'])
        event_grid_client = EventGridClient(credentials)
        events=[{
                'id' : "dbf93d79-3859-4cac-8055-51e3b6b54bea",
                'subject' : "Sample subject",
                'data': {
                    'key': 'Sample Data'
                },
                'event_type': 'SampleEventType',
                'event_time': datetime(2018, 5, 2),
                'data_version': 1
            }]
        event_grid_client.publish_events(config['hostname'],events)