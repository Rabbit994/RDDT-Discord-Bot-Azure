from datetime import datetime
from datetime import timezone
from azure.eventgrid import EventGridClient
from msrest.authentication import TopicCredentials
import Frameworks.CommonFramework as CommonFramework
import hashlib as hashlib

async def publish_event(eventid,subject,data,eventtype):
        config = CommonFramework.RetrieveConfigOptions("eventgrid")
        credentials = TopicCredentials(config['key'])
        event_grid_client = EventGridClient(credentials)
        events=[{
            'id': str(eventid),
            'subject' : str(subject),
            'data': [data],
            'event_time': datetime.now(timezone.utc),
            'event_type': str(eventtype),
            'data_version': 1
            }]    
        event_grid_client.publish_events(config['hostname'],events)